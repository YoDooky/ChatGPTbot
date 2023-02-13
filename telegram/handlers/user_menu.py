from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from telegram import validate
from datetime import datetime

from telegram import markups
from chatGPT_summary import get_ai_summary
from database.controllers import message_controller
from aux_func import compare_dates


class MessageState(StatesGroup):
    waiting_for_link = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def user_choice(call: types.CallbackQuery, state: FSMContext):
        if compare_dates(str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')),
                         message_controller.db_read_expiring_period(call.from_user.id)):
            keyboard = markups.get_refill_balance_menu()
            try:
                await call.message.edit_text(text='К сожалению Ваша подписка не активна, '
                                                  'для пополнения нажмите "Пополнить баланс"',
                                             reply_markup=keyboard)
            except Exception as ex:
                await call.message.answer(text='К сожалению Ваша подписка не активна, '
                                               'для пополнения нажмите "Пополнить баланс"',
                                          reply_markup=keyboard)
            return
        await state.set_state(MessageState.waiting_for_link.state)
        await call.message.answer(text='Скопируйте ссылку на youtube видео и я вам расскажу о чем оно🧐')

    @staticmethod
    async def user_choice_command(message: types.Message, state: FSMContext):
        if compare_dates(str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')),
                         message_controller.db_read_expiring_period(message.from_user.id)):
            keyboard = markups.get_refill_balance_menu()
            try:
                await message.edit_text(text='К сожалению Ваша подписка не активна, '
                                             'для пополнения нажмите "Пополнить баланс"',
                                        reply_markup=keyboard)
            except Exception as ex:
                await message.answer(text='К сожалению Ваша подписка не активна, '
                                          'для пополнения нажмите "Пополнить баланс"',
                                     reply_markup=keyboard)
            return
        await state.set_state(MessageState.waiting_for_link.state)
        await message.answer(text='Скопируйте ссылку на youtube видео и я вам расскажу о чем оно🧐')

    @staticmethod
    async def get_youtube_link(message: types.Message, state: FSMContext):
        valid_link = validate.validate_data(message.text)
        if not valid_link:
            await message.answer('Пожалуйста скопируйте ссылку на видео с youtube, а не другой платформы...')
            return
        await state.update_data(youtube_link=valid_link)
        keyboard = markups.get_approve_menu()
        await message.answer("Выберите язык и я вам предоставлю краткое описание видео на нем. "
                             "Либо выберите другое видео", reply_markup=keyboard)

    @staticmethod
    async def approve_ru_choose_video(call: types.CallbackQuery, state: FSMContext):
        """Get RU summary"""
        user_data = await state.get_data()
        youtube_link = user_data.get("youtube_link")
        await call.message.answer('Пожалуйста подождите, идет обработка...')
        try:
            summary_text = get_ai_summary(youtube_link, "ru")
            await state.finish()
            keyboard = markups.get_continue_menu()
            await call.message.answer(f'{summary_text}', reply_markup=keyboard)
        except Exception as ex:
            await state.finish()
            await call.message.answer('Не удалось получить краткое описание видео (возможно из-за нагрузки на сервер). '
                                      'Пожалуйста повторите попытку позже...')

    @staticmethod
    async def approve_en_choose_video(call: types.CallbackQuery, state: FSMContext):
        """Get EN summary"""
        user_data = await state.get_data()
        youtube_link = user_data.get("youtube_link")
        await call.message.answer('Пожалуйста подождите, идет обработка...')
        try:
            summary_text = get_ai_summary(youtube_link, "en")
            await state.finish()
            keyboard = markups.get_continue_menu()
            await call.message.answer(f'{summary_text}', reply_markup=keyboard)
        except Exception as ex:
            await state.finish()
            await call.message.answer('Не удалось получить краткое описание видео (возможно из-за нагрузки на сервер). '
                                      'Пожалуйста повторите попытку позже...')

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.user_choice, text="start_app", state='*')
        dp.register_message_handler(self.user_choice_command, commands="messages", state='*')
        dp.register_message_handler(self.get_youtube_link, content_types=["text"], state=MessageState.waiting_for_link)
        dp.register_callback_query_handler(self.approve_ru_choose_video, text="approve_choice_ru",
                                           state=MessageState.waiting_for_link)
        dp.register_callback_query_handler(self.approve_en_choose_video, text="approve_choice_en",
                                           state=MessageState.waiting_for_link)  # so bad practice but (DRY IT!!!) ... MUST change that
