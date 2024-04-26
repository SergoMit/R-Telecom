"""
В данном модуле содержатся все состояния, используемые FSMContext для 
корректной работы бота
"""

from aiogram.fsm.state import State, StatesGroup


class AdminsList:
    ADMIN_ID = []


class AuthStates(StatesGroup):
    wait_pass = State()
    wait_file = State()
    ADMIN = State()
    USER = State()
    
    
class Region(StatesGroup):
    select=State()


class PrevState:
    previous = None
