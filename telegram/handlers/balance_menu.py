from aiogram import Dispatcher, types
from aiogram import Bot
from aiogram.utils.exceptions import MessageNotModified
from glQiwiApi import QiwiP2PClient

from config.app_config import MONTH_PRICE
import vars_global
from telegram import markups
from database.controllers import message_controller
from config.app_config import P2P_TOKEN


class BalanceMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def refill_balance(self, call: types.CallbackQuery):
        last_payment_message_id = message_controller.db_read_payment_message_id(call.from_user.id)
        if last_payment_message_id:
            await self.bot.delete_message(call.from_user.id, last_payment_message_id)  # delete last payment message

        async with QiwiP2PClient(secret_p2p=P2P_TOKEN) as p2p:
            bill = await p2p.create_p2p_bill(amount=MONTH_PRICE)
            vars_global.update_schedule[0] = True
            message_controller.db_update_payment_bill_id(tg_user_id=call.from_user.id, bill_id=bill.id)
            keyboard = markups.get_payment_link_menu(link=bill.pay_url)
            try:
                pay_msg = await call.message.edit_text(f"Для подписки на месяц ({MONTH_PRICE} RUB) нажмите 'Оплатить'\n"
                                                       f"Для проверки статуса оплаты, нажмите 'Проверить'\n"
                                                       f"Мы пришлем Вам уведомление об оплате",
                                                       reply_markup=keyboard)
            except MessageNotModified:
                pay_msg = await call.message.answer(f"Для подписки на месяц ({MONTH_PRICE} RUB) нажмите 'Оплатить'\n"
                                                    f"Для проверки статуса оплаты, нажмите 'Проверить'\n"
                                                    f"Мы пришлем Вам уведомление об оплате",
                                                    reply_markup=keyboard)
            message_controller.db_update_payment_tg_message_id(tg_user_id=call.from_user.id,
                                                               message_id=pay_msg.message_id)

    @staticmethod
    async def check_payment(call: types.CallbackQuery):
        async with QiwiP2PClient(secret_p2p=P2P_TOKEN) as p2p:
            bill_id = message_controller.db_read_bill_id(call.from_user.id)
            status = await p2p.get_bill_status(bill_id)
        if status == 'WAITING':
            keyboard = markups.check_payment_menu()
            await call.message.answer("Платеж все ещё в обработке, пожалуйста подождите",
                                      reply_markup=keyboard)
        elif status == 'PAID':
            keyboard = markups.get_continue_menu('Вернуться к выбору видео')
            message_controller.db_update_payment_bill_id(tg_user_id=call.from_user.id, bill_id="")
            message_controller.db_add_pay_month(call.from_user.id)
            expiration_date = message_controller.db_read_expiring_period(call.from_user.id)
            message_controller.db_update_payment_tg_message_id(tg_user_id=call.from_user.id,
                                                               message_id=0)
            await call.message.answer(f"Платеж совершен успешно, дата следующей оплаты:\n{expiration_date}\n"
                                      f"Нажмите /messages чтобы продолжить",
                                      reply_markup=keyboard)

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.refill_balance, text="refill_balance")
        dp.register_callback_query_handler(self.check_payment, text="check_payment")
