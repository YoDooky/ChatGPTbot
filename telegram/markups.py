from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_start_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    user_menu.insert(start_button)
    return user_menu


def get_continue_menu():
    continue_menu = InlineKeyboardMarkup(row_width=1)
    continue_button = InlineKeyboardButton(text='🔁Выбрать другое видео🔁', callback_data='start_app')
    continue_menu.insert(continue_button)
    return continue_menu


def get_approve_menu():
    approve_menu = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text='👍Подтвердить', callback_data='check_balance'),
               InlineKeyboardButton(text='🔁Выбрать другое видео🔁', callback_data='start_app')]
    for button in buttons:
        approve_menu.insert(button)
    return approve_menu


def get_refill_balance_menu():
    approve_menu = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text='💳Пополнить баланс', callback_data='refill_balance'),
               InlineKeyboardButton(text='👈Вернуться назад', callback_data='start_app')]
    for button in buttons:
        approve_menu.insert(button)
    return approve_menu


def get_spent_minutes_menu():
    approve_menu = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text='💸Списать минуты', callback_data='spent_minutes'),
               InlineKeyboardButton(text='👈Вернуться назад', callback_data='start_app')]
    for button in buttons:
        approve_menu.insert(button)
    return approve_menu


def get_collect_data_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    get_all_msg_button = InlineKeyboardButton(text='Получить все сообщения',
                                              callback_data='get_messages')
    get_filtered_msg_button = InlineKeyboardButton(text='Сообщения за определенное время',
                                                   callback_data='get_messages_filtered')
    user_menu.insert(get_all_msg_button)
    user_menu.insert(get_filtered_msg_button)
    return user_menu
