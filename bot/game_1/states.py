from aiogram.fsm.state import StatesGroup, State


class GameName(StatesGroup):
    game_name = State()
