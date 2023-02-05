from typing import List, Dict

from database.models.utils import dbcontrol
from app_types import User
from config.db_config import USERS_TABLE
from config.app_config import TRIAL_FREE, PRICE_MUL


def db_adduser(data: User) -> None:
    """Adds user to DB when it pressed start"""
    data_dict = {}
    for each in data.__annotations__:
        data_dict[each] = data.__getattribute__(each)
    try:
        dbcontrol.insert_db(USERS_TABLE, data_dict)
    except Exception as ex:
        print(ex)


def db_add_minutes(tg_user_id: int, money_amount: int):
    """Adds minutes to selected user and increment spent money"""
    minutes_amount = money_amount * PRICE_MUL
    dbcontrol.update_db(USERS_TABLE, {"minute_balance": minutes_amount}, {"tg_id": tg_user_id})
    money_spent = db_read_spent_money(tg_user_id) + money_amount
    dbcontrol.update_db(USERS_TABLE, {"money_spent": money_spent}, {"tg_id": tg_user_id})


def db_read_spent_money(tg_user_id: int) -> int:
    """Return user minute balance"""
    data_columns = ['tg_id', 'money_spent']
    table_data = dbcontrol.fetchall(USERS_TABLE, data_columns)
    for data in table_data:
        if data.get('tg_id') != tg_user_id:
            pass
        return data.get('money_spent')


def db_read_minute_balance(tg_user_id: int) -> int:
    """Return user minute balance"""
    data_columns = ['tg_id', 'minute_balance']
    table_data = dbcontrol.fetchall(USERS_TABLE, data_columns)
    for data in table_data:
        if data.get('tg_id') != tg_user_id:
            pass
        return data.get('minute_balance')


def db_read_message_data() -> List[User]:
    """Read message data from DB"""
    data_columns = ['tg_id', 'tg_username', 'tg_phone', 'tg_fname', 'tg_lname', 'message', 'timestamp']
    table_data = dbcontrol.fetchall(USERS_TABLE, data_columns)
    data_list = []
    for data in table_data:
        message_data = User(
            tg_id=data.get('tg_id'),
            tg_username=data.get('tg_username'),
            tg_phone=data.get('tg_phone'),
            tg_fname=data.get('tg_fname'),
            tg_lname=data.get('tg_lname'),
            message=data.get('message'),
            timestamp=data.get('timestamp')
        )
        data_list.append(message_data)
    return data_list


def db_get_sorted_data(data_filter: str = None) -> List[User]:
    """Read sorted message data from DB"""
    data_columns = ['tg_id', 'tg_username', 'tg_phone', 'tg_fname', 'tg_lname', 'message', 'timestamp']
    table_data = dbcontrol.sort(USERS_TABLE, data_columns, 'timestamp')
    data_list = []
    for data in table_data:
        message_data = User(
            tg_id=data.get('tg_id'),
            tg_username=data.get('tg_username'),
            tg_phone=data.get('tg_phone'),
            tg_fname=data.get('tg_fname'),
            tg_lname=data.get('tg_lname'),
            message=data.get('message'),
            timestamp=data.get('timestamp')
        )
        data_list.append(message_data)

    if not data_filter:
        return data_list
    filtered_data = []
    for num, data in enumerate(data_list):
        if data_filter in data.timestamp:
            filtered_data.append(data)
    return filtered_data
