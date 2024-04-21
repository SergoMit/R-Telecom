"""
В данном модуле нужно разработать функции для 
осуществления CRUD-операций с датасетом
"""

from datetime import datetime
import aiohttp
from yadisk import AsyncClient
from yadisk import YaDisk
from rostelecom_bot.utils.config import configuration
from rostelecom_bot.main import TgBot

# Инициализация асинхронного клиента Яндекс.Диска
client = AsyncClient(token=configuration['YANDEX_TOKEN'])


async def async_upload_to_yandex(file_id: str, file_name):
    async with client:
        if await client.check_token():

            try:
                file_info = await TgBot.bot.get_file(file_id)
                file_path = file_info.file_path

                if not await client.is_dir('/RostelecomBot'):
                    await client.mkdir('/RostelecomBot')
                
                src = '/RostelecomBot/' + file_name

                if await client.is_file(src):
                    src = '/RostelecomBot/Double-' + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") + '-' + file_name
                
                await client.upload(await TgBot.bot.download_file(file_path), src)
                
                return True
            
            except Exception as e:
                print('Ошибка', e)
        
        else:
            return False
        
        
"""
# Инициализация клиента Яндекс.Диска
y = YaDisk(token=configuration['YANDEX_TOKEN'])


async def upload_to_yandex_disk(file_id: str):
    #Данная функция реализует загрузку полученного файла на Яндекс.Диск
    if y.check_token():

        try:
            # Получение информации о файле из Telegram
            file_info = await TgBot.bot.get_file(file_id)
            file_path = file_info.file_path

            # Получение URL для загрузки файла
            file_url = f"https://api.telegram.orgile/bot{configuration['BOT_TOKEN']}/{file_path}"
            
            # Инициализация клиента aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as response:
                    if response.status == 200:

                        # Загрузка файла на Яндекс.Диск
                        async with  y.upload(f"/client/disk/mipt_dataset/{file_path}") as f:
                            await f.write(await response.read())
                            return True
                    else:
                        return False
                    
        except Exception as e:
            print("Ошибка при загрузке файла на Яндекс.Диск", e)
    
    else:
        print("Яндекс.Диск недоступен. Проверьте корректность токена и работоспособность диска")
"""

async def delete_from_yandex_disk():
    pass

async def read_from_yandex_disk():
    pass

async def upload_from_yandex_disk():
    pass

async def modify_through_bot():
    pass