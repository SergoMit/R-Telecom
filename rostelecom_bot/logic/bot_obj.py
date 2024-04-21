"""
В данном модуле содержится класс с инициированным ботом
и диспетчером
"""

from aiogram import Bot, Dispatcher
from rostelecom_bot.utils.config import configuration
from aiogram.fsm.storage.memory import MemoryStorage

class TgBot:
    bot = Bot(token=configuration['BOT_TOKEN'])
    dp = Dispatcher(storage=MemoryStorage())
    