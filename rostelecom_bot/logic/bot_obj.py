"""
В данном модуле содержится класс с инициированным ботом
и диспетчером
"""
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher
from rostelecom_bot.utils.config import configuration
from aiogram.fsm.storage.memory import MemoryStorage

class TgBot:
    """Инициализация бота и диспетчера"""
    bot = Bot(token=configuration['BOT_TOKEN'], parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    