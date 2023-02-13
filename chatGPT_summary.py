from __future__ import annotations
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from config.bot_config import CHATGPT_APIKEY
from config.app_config import MAX_VIDEO_TOKENS
from transformers import GPT2TokenizerFast
import textwrap
from googletrans import Translator


class Subtitles:
    def __init__(self, youtube_link):
        self.youtube_link = youtube_link

    @staticmethod
    def __get_en_subtitles(transcript_list, available_lang) -> List | None:
        transcript = None
        for lang in available_lang:
            try:
                transcript = transcript_list.find_transcript([lang])
                break
            except Exception as ex:
                pass
        if transcript:
            translated_transcript = transcript.translate('en')
            return translated_transcript.fetch()
        return transcript

    def __get_youtube_subtitles(self, youtube_link: str) -> List | None:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_link)
        except Exception as ex:
            return None

        available_lang = [transcript.language_code for transcript in transcript_list]
        if 'en' in available_lang:
            return YouTubeTranscriptApi.get_transcript(youtube_link, languages=['en'])
        return self.__get_en_subtitles(transcript_list, available_lang)

    def get_subtitles_text(self):
        video_text = self.__get_youtube_subtitles(self.youtube_link)
        if not video_text:
            return None
        video_text_list = []
        for each in video_text:
            if '[' in each.get('text'):
                continue
            video_text_list.append(each.get('text'))
        return ' '.join(video_text_list)


class VideoSummary:
    def __init__(self, subtitle_text: str, model: str):
        self.subtitle_text = subtitle_text
        self.model = model

    def get_optimized_text(self) -> List[str] | None:
        max_tokens = 1600
        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        number_of_tokens = len(tokenizer(self.subtitle_text)['input_ids'])
        if number_of_tokens > MAX_VIDEO_TOKENS:
            return None
        optimized_text = [self.subtitle_text]
        if number_of_tokens > max_tokens:
            optimized_text = textwrap.wrap(self.subtitle_text, max_tokens * 4)
            optimized_text = [each.strip().replace("\n", "") + "\n\nTl;dr" for each in optimized_text]
        return optimized_text

    @staticmethod
    def set_sum_markers(text) -> str:
        """Added "\n\nTl;dr" to AI understand that we need a summary"""
        return text + "\n\nTl;dr"

    def get_summary(self, text: str, req: str = "") -> str:
        openai.api_key = CHATGPT_APIKEY
        response = openai.Completion.create(
            engine=self.model,
            prompt=f"{req}{text}",
            max_tokens=256,
            stop=None,
            top_p=1,
            temperature=0.7,
        )
        return response.get('choices')[0].get('text')

    def get_final_summary(self) -> str | None:
        optimized_text = self.get_optimized_text()
        if not optimized_text:
            return  # amount of symbols is too big
        if len(optimized_text) == 1:
            if self.model == "text-davinci-003":
                response = self.get_summary(self.set_sum_markers(optimized_text[0]), "Summarize this in 4 bullets:\n\n")
            else:  # for ada model
                response = self.get_summary(self.set_sum_markers(optimized_text[0]))
            return response

        response_list = []
        for text in optimized_text:
            if self.model == "text-davinci-003":
                response = self.get_summary(text, "Summarize this for a second-grade student:\n\n")
            else:  # for ada model
                response = self.get_summary(text, "Summarize this for a second-grade student:\n\n")
            response_list.append(response.strip(':').strip())
        if self.model == "text-davinci-003":
            response = self.get_summary(self.set_sum_markers(''.join(response_list)),
                                        "Summarize this in 4 bullets:\n\n")
        else:  # for ada model
            response = '\n'.join(response_list)
        return response


def get_youtube_link_id(link: str) -> str:
    return link.split('?v=')[-1]


def get_stripped_text(text: str):
    pass


def get_ai_summary(youtube_link: str, language: str = "ru"):
    link_id = get_youtube_link_id(youtube_link)
    video_subtitles = Subtitles(link_id)
    video_en_text = video_subtitles.get_subtitles_text()
    if not video_en_text:
        return 'в выбранном видео не найден текст'

    model = "text-davinci-003"
    video_summary = VideoSummary(video_en_text, model)
    summary_text = video_summary.get_final_summary()

    if not summary_text:
        return 'выбранное видео слишком длинное'

    translator = Translator()
    if language == "en":
        return summary_text.strip(":.; \n")
    ru_text = translator.translate(summary_text, src='en', dest='ru')
    return ru_text.text.strip(":.; \n")
