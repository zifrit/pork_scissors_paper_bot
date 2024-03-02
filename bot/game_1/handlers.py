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


@router.message(F.text == '/start')
async def start(message: Message):
    first_text = '''
        Привет 👋
Используй меню, чтобы пользоваться ботом.\n\n
Если оно не появилось, нажми на 🎛 в правом нижнем углу.'''
    second_text = '''
Чтобы знать обо всех скидках, акциях и обновлениях бота, необходимо подписаться на наш канал  @mediabullet
        '''
    await message.answer(text=first_text)
    await message.answer(text=second_text)
