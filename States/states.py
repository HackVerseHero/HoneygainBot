from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    menu = State()
