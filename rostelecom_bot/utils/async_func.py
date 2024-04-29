"""
 В данном модуле содержатся асинхронные функции,
реализующие вспомогательный функционал
"""

from rostelecom_bot.utils.config import configuration


async def clear_admin_id(id_list: list) -> None:
    """Очистка списка с id Администратора"""
    id_list.clear()


async def add_admin_id(id_list: list, adm_id: int) -> None:
    """Добавление id администратора"""
    id_list.append(adm_id)


async def get_password() -> str:
    """Вовращение строкового значения пароля из env-файла"""
    return str(configuration['ADMIN_PASS'])
