from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from telegram import validate

from telegram import markups
from chatGPT_summary import get_ai_summary


class MessageState(StatesGroup):
    waiting_for_approve = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def user_choice(call: types.CallbackQuery):
        await call.message.answer(text='Скопируйте ссылку на youtube видео и я вам расскажу о чем оно🧐')

    @staticmethod
    async def user_choice_command(message: types.Message):
        await message.answer(text='Скопируйте ссылку на youtube видео и я вам расскажу о чем оно🧐')

    @staticmethod
    async def get_youtube_link(message: types.Message, state: FSMContext):
        if not validate.validate_data(message.text):
            await message.answer('Пожалуйста скопируйте ссылку на видео с youtube, а не другой платформы...')
            return
        await state.update_data(youtube_link=message.text)
        keyboard = markups.get_approve_menu()
        await message.answer("Подтвердите выбор или выберите другое видео", reply_markup=keyboard)

    @staticmethod
    async def approve_choose_video(call: types.CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        youtube_link = user_data.get("youtube_link")
        await call.message.answer('Пожалуйста подождите, идет обработка...')
        try:
            summary_text = get_ai_summary(youtube_link)
            keyboard = markups.get_continue_menu()
            await call.message.answer(f'Краткое описание видео: \n\n{summary_text}', reply_markup=keyboard)
        except Exception as ex:
            await call.message.answer('Не удалось получить краткое описание видео (возможно из-за нагрузки на сервер). '
                                      'Пожалуйста повторите попытку позже...')

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.user_choice, text="start_app")
        dp.register_message_handler(self.user_choice_command, commands="messages")
        dp.register_message_handler(self.get_youtube_link, content_types=["text"], state='*')
        dp.register_callback_query_handler(self.approve_choose_video, text="approve", state='*')

