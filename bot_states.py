from aiogram.fsm.state import StatesGroup, State


class PokurimStates(StatesGroup):
    set_name = State()
    set_age = State()
    set_prefs = State()
    idle = State()
    search = State()
