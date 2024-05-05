"""
В данном модуле нужно разработать функции для
осуществления CRUD-операций с датасетом
"""

from datetime import datetime
from yadisk import AsyncClient
from rostelecom_bot.utils.config import configuration
from rostelecom_bot.logic.bot_obj import TgBot


async def get_yandex_client() -> AsyncClient:
    """Функция, устанавливающая связь с Яндекс.Диском"""

    client = AsyncClient(token=configuration['YANDEX_TOKEN'])
    if await client.check_token():
        return client
    else:
        raise ValueError


async def async_upload_to_yandex(folder_path: str, file_id: str, file_name: str) -> None:
    """Данная функция создаёт директорию для сохранения файла, если таковая отсутствует,
    и загружает в неё файл, отправленный администратором"""
    
    async with await get_yandex_client() as client:
        try:
            file_info = await TgBot.bot.get_file(file_id)
            file_path = file_info.file_path

            if not await client.is_dir(folder_path):
                await client.mkdir(folder_path)

            src = folder_path + '/' + file_name

            if await client.is_file(src):
                src = folder_path + '/Double-' + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") + '-' + file_name

            await client.upload(await TgBot.bot.download_file(file_path), src)

        except Exception as e:
            raise e


async def check_yandex_disk(folder_path: str) -> str:
    """Данная функция проверяет наличие файлов и их количество
    при присутствии в указанной директории """

    async with await get_yandex_client() as client:
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
            raise e


async def delete_from_yandex_disk(folder_path: str) -> str:
    """Данная функция реализует удаление файлов из указанной директории"""

    async with await get_yandex_client() as client:
        try:
            client = await get_yandex_client()
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
            raise e


async def read_from_yandex_disk(folder_path: str) -> str:
    """Данная функция реализует скачивание данных  из указанной директории"""

    async with await get_yandex_client() as client:
        try:
            if await client.is_dir(folder_path):
                files = await client.listdir(folder_path)
                file_list = [i async for i in files]

                if len(file_list) > 0:
                    for file in file_list:
                        return await client.get_download_link(file['path'])
                else:
                    raise ValueError

        except Exception as e:
            raise e
