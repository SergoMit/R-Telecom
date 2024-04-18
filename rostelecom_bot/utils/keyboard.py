from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_usr_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Администратор'), KeyboardButton(text='Пользователь')]
], 
resize_keyboard=True, input_field_placeholder='Выберите уровень доступа')

usr_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Запросить данные'), KeyboardButton(text='Выйти')]
], 
resize_keyboard=True, input_field_placeholder='Выберите действие')
