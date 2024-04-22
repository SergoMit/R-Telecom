"""
Здесь указаны хэндлеры, которые обрабатывают запросы,
исходящие как от пользователя, так и от администратора
"""

import rostelecom_bot.utils.phrases as phrase
import rostelecom_bot.utils.keyboard as kb
import rostelecom_bot.utils.async_func as af
import rostelecom_bot.logic.crud as crd
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.enums.content_type import ContentType
from aiogram.filters import StateFilter, BaseFilter
from aiogram.utils.formatting import Text, Bold
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from rostelecom_bot.utils.config import file_extension, configuration


class AdminsList:
    ADMIN_ID = []


class AuthStates(StatesGroup):
    wait_pass = State()
    wait_file = State()
    ADMIN = State()
    USER = State()

# Фильтр, реагирующий на загрузку документов
class DocFilter(BaseFilter):
    def __init__(self, doc_type):
        self.doc_type = doc_type
    
    async def __call__(self, message: types.Message) -> bool:
        return message.content_type == self.doc_type


router = Router()

# Начало взаимодействия с ботом
@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    content = Text(
        "Здравствуйте, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(**content.as_kwargs())
    await message.answer(f'Ваш id: {str(message.from_user.id)}')
    await message.answer(phrase.usr_phrase)
    await state.set_state(AuthStates.USER)


# Команда переключения на профиль пользователя
@router.message(AuthStates.ADMIN, Command("user"))
async def switch_to_user(message: types.Message, state: FSMContext):
    if message.from_user.id not in AdminsList.ADMIN_ID:
        await message.answer("Вы уже Пользователь!")
    else:
        await message.answer("Переключение на профиль пользователя...")
        await af.clear_admin_id(AdminsList.ADMIN_ID)
        await state.set_state(AuthStates.USER)
        await message.answer(phrase.usr_phrase)


# Команда переключения на профиль администратора
@router.message(AuthStates.USER, Command("admin"))
async def switch_to_admin(message: types.Message, state: FSMContext):
    if message.from_user.id in AdminsList.ADMIN_ID:
        await message.answer("Вы уже Администратор!")
    else:
        await message.answer("Вы вошли в режим авторизации. \n\rВведите пароль")
        await state.set_state(AuthStates.wait_pass)


# Отмена авторизации
@router.message(AuthStates.wait_pass, Command("cancel"))
async def cancel_authorization(message: types.Message, state: FSMContext):
    await state.set_state(AuthStates.USER)
    await message.answer("Вы вышли из режима авторизации.")


# Попытка авторизации
@router.message(AuthStates.wait_pass)
async def authorizations(message: types.Message, state: FSMContext):
    if message.text == await af.get_password():
        await message.answer(phrase.adm_phrase)
        await state.set_state(AuthStates.ADMIN)
        await af.add_admin_id(AdminsList.ADMIN_ID, message.from_user.id)
    else:
        await message.answer("Неверный пароль.\
                             \n\rДля выхода из режима авторизации воспользуйтесь командой /cancel")


# Команды, доступные только администратору
@router.message(AuthStates.ADMIN, Command("upload_file"))
async def admin_command(message: types.Message, state: FSMContext):
    if message.from_user.id in AdminsList.ADMIN_ID:
        await state.set_state(AuthStates.wait_file)
        await message.answer("Вы вошли в режим загрузки.\
                             \n\rЗагрузите файл в формате xls.")

    else:
        await message.answer("У вас нет доступа к данной команде.")


# Загрузка на Яндекс.Диск файла, добавленного администратором
@router.message(AuthStates.wait_file, DocFilter(doc_type=ContentType.DOCUMENT))
async def handle_document(message: types.Message, state: FSMContext):
    name_of_file = str(message.document.file_name)
    name_length = len(name_of_file)
    if name_of_file.endswith(file_extension, 0, name_length):
        file_id = message.document.file_id
        success = await crd.async_upload_to_yandex(configuration['DIRECTORY'], file_id, message.document.file_name)
        if success:
            await state.set_state(AuthStates.ADMIN)
            await message.reply("Файл успешно загружен на Яндекс.Диск!")

        else:
            await message.reply("Произошла ошибка при загрузке файла на Яндекс.Диск.")
    else:
        await message.answer("Некорректный формат документа.\
                             \n\rК загрузке допустимы файлы с расширением .xls/.xlsx.")


# Выход из режима загрузки файлов
@router.message(AuthStates.wait_file, Command('cancel_upload'))
async def cancel_upload_file(message: types.Message, state: FSMContext):
    await state.set_state(AuthStates.ADMIN)
    await message.answer("Вы вышли из режима загрузки.")


# Обработка случайных сигналов в режиме ожидания файла
@router.message(AuthStates.wait_file)
async def wait_file_interceptor(message: types.Message):
    await message.answer("Данное сообщение не содержит xls-файл.\
                         \n\rДля выхода из режима загрузки воспользуйтесь командой /cancel_upload")
                                

# Команды, доступные только администратору
@router.message(AuthStates.ADMIN, Command("delete_file"))
async def delete_file_cmd(message: types.Message):
    if message.from_user.id in AdminsList.ADMIN_ID:
        response = await crd.delete_from_yandex_disk(configuration['DIRECTORY'])
        if response:
            await message.answer(response)
        else:
            await message.answer("Произошла ошибка во время удаления файла с Яндекс.Диска.")

    else:
        await message.answer("У вас нет доступа к данной команде.")


# Команды, доступные только администратору
@router.message(AuthStates.ADMIN, Command("modify_file"))
async def modify_file_cmd(message: types.Message):
    if message.from_user.id in AdminsList.ADMIN_ID:
        await message.answer("Файл изменён!")
    else:
        await message.answer("У вас нет доступа к данной команде.")


# Функция, которая доступна как администратору, так и пользователю
@router.message(StateFilter(AuthStates.ADMIN, AuthStates.USER), Command("get_data"))
async def read_data(message: types.Message):
    await message.answer('Выполняю выгрузку данных...')


# Функция, доступная как администратору, так и пользователю
@router.message(StateFilter(AuthStates.ADMIN, AuthStates.USER), Command("check_disk"))
async def check_disk_data(message: types.Message):
    response = await crd.check_yandex_disk(configuration['DIRECTORY'])
    if response:
        await message.answer(response)
    else:
        await message.answer("Произошла ошибка при проверке файлов на Яндекс.Диске.")


# Обработка случайных сигналов
@router.message(StateFilter(AuthStates.ADMIN, AuthStates.USER))
async def signal_interceptor(message: types.Message):
    await message.answer("Команда не распознана. Используйте доступные вам функции.")
