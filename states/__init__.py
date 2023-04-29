from aiogram.dispatcher.filters.state import StatesGroup, State


class StartStates(StatesGroup):
    i_lost = State()
    i_found = State()
    number = State()
