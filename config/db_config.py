import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

USERS_TABLE = 'users'
PAYMENTS_TABLE = 'payments'

EXCEL_TABLE_PATH = 'excel/messages.xlsx'
EXCEL_SHEET_NAME = 'data'
