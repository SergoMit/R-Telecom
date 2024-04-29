"""
В данном модуле содержатся все состояния, используемые FSMContext для 
корректной работы бота
"""

from aiogram.fsm.state import State, StatesGroup


# Контейнер с id Администратора
class AdminsList:
    ADMIN_ID = []


# Состояния ожидания авторизации, ожидания файла, Администратора, Пользователя
class AuthStates(StatesGroup):
    wait_pass = State()
    wait_file = State()
    ADMIN = State()
    USER = State()
    

# Состояние, активирующее режим запроса
class Region(StatesGroup):
    select=State()


# Контейнер, куда сохраняется состояние до перехода в режим запроса
class PrevState:
    previous = None
