from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from telegram import validate

from telegram import markups
from chatGPT_summary import get_ai_summary
from database.controllers import message_controller


class MessageState(StatesGroup):
    waiting_for_approve = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    # Here is decorator to check users available minutes
    # def balance_decorator(self, func):
    #     def wrapper(*args, **kwargs):
    #         if not self.check_user_balance():
    #             await self.bot.send_message(chat_id=, text="На вашем счету низкий баланс")
    #         func(*args, **kwargs)
    #     return wrapper

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

    async def check_user_balance(self, call: types.CallbackQuery, state: FSMContext):
        """Checks user's available minutes amount"""
        available_minutes = message_controller.db_read_minute_balance(call.from_user.id)

        if available_minutes < demand_minutes:
            keyboard = markups.get_refill_balance_menu()
            await call.message.answer(f"На вашем счету недостаточно минут.\n"
                                      f"Доступно: {available_minutes}\nНеобходимо: {demand_minutes}",
                                      reply_markup=keyboard)
            return
        keyboard = markups.get_spent_minutes_menu()
        await call.message.answer(f"Хотите списать {demand_minutes} минут с баланса?\n"
                                  f"Доступно: {available_minutes}", reply_markup=keyboard)

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
        dp.register_callback_query_handler(self.check_user_balance, text="check_balance", state='*')
        dp.register_callback_query_handler(self., text="refill_balance", state='*')
        dp.register_callback_query_handler(self.approve_choose_video, text="spent_minutes", state='*')
