from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_start_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    user_menu.insert(start_button)
    return user_menu


def get_collect_data_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    get_all_msg_button = InlineKeyboardButton(text='Получить все сообщения',
                                              callback_data='get_messages')
    get_filtered_msg_button = InlineKeyboardButton(text='Сообщения за определенное время',
                                                   callback_data='get_messages_filtered')
    user_menu.insert(get_all_msg_button)
    user_menu.insert(get_filtered_msg_button)
    return user_menu
