"""
Файл с реализацией рабочего интерфейса телеграм-бота
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from rostelecom_bot.utils.config import configuration
from aiogram.fsm.storage.memory import MemoryStorage
from rostelecom_bot.handlers import common_handlers


async def main():
    """Запуск бота"""
    
    bot = Bot(token=configuration['BOT_TOKEN'])
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_router(common_handlers.router)
    
    # Запуск бота и пропуск всех накопленных входящих
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
