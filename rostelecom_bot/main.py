"""
Файл с реализацией рабочего интерфейса телеграм-бота
"""

import asyncio
import logging

from rostelecom_bot.handlers import common_handlers, inline_reg_handlers
from rostelecom_bot.logic.bot_obj import TgBot


async def main():
    """Запуск бота"""
    #logging.basicConfig(level=logging.INFO) - раскомментируйте, если нужно отслеживать изменения

    # Регистрация роутеров
    TgBot.dp.include_routers(common_handlers.router, inline_reg_handlers.reg_router)

    # Запуск бота и пропуск всех накопленных входящих
    try:
        await TgBot.bot.delete_webhook(drop_pending_updates=True)
        await TgBot.dp.start_polling(TgBot.bot)
    except KeyboardInterrupt:
        await TgBot.bot.close()
    

if __name__ == "__main__":
    asyncio.run(main())
