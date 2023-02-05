import psycopg2
from config import db_config
from config.db_config import USERS_TABLE


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

    def __create_messages_table(self):
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {USERS_TABLE} (
                            id SERIAL PRIMARY KEY,
                            tg_id bigint,
                            tg_username text,
                            tg_phone text,
                            tg_fname text,
                            tg_lname text,
                            minute_balance bigint,
                            money_spent bigint,
                            timestamp text
                            )""")

    def __init_db__(self):
        try:
            self.__create_messages_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create posts table\n'
                  f'[EX] {ex}')
