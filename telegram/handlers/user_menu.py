from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from telegram import validate

import aux_func
from telegram import markups
from chatGPT_summary import get_ai_summary


class MessageState(StatesGroup):
    waiting_for_filter = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def user_choice(call: types.CallbackQuery):
        await call.answer()
        await call.message.answer(text='Скопируйте ссылку на youtube видео и я вам расскажу о чем оно🧐')

    @staticmethod
    async def user_choice_command(message: types.Message):
        await message.answer(text='Скопируйте ссылку на youtube видео и я вам расскажу о чем оно🧐')

    @staticmethod
    async def get_youtube_link(message: types.Message):
        if not validate.validate_data(message.text):
            await message.answer('Пожалуйста скопируйте ссылку на видео с youtube, а не другой платформы...')
            return
        await message.answer('Пожалуйста подождите, идет обработка...')
        summary_text = get_ai_summary(message.text)
        keyboard = markups.get_continue_menu()
        await message.answer(f'Краткое описание видео: \n\n{summary_text}', reply_markup=keyboard)

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.user_choice, text='start_app')
        dp.register_message_handler(self.user_choice_command, commands="messages")
        dp.register_message_handler(self.get_youtube_link, content_types='text')
