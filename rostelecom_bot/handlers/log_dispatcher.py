import logging
import os
import traceback
import aiofiles

from aiogram import types
import rostelecom_bot.utils.async_func as af


async def on_error(message: types.Message, exception: Exception):
    """
  Обрабатывает исключения, возникшие в обработчиках сообщений и других функциях, 
  которые вызываются из обработчиков сообщений.
  Сохраняет информацию об исключении в файл error.txt.

    Args:
        message: Сообщение, вызвавшее исключение.
        exception: Исключение, которое было вызвано.
    """
    logging.error("Возникла ошибка во время обработки сообщения:")
    logging.error(traceback.format_exc())
    await save_error(message, exception)
        

async def save_error(message: types.Update, exception: Exception):
    """
    Сохраняет информацию об исключении в файл error.txt.
    Если файла не существует, создает его.

    Args:
        message: Сообщение, вызвавшее исключение.
        exception: Исключение, которое было вызвано.
    """

    try:
        # Получение информации о пользователе и чате
        msg_date = message.date.strftime("%m/%d/%Y, %H:%M:%S")
        user_id = message.from_user.id
        user_name = message.from_user.username if message.from_user.username else "Неизвестно"
        chat_id = message.chat.id
        chat_title = message.chat.title if message.chat.title else "Неизвестно"

        # Формирование сообщения об ошибке
        error_message = f"-------- AN ERROR OCCURED --------\n\r"\
                         f"Date: {msg_date}\n" \
                         f"User ID: {user_id}\n" \
                         f"User name: {user_name}\n" \
                         f"Chat ID: {chat_id}\n" \
                         f"Chat title: {chat_title}\n" \
                         f"Message: {message.text}\n" \
                         f"Exception: {type(exception).__name__}\n"\
                         f"Traceback: {traceback.format_exc()}\n\r"

        # Сохранение сообщения об ошибке в файл
        async with aiofiles.open(os.path.join(os.getcwd(), 'errors.txt'), "a+") as file:
            await file.write(error_message)
    except Exception:
        logging.error("Возникла ошибка во время сохранения ошибки:")
        logging.error(traceback.format_exc())
