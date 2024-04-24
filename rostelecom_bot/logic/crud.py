"""
В данном модуле нужно разработать функции для 
осуществления CRUD-операций с датасетом
"""

from datetime import datetime
import aiohttp
from yadisk import AsyncClient
from rostelecom_bot.utils.config import configuration
from rostelecom_bot.main import TgBot


async def async_upload_to_yandex(folder_path: str, file_id: str, file_name) -> bool:
    """Данная функция создаёт директорию для сохранения файла, если таковая отсутствует,
    и загружает в неё файл, отправленный администратором"""
    client = AsyncClient(token=configuration['YANDEX_TOKEN'])
    async with client:
        if await client.check_token():
            try:
                file_info = await TgBot.bot.get_file(file_id)
                file_path = file_info.file_path

                if not await client.is_dir(folder_path):
                    await client.mkdir(folder_path)
                
                src = folder_path + '/' + file_name

                if await client.is_file(src):
                    src = folder_path + '/Double-' + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") + '-' + file_name
                
                await client.upload(await TgBot.bot.download_file(file_path), src)
                
                return True
            except Exception as e:
                print('Ошибка', e)
                return False
        else:
            return False


async def check_yandex_disk(folder_path: str) -> str | bool:
    """Данная функция проверяет наличие файлов и их количество
    при присутствии в указанной директории """
    client = AsyncClient(token=configuration['YANDEX_TOKEN'])
    async with client:
        if await client.check_token():
            try:
                if await client.is_dir(folder_path):
                    files = await client.listdir(folder_path)
                    file_list = [i async for i in files]
                    if len(file_list) == 0:
                        return f"Файлов не обнаружено"
                    else:
                        result = f"Обнаружено файлов: {len(file_list)}\n\r\n\r"
                        for file in file_list:
                            result += f"{file['name']}\n\r"
                        return result
                else:
                    return f"Указанная папка не существует.\n\rЧтение невозможно!"
            except Exception as e:
                print('Ошибка', e)
                return False
        else:
            return False


async def delete_from_yandex_disk(folder_path) -> str | bool:
    """Данная функция реализует удаление файлов из указанной директории"""
    client = AsyncClient(token=configuration['YANDEX_TOKEN'])
    async with client:
        if await client.check_token():
            try:
                if await client.is_dir(folder_path):              
                    files = await client.listdir(folder_path)
                    file_list = [i async for i in files]
                    if len(file_list) > 0:
                        for file in file_list:
                            await client.remove(file['path'], permanently=True)
                            return f"Все файлы успешно удалены!"
                    else:
                        return f"Файлов для удаления не найдено."
                else:
                    return f"Указанная папка не существует.\n\rУдаление невозможно!"
            except Exception as e:
                print("Ошибка", e)
                return False
        return False


async def read_from_yandex_disk():
    pass
