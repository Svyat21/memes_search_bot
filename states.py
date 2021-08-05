from aiogram.dispatcher.filters.state import StatesGroup, State


class DarkState(StatesGroup):
    STATE_OF_REST = State()
    SEARCH_STATE = State()
    DESCRIPTION_STATE = State()
