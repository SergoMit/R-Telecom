"""
В данном модуле содержатся клавиатуры, используемые при работе бота
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Загрузить на диск 💾'), KeyboardButton(text='Очистить диск 🗑')],
    [KeyboardButton(text='Запросить логи 📝'), KeyboardButton(text='Очистить логи 🧹')],
    [KeyboardButton(text='Пользователь 🧑‍💻')]
], 
resize_keyboard=True)


cancel_upload_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Покинуть режим загрузки 🚪')]
],
resize_keyboard=True)


cancel_authorisation = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Покинуть авторизацию 🚪')]
], resize_keyboard=True)


cancel_get_data = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Покинуть режим запроса 🚪')]
], resize_keyboard=True)
