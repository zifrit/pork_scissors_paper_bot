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
