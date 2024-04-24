"""
Файл с реализацией рабочего интерфейса телеграм-бота
"""

import asyncio
import logging


from rostelecom_bot.handlers import common_handlers
from rostelecom_bot.logic.bot_obj import TgBot


async def main():
    """Запуск бота"""

    # Регистрация роутеров
    TgBot.dp.include_router(common_handlers.router)
    
    # Запуск бота и пропуск всех накопленных входящих
    await TgBot.bot.delete_webhook(drop_pending_updates=True)
    await TgBot.dp.start_polling(TgBot.bot)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
