import asyncio
import logging
import sys
import traceback
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import ContentType


async def on_error(update: types.Update, exception):
    """
    Обрабатывает исключения, возникшие в обработчиках сообщений.
    Сохраняет информацию об исключении в файл error.txt.

    Args:
        update: Обновление, вызвавшее исключение.
        exception: Исключение, которое было вызвано.
    """
    logging.error("An error occurred while handling an update:")
    logging.error(traceback.format_exc())
    await save_error(update, exception)


async def save_error(update: types.Update, exception: Exception):
    """
    Сохраняет информацию об исключении в файл error.txt.

    Args:
        update: Обновление, вызвавшее исключение.
        exception: Исключение, которое было вызвано.
    """
    try:
        # Получение информации о пользователе и чате
        user_id = update.message.from_user.id
        user_name = update.message.from_user.username if update.message.from_user.username else "Unknown"
        chat_id = update.message.chat.id
        chat_title = update.message.chat.title if update.message.chat.title else "Unknown"

        # Формирование сообщения об ошибке
        error_message = f"User ID: {user_id}\n\rUser name: {user_name}\n\rChat ID: {chat_id}\n\r\
            Chat title: {chat_title}\n\rException: {exception}"

        # Сохранение сообщения об ошибке в файл
        with open("error.txt", "a+") as file:
            file.write(error_message)
    except Exception as e:
        logging.error(f"Возникла ошибка в ходе сохранения ошибки в лог-файл {e}")
        logging.error(traceback.format_exc())
