from aiogram import Bot
import aioschedule
import asyncio
from glQiwiApi import QiwiP2PClient

from database.controllers import message_controller
import vars_global
from config.app_config import P2P_TOKEN


class Schedule:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def request_payment_status(self, buyer_id: int, payment_message_id: int, last_bill_id: str):
        async with QiwiP2PClient(secret_p2p=P2P_TOKEN) as p2p:
            try:
                status = await p2p.get_bill_status(last_bill_id)
            except Exception as ex:
                aioschedule.clear(f'{buyer_id}')
                print(f'[SHEDULE] {ex}\nThere is no such a bill id...')
        if status == 'PAID':
            aioschedule.clear(f'{buyer_id}')
            message_controller.db_update_payment_bill_id(tg_user_id=buyer_id, bill_id="")
            message_controller.db_add_pay_month(buyer_id)
            expiration_date = message_controller.db_read_expiring_period(buyer_id)
            message_controller.db_update_payment_tg_message_id(tg_user_id=buyer_id,
                                                               message_id=0)
            try:
                await self.bot.delete_message(buyer_id, payment_message_id)
            except Exception as ex:
                pass
            await self.bot.send_message(buyer_id, f"Платеж совершен успешно, дата следующей оплаты:\n{expiration_date}")

    async def scheduler(self):
        """Shedule loop"""
        self.startup_schedule()  # init schedule
        while True:
            if vars_global.update_schedule[0]:
                self.startup_schedule(welcome_text='Updating schedule...')
                vars_global.update_schedule[0] = False
            await aioschedule.run_pending()
            await asyncio.sleep(10)

    def startup_schedule(self, welcome_text: str = 'Starting up schedule...'):
        """Make shedule via DB"""
        print(f'[SHEDULE] {welcome_text}')
        in_progress_payments = message_controller.db_get_payments()
        for payments in in_progress_payments:
            if not payments.get('last_bill_id'):
                continue
            db_buyer_id = payments.get('buyer_id')
            db_payment_message_id = payments.get('payment_message_id')
            db_last_bill_id = payments.get('last_bill_id')
            aioschedule.clear(f'{db_buyer_id}')
            aioschedule.every().minute.do(self.request_payment_status,
                                          buyer_id=db_buyer_id,
                                          payment_message_id=db_payment_message_id,
                                          last_bill_id=db_last_bill_id).tag(f'{db_buyer_id}')
