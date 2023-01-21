from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot
from aiogram.dispatcher import FSMContext

import aux_func
from telegram import markups


class MessageState(StatesGroup):
    waiting_for_filter = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def user_choice(call: types.CallbackQuery):
        await call.answer()
        await call.message.answer(text='Дайте мне ссылку на youtube видео и я вам расскажу вкратце о чем оно🧐')

    @staticmethod
    async def user_choice_command(message: types.Message):
        await message.answer(text='Дайте мне ссылку на youtube видео и я вам расскажу вкратце о чем оно🧐')

    @staticmethod
    async def get_filter_for_messages(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        await call.message.answer(f'Введите дату в формате "yyyy-mm-dd"\n'
                                  f'например: 2022-12-30')
        await state.set_state(MessageState.waiting_for_filter.state)

    @staticmethod
    async def get_filtered_messages(message: types.Message, state: FSMContext):
        data_filter = message.text
        data_filtered = aux_func.valid_date(data_filter)
        if not data_filtered:
            await message.answer(f'Формат даты не верный. '
                                 f'Убедитесь что формат соответствует "yyyy-mm-dd"\n'
                                 f'например: 2022-12-30')
            return

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.user_choice, text='start_app')
        dp.register_message_handler(self.user_choice_command, commands="messages")
        dp.register_callback_query_handler(self.get_filter_for_messages, text='get_messages_filtered')
        dp.register_message_handler(self.get_filtered_messages, content_types='text',
                                    state=MessageState.waiting_for_filter)
