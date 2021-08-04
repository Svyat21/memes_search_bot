from aiogram.dispatcher.filters.state import StatesGroup, State


class AddMem(StatesGroup):
    STATE_1 = State()
    STATE_2 = State()


class SearchMem(StatesGroup):
    STATE_1 = State()
