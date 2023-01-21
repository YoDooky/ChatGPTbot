from typing import List

from database.models.utils import dbcontrol
from app_types import User

from config.db_config import USERS_TABLE


def db_write_message_data(message_data: User):
    """Write message data to DB"""
    data = {
        'tg_id': message_data.tg_id,
        'tg_username': message_data.tg_username,
        'tg_phone': message_data.tg_phone,
        'tg_fname': message_data.tg_fname,
        'tg_lname': message_data.tg_lname,
        'message': message_data.message,
        'timestamp': message_data.timestamp
    }
    try:
        dbcontrol.insert_db(USERS_TABLE, data)
    except Exception as ex:
        print(ex)


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
