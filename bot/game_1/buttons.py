from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_key_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🪨✂️📄'),
        ],
    ],
    resize_keyboard=True,
)

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Меню', callback_data='menu'),
        ],
    ],
)

games = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📄Список игр', callback_data='list_of_games'),
        ],
        [
            InlineKeyboardButton(text='🕹Создать игру', callback_data='start_games'),
        ],
        [
            InlineKeyboardButton(text='🤖Мои игры', callback_data='personal_games'),
        ],
    ],
)


class PaginationGames(CallbackData, prefix='orders'):
    action: str
    page: int
    count_page: int


def many_page_games(name_prev_action: str, name_nex_action: str, page: int = 1, count_page: int = 1):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅️', callback_data=PaginationGames(action=name_prev_action, page=page,
                                                                      count_page=count_page).pack()),
        InlineKeyboardButton(text=f'{page} из {count_page} стр.', callback_data='list games'),
        InlineKeyboardButton(text='➡️', callback_data=PaginationGames(action=name_nex_action, page=page,
                                                                      count_page=count_page).pack()),
        InlineKeyboardButton(text='Назад', callback_data='back_rsp'),
        width=3
    )
    return builder.as_markup()


def many_page_games_without_left(name_nex_action: str, page: int = 1, count_page: int = 1):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='❎', callback_data='❎'),
        InlineKeyboardButton(text=f'{page} из {count_page} стр.', callback_data='list games'),
        InlineKeyboardButton(text='➡️', callback_data=PaginationGames(action=name_nex_action, page=page,
                                                                      count_page=count_page).pack()),
        InlineKeyboardButton(text='Назад', callback_data='back_rsp'),
        width=3
    )
    return builder.as_markup()


def many_page_games_without_right(name_prev_action: str, page: int = 1, count_page: int = 1):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅️', callback_data=PaginationGames(action=name_prev_action, page=page,
                                                                      count_page=count_page).pack()),
        InlineKeyboardButton(text=f'{page} из {count_page} стр.', callback_data='list games'),
        InlineKeyboardButton(text='❎', callback_data='❎'),
        InlineKeyboardButton(text='Назад', callback_data='back_rsp'),
        width=3
    )
    return builder.as_markup()
