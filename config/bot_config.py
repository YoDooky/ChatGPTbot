import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CHATGPT_APIKEY = os.getenv('CHATGPT_APIKEY')
TOKEN = os.getenv('TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
USER_ID = os.getenv('USER_ID')
BOT_ID = int(os.getenv('BOT_ID'))
ACCESS_ID_LIST = [int(os.getenv('ADMIN_1')), int(os.getenv('ADMIN_2'))]

WEBHOOK_PATH = f"/main/{TOKEN}"
APP_URL = os.getenv('APP_URL')
WEBHOOK_URL = APP_URL + WEBHOOK_PATH
