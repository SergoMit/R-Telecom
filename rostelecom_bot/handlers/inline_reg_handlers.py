"""
В данном модуле реализована логика выведения списка регионов пользователю,
а также представлена обработка запроса, задаваемого пользователем
"""

import pandas as pd

from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove, InlineQuery,\
    InlineQueryResultArticle, InputTextMessageContent

import rostelecom_bot.utils.states_obj as st
import rostelecom_bot.utils.keyboard as kb

from rostelecom_bot.logic.crud import read_from_yandex_disk
from rostelecom_bot.utils.config import configuration
from rostelecom_bot.handlers.log_dispatcher import on_error


reg_router = Router()


# Класс-контейнер для хранения промежуточных данных
class Param:
    cur_data = None
    cur_regions = None


async def read(file) -> pd.DataFrame  | bool:
    """Данная функция реализует скачивание данных из указанной директории"""

    return pd.read_excel(file, engine='openpyxl') 
                            

async def regions_list(data: pd.DataFrame) -> list:
    """Данная функция формирует список регионов"""
    
    p = data['Unnamed: 1'].tolist()
    X = list()
    for i in p:
        if str(i).lower() != 'nan':
            X.append(str(i).lower())
    
    X.reverse()
    return X


@reg_router.inline_query(st.Region.select, F.query)
async def show_inline_regions(inline_query: InlineQuery):
    """Данная функция формирует инлайн-отображение регионов"""

    a = []
    b = inline_query.query.lower()
    df_id = 0

    if type(Param.cur_data) is not pd.DataFrame:
        Param.cur_data = await read(await read_from_yandex_disk(configuration['DIRECTORY']))
        Param.cur_regions = await regions_list(Param.cur_data)

    for i in Param.cur_regions:
        df_id += 1
        if b in i:
            a.append(InlineQueryResultArticle(
                id = f'{df_id}',
                title = i,
                description = i,
                input_message_content = InputTextMessageContent(
                message_text = i,
                parse_mode = "HTML"
                ),
            ))
                  
    await inline_query.answer(
        a, is_personal = True,
        switch_pm_text = "Список регионов",
        switch_pm_parameter= "add"
    )    

@reg_router.message(st.Region.select, F.text == 'Покинуть режим запроса 🚪')
async def cancel_get_data(message: types.Message, state: FSMContext):
    """Хэндлер, обрабатывающий выход из режима запроса"""

    if st.PrevState.previous == st.AuthStates.ADMIN:
        await state.set_state(st.AuthStates.ADMIN)
        await message.answer("Вы вышли из режима запроса к данным", reply_markup=kb.admin_kb)
    if st.PrevState.previous == st.AuthStates.USER:
        await state.set_state(st.AuthStates.USER)
        await message.answer("Вы вышли из режима запроса к данным", reply_markup=ReplyKeyboardRemove())
    
    st.PrevState.previous = None



@reg_router.message(st.Region.select)
async def show_celected_data(message: types.Message):
    """Получаем данные из id пользователя телеграм"""
    
    try:
        mes = message.text

        df1 = Param.cur_data[0:1]
        
        df2 = Param.cur_data.loc[Param.cur_data['Unnamed: 1'].str.lower() == mes]

        d = list()
        n = len(df1.columns)

        for i in range(1,n):
            if str(df2[f'Unnamed: {i}'].tolist()) != '[nan]':
                d.append(df1[f'Unnamed: {i}'].tolist() 
                    + df2[f'Unnamed: {i}'].tolist())

        for i in range(0,len(d)):
            await message.answer(str(d[i][0])+' -- '+str(d[i][1])+'\n')

    except Exception as e:
        await on_error(message ,e)
        await message.answer("Произошла ошибка при осуществлении запроса.\
                             \n\rСведения о ней доступны Администратору")       
