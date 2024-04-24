from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Загрузить на диск'), KeyboardButton(text='Очистить диск')],
    [KeyboardButton(text='Пользователь'), KeyboardButton(text='Запросить логи')]
], 
resize_keyboard=True)


cancel_upload_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Покинуть режим загрузки')]
],
resize_keyboard=True)


cancel_authorisation = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Покинуть авторизацию')]
], resize_keyboard=True)
