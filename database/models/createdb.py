import psycopg2
from config import db_config
from config.db_config import USERS_TABLE, PAYMENTS_TABLE


class DbCreator:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=db_config.DB_HOST,
            dbname=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            port=db_config.DB_PORT,
        )
        self.cursor = self.conn.cursor()

    def __create_users_table(self):
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {USERS_TABLE} (
                            id SERIAL PRIMARY KEY,
                            tg_id bigint,
                            tg_username text,
                            tg_fname text,
                            tg_lname text,
                            timestamp text
                            )""")

    def __create_payments_table(self):
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {PAYMENTS_TABLE} (
                            id SERIAL PRIMARY KEY,
                            buyer_id bigint,
                            usage_expiring text,
                            money_spent bigint,
                            last_bill_id text,
                            payment_message_id bigint,
                            timestamp text
                            )""")

    def __init_db__(self):
        try:
            self.__create_users_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create "users" table\n'
                  f'[EX] {ex}')

        try:
            self.__create_payments_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create "payments" table\n'
                  f'[EX] {ex}')
