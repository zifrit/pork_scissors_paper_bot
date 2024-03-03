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
    count_page = data['count'] // 3 + 1 if data['count'] % 3 != 0 else data['count'] // 3
    if 0 < data['count'] <= 3:
        text = []
        for result in data['results']:
            text.append(f'''
👤Создатель {result['creator']}
🕹Название игры {result['game_name']} {result['players']}
🤝Присоединится к игре /join_rsp_{result['id']}''')
        await callback_query.message.answer(text='\n'.join(text))

    elif data['count'] > 3:
        text = []
        for result in data['results']:
            text.append(f'''
👤Создатель {result['creator']}
🕹Название игры {result['game_name']} {result['players']}
🤝Присоединится к игре /join_rsp_{result['id']}''')
        await callback_query.message.edit_text(text='\n'.join(text),
                                               reply_markup=buttons.many_page_games_without_left(
                                                   count_page=count_page, name_nex_action='next_page_rsp'))

    elif data['count'] == 0:
        await callback_query.message.answer(text='Еще игры не создано', reply_markup=buttons.menu)


@router.callback_query(buttons.PaginationGames.filter(F.action.in_(['prev_page_rsp', 'next_page_rsp'])))
async def paginator_service(callback_query: CallbackQuery, callback_data: buttons.PaginationGames):
    left = True
    right = True
    if callback_data.action == 'prev_page_rsp':
        if callback_data.page > 1:
            page = callback_data.page - 1
            if page <= 1:
                left = False
                right = True
        else:
            page = callback_data.page
            left = False
            right = True
    elif callback_data.action == 'next_page_rsp':
        if callback_data.page < callback_data.count_page:
            page = callback_data.page + 1
            if page >= callback_data.count_page:
                left = True
                right = False
        else:
            page = callback_data.page
            left = True
            right = False
    response = requests.get(
        f'{base_url}/games/?&page={str(page)}')
    data = response.json()
    count_page = data['count'] // 3 + 1 if data['count'] % 3 != 0 else data['count'] // 3
    text = []
    for result in data['results']:
        text.append(f'''
👤Создатель {result['creator']}
🕹Название игры {result['game_name']} {result['players']}
🤝Присоединится к игре /join_rsp_{result['id']}''')
    with suppress(TelegramBadRequest):
        if right and left:
            await callback_query.message.edit_text(reply_markup=buttons.many_page_games(
                count_page=count_page, page=page, name_prev_action='prev_page_rsp',
                name_nex_action='next_page_rsp'), text='\n'.join(text))
        elif right and not left:
            await callback_query.message.edit_text(reply_markup=buttons.many_page_games_without_left(
                count_page=count_page, page=page, name_nex_action='next_page_rsp'), text='\n'.join(text))
        elif not right and left:
            await callback_query.message.edit_text(reply_markup=buttons.many_page_games_without_right(
                count_page=count_page, page=page, name_prev_action='prev_page_rsp'), text='\n'.join(text))


@router.callback_query(F.data.in_(['menu', 'back_rsp']))
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


@router.message(F.text.startswith('/join_rsp'))
async def join_room_game(message: Message):
    id_room_game = message.text.split('_')[-1]
    response = requests.post(f'{base_url}/games/join/{id_room_game}/', json={'player': message.from_user.id}).json()
    await message.answer(text=response['massages'])


@router.callback_query(F.data == 'personal_games')
async def list_of_games(callback_query: CallbackQuery):
    response = requests.get(f'{base_url}/games/user-games/', json={'id': str(callback_query.from_user.id)})

    data = response.json()
    count_page = data['count'] // 3 + 1 if data['count'] % 3 != 0 else data['count'] // 3
    if 0 < data['count'] <= 3:
        text = []
        for result in data['results']:
            text.append(f'''
🕹Название игры {result['game_name']} {result['players']} /start_rsp_{result['id']}''')
        await callback_query.message.answer(text='\n'.join(text))

    elif data['count'] > 3:
        text = []
        for result in data['results']:
            text.append(f'''
🕹Название игры {result['game_name']} {result['players']} /start_rsp_{result['id']}''')
        await callback_query.message.edit_text(text='\n'.join(text),
                                               reply_markup=buttons.many_page_games_without_left(
                                                   count_page=count_page,
                                                   name_nex_action='next_page_pers_games'
                                               ))

    elif data['count'] == 0:
        await callback_query.message.answer(text='Еще игры не создано', reply_markup=buttons.menu)


@router.callback_query(buttons.PaginationGames.filter(F.action.in_(['prev_page_pers_games', 'next_page_pers_games'])))
async def paginator_service(callback_query: CallbackQuery, callback_data: buttons.PaginationGames):
    left = True
    right = True
    if callback_data.action == 'prev_page_pers_games':
        if callback_data.page > 1:
            page = callback_data.page - 1
            if page <= 1:
                left = False
                right = True
        else:
            page = callback_data.page
            left = False
            right = True
    elif callback_data.action == 'next_page_pers_games':
        if callback_data.page < callback_data.count_page:
            page = callback_data.page + 1
            if page >= callback_data.count_page:
                left = True
                right = False
        else:
            page = callback_data.page
            left = True
            right = False
    response = requests.get(
        f'{base_url}/games/user-games/?&page={str(page)}', json={'id': str(callback_query.from_user.id)})
    data = response.json()
    count_page = data['count'] // 3 + 1 if data['count'] % 3 != 0 else data['count'] // 3
    text = []
    for result in data['results']:
        text.append(f'''
🕹Название игры {result['game_name']} {result['players']} /start_rsp_{result['id']}''')
    with suppress(TelegramBadRequest):
        if right and left:
            await callback_query.message.edit_text(reply_markup=buttons.many_page_games(
                count_page=count_page, page=page, name_nex_action='next_page_pers_games',
                name_prev_action='prev_page_pers_games'), text='\n'.join(text))
        elif right and not left:
            await callback_query.message.edit_text(reply_markup=buttons.many_page_games_without_left(
                count_page=count_page, page=page, name_nex_action='next_page_pers_games'), text='\n'.join(text))
        elif not right and left:
            await callback_query.message.edit_text(reply_markup=buttons.many_page_games_without_right(
                count_page=count_page, page=page, name_prev_action='prev_page_pers_games'), text='\n'.join(text))

