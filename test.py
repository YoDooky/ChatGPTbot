from youtube_transcript_api import YouTubeTranscriptApi
import openai
from config.bot_config import CHATGPT_APIKEY
from transformers import GPT2TokenizerFast


def get_tokens_number(text):
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    number_of_tokens = len(tokenizer(text)['input_ids'])
    return number_of_tokens


def get_youtube_subtitles(youtube_link):
    transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_link)
    available_lang = [transcript.language_code for transcript in transcript_list]
    if 'en' in available_lang:
        return YouTubeTranscriptApi.get_transcript(youtube_link, languages=['en'])
    transcript = transcript_list.find_transcript(available_lang)
    translated_transcript = transcript.translate('en')
    return translated_transcript.fetch()


def get_subtitles_text(video_text):
    video_text_list = []
    for each in video_text:
        if '[' in each.get('text'):
            continue
        video_text_list.append(each.get('text'))
    return ' '.join(video_text_list)


def get_summary(subtitle_text):
    req = "summarize in 4 bullets"
    openai.api_key = CHATGPT_APIKEY
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{req}: {subtitle_text}",
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.get('choices')[0].get('text')


def main():
    link = "PqJ2iua6Ick&ab_channel=HeARTwood"
    video_text = get_youtube_subtitles(link)
    subtitle_text = get_subtitles_text(video_text)
    print(subtitle_text)
    # summary_text = get_summary(subtitle_text)


if __name__ == '__main__':
    # prompt = "hello dear viewers subscribers welcome to the heartwood channel my name is michael the topic of today's video of making such a circle and wooden sticks the range of their application is quite extensive it can be dowels for assembling furniture details of a children's designer knitting needles hairpins or anything else I have enough imagination for such sticks are needed in order to insert here, paste into these holes, this will be a suspension for wooden doses of points, in fact, there are a lot of options for making such sticks, it can be an old die for threading a suitable diameter and a wooden jig with a chisel, also a lathe, a milling table, everything anything, but I wanted to offer you my, in my opinion, very simple quick way how to make such sticks for making a jig, we need a massive steel plate, in this case I found this 12 millimeters and also a small strip of steel 45 millimeters thick, we also need two drills one a drill of such a diameter as we want them with wooden sticks and a second drill thinner than 45 millimeters, the diameter is not important, and of course, we need a drill in a rack or a drilling machine, first of all we put a large diameter drill and we will need to make two drillings, one drilling is done through and the second it is done in a depth of about two to three millimeters, I choose a place arbitrarily, it doesn’t matter much, but we need to drill the next hole so that it either touches or slightly overlaps, this is our preliminary drilling, you see the hole blocked each other for drilling 2 holes that will be through they definitely need to use oil because we need very smooth walls. if drilling without oil, it is quite possible that a scuff is formed and on the walls, which is not very good, as you understand, we will scroll the rail through this hole, this drilling was necessary in order to form a cutting tooth but since we will be behind to rule a non-round square rail here, then you still need to do a preliminary removal of the material for this and you need this plate here I made a sharp sharpened tooth now we will drill a hole here it will need to adjust the position of the tooth relative to the hole first I level the plate so that it lines up with its tooth with the center of the hole and shifting in such a way that about one millimeter remains to the edge of the hole, I place the shanks approximately in the middle, all that remains to be done is to connect the bases together and this additional element I will put a few washers, this is necessary in order to provide a little distance between the base and with a cutter, this will eliminate the stuffing of chips under the cutter and then fixing tightening the nut, the opposite side can be fixed either with hand flowers or pliers with a lock, now we just have to slightly prepare the plan, I sawed these blanks with a cross section of about 9 by 9 millimeters we just need to force the ditch in order to correctly fill the reverse side into this hole if you need to slightly grind it, but in principle, it fits into the door normally for me, that's what we got as a result, practically here we need very little grinding by tilting the bar, you can adjust the preliminary the material is removed, as you can see, the removal takes place twice, that is, the first removal and now the second cutting teeth into the holes, so with the help of such a simple jig made in a matter of minutes, you can make such round wooden sticks sticks can be made of absolutely any diameter, I had to make sticks with a diameter from 5 to 12 millimeters in any case, this jig works fine, I hope that this video will be useful to you, do not forget to subscribe to the channel, like everyone for now"
    # prompt = "здравствуйте уважаемые зрители подписчики добро пожаловать на канал хартвуд меня зовут михаил тема сегодняшнего видео изготовления вот таких круг и деревянных палочек спектр их применения довольно обширен это могут быть шканты для сборки мебели детали детского конструктора вязальные спицы шпильки для волос либо все на что еще хватит фантазии мне такие палочки нужны для того чтобы вставить вот вклеить в эти отверстия это будет подвес для деревянных доз точек на самом деле вариантов изготовления таких палочек очень много это может быть и старая плашка для нарезания резьбы подходящего диаметра и деревянный кондуктор со стамеской также токарный станок фрезерный стол все что угодно но я хотел предложить вам свой на мой взгляд очень несложный быстрый способ как изготовить такие палочки для изготовления кондуктора нам потребуется массивная стальная пластина в данном случае я нашел такой 12 миллиметров а также небольшая полоса стали толщиной 45 миллиметров также нам потребуется два сверла одно сверло такого диаметра какие мы хотим ими деревянные палочки и второе сверло потоньше 45 миллиметров диаметр не важен ну и естественно что нам потребуется дрель в стойке либо сверлильный станок прежде всего мы ставим сверло большого диаметра и нам нужно будет сделать два сверления одно сверление делается насквозь а второе делается в на глубину порядка двух трех миллиметров место я выбираю произвольно это большого значения не имеет а вот следующее отверстие нам надо просверлить так чтобы она либо коснулась либо слегка перекрыла вот это наше предварительное сверление вот видите отверстие перекрыли друг друга для сверления 2 отверстия которое будет сквозь ним обязательно нужно использовать масло потому что нам нужны очень гладкие стенки если сверлить без масла то вполне возможно что образуется задир и на стенках что не очень хорошо как вы понимаете мы будем прокручивать рейку через вот это отверстие вот это сверление нужно было для того чтобы образовать режущий зуб но так как мы будем заправлять сюда не круглая квадратную рейку то нужно еще сделать предварительный съём материала для этого и нужна вот этого пластинка здесь я сделал острый заточенный зуб сейчас мы просверлим вот здесь отверстие она нужно будет для того чтобы регулировать положение зуба относительно отверстия сначала ровняю пластину так чтобы она поравнялась своим зубцом с центром отверстия и сдвигая таким образом чтобы оставалось примерно около одного миллиметра до края отверстия хвостовики располагаю примерно посередине все что остается сделать это соединить между собой основания и вот этот дополнительный элемент я положу несколько шайбочек это нужно для того чтобы немножко обеспечить дистанцию между основанием и резцом это исключит набивание стружек под резец и дальше фиксируя затягиваю гайку противоположную сторону можно зафиксировать либо ручными цветками либо пассатижами с фиксатором теперь нам остаётся только слегка подготовить план я напилил вот такие заготовочки сечением примерно 9 на 9 миллиметров нам нужно всего лишь заставить для того чтобы правильно заправить вот в это отверстие обратную сторону если нужно слегка подточить но в принципе у меня и так вставляется в дверь нормально вот что у нас получилось в итоге практически здесь требуется совсем небольшая шлифовка наклоном планки можно регулировать предварительный съём материала как видите съем происходит за два раза то есть первый съем и вот второй уже режущим зубам в отверстия итак при помощи вот такого несложного кондуктор изготовленного за считанные минуты можно делать вот такие круглые деревянные палочки палочки можно сделать совершенно любого диаметра мне приходилось изготавливать палочки диаметром от 5 до 12 миллиметров в любом случае этот кондуктор работает отлично я надеюсь что это видео будет вам полезно не забывайте подписываться на канал ставить лайки всем пока"
    # print(get_tokens_number(prompt))
    main()
