from contextlib import suppress
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from settings.conf import settings
from aiogram.fsm.context import FSMContext
from . import states, buttons

import re
import requests

router = Router()
base_url = settings.base_url


@router.message(F.text == '/start')
async def start(message: Message):
    first_text = '''
        Привет вас пользователь 👋
Используй меню, чтобы пользоваться ботом.\n
Если оно не появилось, нажми на 🎛 в правом нижнем углу.
        '''

    json_data = {
        'tg_id': message.from_user.id,
        'first_name': message.from_user.first_name or 'bot_firstname',
        'last_name': message.from_user.last_name or 'bot_lastname',
        'username': message.from_user.username or 'bot_username',
    }

    response = requests.post(f'{base_url}/user/check-user/', json={'id': message.from_user.id}).json()
    if not response['status']:
        requests.post(f'{base_url}/user/', json=json_data)
    await message.answer(text=first_text, reply_markup=buttons.start_key_button)


@router.message(F.text == '🪨✂️📄')
async def start_game(message: Message):
    await message.answer(text='игра 🪨✂️📄', reply_markup=buttons.games)


@router.callback_query(F.data == 'list_of_games')
async def list_of_games(callback_query: CallbackQuery):
    response = requests.get(f'{base_url}/games/')

    data = response.json()
    if 0 < data['count'] <= 3:
        text = []
        for result in data['results']:
            text.append(f'''
👤Создатель {result['creator']}
🕹Название игры {result['game_name']} {result['players']}
🤝Присоединится к игре /join_rsp{result['id']}''')
        await callback_query.message.answer(text='\n'.join(text))
    elif data['count'] > 3:
        ...
    elif data['count'] == 0:
        await callback_query.message.answer(text='Еще игры не создано', reply_markup=buttons.games)


@router.callback_query(F.data == 'menu')
async def menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text='игра 🪨✂️📄', reply_markup=buttons.games)


@router.callback_query(F.data == 'start_games')
async def start_games(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(states.GameName.game_name)
    await callback_query.message.answer(text='Напишите название игры:')


@router.message(states.GameName.game_name)
async def create_room(message: Message, state: FSMContext):
    await state.clear()
    json_data = {
        'id': message.from_user.id,
        'game_name': message.text,
    }
    requests.post(f'{base_url}/games/', json=json_data)
    await message.answer(text='игра создалась!', reply_markup=buttons.games)
