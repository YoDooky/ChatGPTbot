import asyncio

from glQiwiApi import QiwiP2PClient
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

p2p_token = os.getenv('P2P_TOKEN')


async def create_p2p_bill():
    async with QiwiP2PClient(secret_p2p=p2p_token) as p2p:
        bill = await p2p.create_p2p_bill(amount=1)
        print(f"Link to pay bill with {bill.id} id = {bill.pay_url}")
        # print(bill.id)
        # print(await p2p.get_bill_status("df978efe-b31a-4b17-b1c4-5fd559684174"))


asyncio.run(create_p2p_bill())
"PAID"
"WAITING"
