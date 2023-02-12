import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

FREE_DAYS_TRIAL = 0  # amount of free trial days for user
MONTH_PRICE = 1
P2P_TOKEN = os.getenv('P2P_TOKEN')
