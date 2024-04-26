"""
Здесь указаны хэндлеры, которые обрабатывают запросы,
исходящие как от пользователя, так и от администратора
"""
import logging
import traceback
import rostelecom_bot.utils.phrases as phrase
import rostelecom_bot.utils.keyboard as kb
import rostelecom_bot.utils.async_func as af
import rostelecom_bot.logic.crud as crd
import rostelecom_bot.utils.states_obj as st

from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.enums.content_type import ContentType
from aiogram.filters import StateFilter, BaseFilter
from aiogram.utils.formatting import Text, Bold
from aiogram.fsm.context import FSMContext

from rostelecom_bot.utils.config import file_extension, configuration


# Фильтр, реагирующий на загрузку документов
class DocFilter(BaseFilter):
    def __init__(self, doc_type):
        self.doc_type = doc_type
    
    async def __call__(self, message: types.Message) -> bool:
        return message.content_type == self.doc_type
    

router = Router()


# Начало взаимодействия с ботом
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    content = Text(
        "Здравствуйте, Пользователь ",
        Bold(message.from_user.full_name)
    )
    await message.answer(**content.as_kwargs(), reply_markup=ReplyKeyboardRemove())
    await af.clear_admin_id(st.AdminsList.ADMIN_ID)
    await state.set_state(st.AuthStates.USER)
    await message.answer("Список доступных команд указан в меню чат-бота")


# Команда переключения на профиль пользователя
@router.message(st.AuthStates.ADMIN, F.text == 'Пользователь')
async def switch_to_user(message: types.Message, state: FSMContext):
    if message.from_user.id not in st.AdminsList.ADMIN_ID:
        await message.answer("Вы уже Пользователь!")
    else:
        await af.clear_admin_id(st.AdminsList.ADMIN_ID)
        await state.set_state(st.AuthStates.USER)
        await message.answer(phrase.greeting_usr, reply_markup=ReplyKeyboardRemove())


# Команда переключения на профиль администратора
@router.message(st.AuthStates.USER, Command("admin"))
async def switch_to_admin(message: types.Message, state: FSMContext):
    if message.from_user.id in st.AdminsList.ADMIN_ID:
        await message.answer("Вы уже Администратор!")
    else:
        await message.answer("Вы вошли в режим авторизации. \n\rВведите пароль", reply_markup=kb.cancel_authorisation)
        await state.set_state(st.AuthStates.wait_pass)


# Отмена авторизации
@router.message(st.AuthStates.wait_pass, F.text == 'Покинуть авторизацию')
async def cancel_authorization(message: types.Message, state: FSMContext):
    await state.set_state(st.AuthStates.USER)
    await message.answer("Вы вышли из режима авторизации", reply_markup=ReplyKeyboardRemove())


# Попытка авторизации
@router.message(st.AuthStates.wait_pass)
async def authorizations(message: types.Message, state: FSMContext):
    if message.text == await af.get_password():
        await message.answer(phrase.greeting_adm, reply_markup=kb.admin_kb)
        await state.set_state(st.AuthStates.ADMIN)
        await af.add_admin_id(st.AdminsList.ADMIN_ID, message.from_user.id)
    else:
        await message.answer("Неверный пароль.\
                             \n\rДля выхода из режима авторизации нажмите на кнопку 'Покинуть авторизацию'")


# Команды, доступные только администратору
@router.message(st.AuthStates.ADMIN, F.text == 'Загрузить на диск')
async def admin_command(message: types.Message, state: FSMContext):
    if message.from_user.id in st.AdminsList.ADMIN_ID:
        await state.set_state(st.AuthStates.wait_file)
        await message.answer("Вы вошли в режим загрузки.\
                             \n\rЗагрузите файл в формате xls", reply_markup=kb.cancel_upload_kb)

    else:
        await message.answer("У вас нет доступа к данной команде")


# Загрузка на Яндекс.Диск файла, добавленного администратором
@router.message(st.AuthStates.wait_file, DocFilter(doc_type=ContentType.DOCUMENT))
async def handle_document(message: types.Message, state: FSMContext):
    name_of_file = str(message.document.file_name)
    name_length = len(name_of_file)
    if name_of_file.endswith(file_extension, 0, name_length):
        file_id = message.document.file_id
        success = await crd.async_upload_to_yandex(configuration['DIRECTORY'], file_id, message.document.file_name)
        if success:
            await state.set_state(st.AuthStates.ADMIN)
            await message.reply("Файл успешно загружен на Яндекс.Диск!", reply_markup=kb.admin_kb)

        else:
            await message.reply("Произошла ошибка при загрузке файла на Яндекс.Диск")
    else:
        await message.answer("Некорректный формат документа.\
                             \n\rК загрузке допустимы файлы с расширением .xls/.xlsx")


# Выход из режима загрузки файлов
@router.message(st.AuthStates.wait_file, F.text == 'Покинуть режим загрузки')
async def cancel_upload_file(message: types.Message, state: FSMContext):
    await state.set_state(st.AuthStates.ADMIN)
    await message.answer("Вы вышли из режима загрузки", reply_markup=kb.admin_kb)


# Обработка случайных сигналов в режиме ожидания файла
@router.message(st.AuthStates.wait_file)
async def wait_file_interceptor(message: types.Message):
    await message.answer("Данное сообщение не содержит xls-файл.\
                         \n\rДля выхода из режима загрузки нажмите кнопку 'Покинуть режим загрузки'")
                                

# Команды, доступные только администратору
@router.message(st.AuthStates.ADMIN, F.text == 'Очистить диск')
async def delete_file_cmd(message: types.Message):
    if message.from_user.id in st.AdminsList.ADMIN_ID:
        response = await crd.delete_from_yandex_disk(configuration['DIRECTORY'])
        if response:
            await message.answer(response)
        else:
            await message.answer("Произошла ошибка во время удаления файла с Яндекс.Диска")

    else:
        await message.answer("У вас нет доступа к данной команде")


# Команды, доступные только администратору
@router.message(st.AuthStates.ADMIN, F.text == "Запросить логи")
async def send_log_file(message: types.Message):
    if message.from_user.id in st.AdminsList.ADMIN_ID:
        try:
            with open("errors.txt", "rb") as file:
                document = types.InputFile(file)
                await message.reply_document(document)
        except Exception as e:
            await message.answer(f"Возникла ошибка в ходе запроса лог-файла: {e}")
            logging.error(traceback.format_exc())


# Функция, включённая в меню бота (общедоступная)
@router.message(StateFilter(st.AuthStates.ADMIN, st.AuthStates.USER), Command("get_data"))
async def read_data(message: types.Message, state: FSMContext):
    st.PrevState.previous = await state.get_state()
    await state.set_state(st.Region.select)
    await message.answer('Вы вошли в режим работы с данными.\
                          \n\rСкопируйте имя бота в строку ввода и начните вводить регион', reply_markup=kb.cancel_get_data)
    await message.answer('@Samanter_bot')


# Функция, включённая в меню бота (общедоступная)
@router.message(StateFilter(st.AuthStates.ADMIN, st.AuthStates.USER), Command("check_disk"))
async def check_disk_data(message: types.Message):
    response = await crd.check_yandex_disk(configuration['DIRECTORY'])
    if response:
        await message.answer(response)
    else:
        await message.answer("Произошла ошибка при проверке файлов на Яндекс.Диске")


# Функция, включённая в меню бота (общедоступная)
@router.message(Command("help"))
async def help_function(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == st.AuthStates.ADMIN:
        await message.answer(phrase.adm_phrase)

    elif current_state == st.AuthStates.USER:
        await message.answer(phrase.usr_phrase)

    await message.answer(phrase.phrase_help)


# Функция, включённая в меню бота (общедоступная)
@router.message(Command("quit"))
async def quit_function(message: types.Message, state: FSMContext):
    await message.answer(phrase.bye_phrase, reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Обработка случайных сигналов
@router.message(StateFilter(st.AuthStates.ADMIN, st.AuthStates.USER))
async def signal_interceptor(message: types.Message):
    await message.answer("Команда не распознана. Обратитесь к меню чат-бота")
