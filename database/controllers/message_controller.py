from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.models.utils import dbcontrol
from app_types import User, Payment
from config.db_config import USERS_TABLE, PAYMENTS_TABLE
from config.app_config import MONTH_PRICE


def db_add_user(data: User) -> None:
    """Adds user to DB when he pressed start"""
    data_dict = {}
    for each in data.__annotations__:
        data_dict[each] = data.__getattribute__(each)
    try:
        dbcontrol.insert_db(USERS_TABLE, data_dict)
    except Exception as ex:
        print(ex)


def db_add_payment(data: Payment) -> None:
    """Adds payment to DB when he pressed start"""
    data_dict = {}
    for each in data.__annotations__:
        data_dict[each] = data.__getattribute__(each)
    try:
        dbcontrol.insert_db(PAYMENTS_TABLE, data_dict)
    except Exception as ex:
        print(ex)


def db_read_bill_id(tg_user_id: int) -> str:
    data_columns = ['buyer_id', 'last_bill_id']
    table_data = dbcontrol.fetchall(PAYMENTS_TABLE, data_columns)
    for data in table_data:
        if data.get('buyer_id') != tg_user_id:
            pass
        return data.get('last_bill_id')


def db_read_payment_message_id(tg_user_id: int) -> str:
    data_columns = ['buyer_id', 'payment_message_id']
    table_data = dbcontrol.fetchall(PAYMENTS_TABLE, data_columns)
    for data in table_data:
        if data.get('buyer_id') != tg_user_id:
            pass
        return data.get('payment_message_id')


def db_update_payment_bill_id(tg_user_id: int, bill_id: str):
    """Updates status of payment"""
    dbcontrol.update_db(PAYMENTS_TABLE, {"buyer_id": tg_user_id}, {"last_bill_id": bill_id})


def db_update_payment_tg_message_id(tg_user_id: int, message_id: int):
    """Updates status of payment"""
    dbcontrol.update_db(PAYMENTS_TABLE, {"buyer_id": tg_user_id}, {"payment_message_id": message_id})


def db_get_payments():
    data_columns = ['buyer_id', 'usage_expiring', 'money_spent', 'last_bill_id', 'payment_message_id']
    table_data = dbcontrol.fetchall(PAYMENTS_TABLE, data_columns)
    return table_data


def db_get_users() -> List:
    data_columns = ['tg_id']
    table_data = dbcontrol.fetchall(USERS_TABLE, data_columns)
    existed_users = [data.get('tg_id') for data in table_data]
    return existed_users


def db_add_pay_month(tg_user_id: int):
    """Adds month to usage expiring"""
    next_pay_date = db_read_expiring_period(tg_user_id)
    datetime_object = datetime.strptime(next_pay_date, '%Y-%m-%d %H:%M:%S')  # convert to datetime data from DB
    next_pay_date = str(datetime_object + relativedelta(months=1))
    dbcontrol.update_db(PAYMENTS_TABLE, {"buyer_id": tg_user_id}, {"usage_expiring": next_pay_date})
    money_spent = db_read_spent_money(tg_user_id) + MONTH_PRICE
    dbcontrol.update_db(PAYMENTS_TABLE, {"buyer_id": tg_user_id}, {"money_spent": money_spent})


def db_read_spent_money(tg_user_id: int) -> int:
    """Return user minute balance"""
    data_columns = ['buyer_id', 'money_spent']
    table_data = dbcontrol.fetchall(PAYMENTS_TABLE, data_columns)
    for data in table_data:
        if data.get('buyer_id') != tg_user_id:
            pass
        return data.get('money_spent')


def db_read_expiring_period(tg_user_id: int) -> str:
    """Return user usage expiring date"""
    data_columns = ['buyer_id', 'usage_expiring']
    table_data = dbcontrol.fetchall(PAYMENTS_TABLE, data_columns)
    for data in table_data:
        if data.get('buyer_id') != tg_user_id:
            pass
        return data.get('usage_expiring')

# def db_read_message_data() -> List[User]:
#     """Read message data from DB"""
#     data_columns = ['tg_id', 'tg_username', 'tg_phone', 'tg_fname', 'tg_lname', 'message', 'timestamp']
#     table_data = dbcontrol.fetchall(USERS_TABLE, data_columns)
#     data_list = []
#     for data in table_data:
#         message_data = User(
#             tg_id=data.get('tg_id'),
#             tg_username=data.get('tg_username'),
#             tg_phone=data.get('tg_phone'),
#             tg_fname=data.get('tg_fname'),
#             tg_lname=data.get('tg_lname'),
#             usage_expiring=data.get('usage_expiring'),
#             money_spent=data.get('money_spent'),
#             timestamp=data.get('timestamp')
#         )
#         data_list.append(message_data)
#     return data_list
#
#
# def db_get_sorted_data(data_filter: str = None) -> List[User]:
#     """Read sorted message data from DB"""
#     data_columns = ['tg_id', 'tg_username', 'tg_phone', 'tg_fname', 'tg_lname', 'message', 'timestamp']
#     table_data = dbcontrol.sort(USERS_TABLE, data_columns, 'timestamp')
#     data_list = []
#     for data in table_data:
#         message_data = User(
#             tg_id=data.get('tg_id'),
#             tg_username=data.get('tg_username'),
#             tg_phone=data.get('tg_phone'),
#             tg_fname=data.get('tg_fname'),
#             tg_lname=data.get('tg_lname'),
#             message=data.get('message'),
#             timestamp=data.get('timestamp')
#         )
#         data_list.append(message_data)
#
#     if not data_filter:
#         return data_list
#     filtered_data = []
#     for num, data in enumerate(data_list):
#         if data_filter in data.timestamp:
#             filtered_data.append(data)
#     return filtered_data
