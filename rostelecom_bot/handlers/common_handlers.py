"""
Здесь указаны хэндлеры, которые обрабатывают запросы,
исходящие как от пользователя, так и от администратора
"""

import rostelecom_bot.utils.phrases as phrase
import rostelecom_bot.utils.keyboard as kb
import rostelecom_bot.utils.async_func as af

from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.formatting import Text, Bold
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from rostelecom_bot.utils.config import configuration


class AdminsList:
    ADMIN_ID = []


class AuthStates(StatesGroup):
    wait_pass = State()
    ADMIN = State()
    USER = State()


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
        await message.answer("Вы уже Пользователь")
    else:
        await message.answer("Переключение на профиль пользователя...")
        await af.clear_admin_id(AdminsList.ADMIN_ID)
        await state.set_state(AuthStates.USER)


# Команда переключения на профиль администратора
@router.message(AuthStates.USER, Command("admin"))
async def switch_to_admin(message: types.Message, state: FSMContext):
    if message.from_user.id in AdminsList.ADMIN_ID:
        await message.answer("Вы уже Администратор")
    else:
        await message.answer("Вы вошли в режим авторизации. \n\rВведите пароль")
        await state.set_state(AuthStates.wait_pass)


# Отмена авторизации
@router.message(AuthStates.wait_pass, Command("cancel"))
async def cancel_authorization(message: types.Message, state: FSMContext):
    await state.set_state(AuthStates.USER)
    await message.answer("Вы вышли из режима авторизации")


# Попытка авторизации
@router.message(AuthStates.wait_pass)
async def authorizations(message: types.Message, state: FSMContext):
    if message.text == await af.get_password():
        await message.answer(phrase.adm_phrase)
        await state.set_state(AuthStates.ADMIN)
        await af.add_admin_id(AdminsList.ADMIN_ID, message.from_user.id)
    else:
        await message.answer("Неверный пароль. Для выхода из режима авторизации воспользуйтесь командой /cancel")


# Команды, доступные только администратору
@router.message(AuthStates.ADMIN, Command("upload_file"))
async def admin_command(message: types.Message):
    if message.from_user.id in AdminsList.ADMIN_ID:
        await message.answer("Выполняется загрузка файла")
    else:
        await message.answer("У вас нет доступа к данной команде")


# Команды, доступные только администратору
@router.message(AuthStates.ADMIN, Command("delete_file"))
async def delete_file_cmd(message: types.Message):
    if message.from_user.id in AdminsList.ADMIN_ID:
        await message.answer("Файл стёрт с удалённого диска")
    else:
        await message.answer("У вас нет доступа к данной команде")


# Команды, доступные только администратору
@router.message(AuthStates.ADMIN, Command("modify_file"))
async def modify_file_cmd(message: types.Message):
    if message.from_user.id in AdminsList.ADMIN_ID:
        await message.answer("Файл изменён")
    else:
        await message.answer("У вас нет доступа к данной команде")


# Функция, которая доступна как администратору, так и пользователю
@router.message(StateFilter(AuthStates.ADMIN, AuthStates.USER), Command("get_data"))
async def read_data(message: types.Message):
    await message.answer('Выполняю выгрузку данных...')


# Обработка случайных сигналов
@router.message(StateFilter(AuthStates.ADMIN, AuthStates.USER))
async def signal_interceptor(message: types.Message):
    await message.answer('Команда не распознана. Используйте доступные вам функции')
