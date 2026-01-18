from aiogram.fsm.state import State, StatesGroup


class MenuSG(StatesGroup):
    start = State()
    description = State()


class AdminMenuSG(StatesGroup):
    start = State()
    price = State()
    price_set = State()
