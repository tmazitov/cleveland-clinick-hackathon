from aiogram.fsm.state import StatesGroup, State

class UserState(StatesGroup):
    symptoms = State()
    user_current = State()