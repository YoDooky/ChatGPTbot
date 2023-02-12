from aiogram import types, Dispatcher
from telegram import markups
from aiogram.dispatcher import FSMContext
from database.controllers import message_controller
from datetime import datetime
from app_types import User, Payment
from dateutil.relativedelta import relativedelta

from config.app_config import FREE_DAYS_TRIAL


async def start_command(message: types.Message, state: FSMContext):
    if message.chat.type != 'private':  # start only in private messages
        return
    await state.finish()
    keyboard = markups.get_start_menu()
    if message.from_user.id not in message_controller.db_get_users():
        trial_period = datetime.strftime(datetime.now() + relativedelta(days=FREE_DAYS_TRIAL), '%Y-%m-%d %H:%M:%S')
        message_controller.db_add_user(User(tg_id=message.from_user.id,
                                            tg_username=message.from_user.username,
                                            tg_fname=message.from_user.first_name,
                                            tg_lname=message.from_user.last_name,
                                            timestamp=str(datetime.now())))
        message_controller.db_add_payment(Payment(buyer_id=message.from_user.id,
                                                  usage_expiring=str(trial_period),
                                                  money_spent=0,
                                                  last_bill_id="",
                                                  payment_message_id=0,
                                                  timestamp=str(datetime.now())))
        await message.answer("👋Добро пожаловать в бот для получения summary с youtube!\n"
                             "Я умею делать краткое описание того что происходит в видео🧠"
                             f"Вам начислено {FREE_DAYS_TRIAL} бесплатных дня для пользования.",
                             reply_markup=keyboard)
        return
    await message.answer("👋С возвращением!\n"
                         "Я умею делать краткое описание того что происходит в видео🧠",
                         reply_markup=keyboard)


def register_handlers(dp: Dispatcher):
    """Register message handlers"""
    dp.register_message_handler(start_command, commands="start")
