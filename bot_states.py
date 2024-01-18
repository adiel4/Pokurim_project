from aiogram.fsm.state import StatesGroup, State


class PokurimStates(StatesGroup):
    set_name = State()
    set_age = State()
    set_prefs = State()
    set_lighter = State()
    set_cigars = State()
    idle = State()
    settings = State()
    search = State()
