"""
Файл с реализацией рабочего интерфейса телеграм-бота
"""
import telebot
from telebot import types


token = 'YOUR TOKEN'  # Замените 'YOUR_TOKEN' на ваш токен бота
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Администратор', callback_data='button1')
    button2 = types.InlineKeyboardButton('Пользователь', callback_data='button2')
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, 'Выберите профиль:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'button1':
        bot.send_message(call.message.chat.id, 'Введите пароль')
    elif call.data == 'button2':
        bot.send_message(call.message.chat.id, 'Что я могу для вас сделать?')


if __name__ == '__main__':
    bot.infinity_polling()
