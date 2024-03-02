import asyncio
import logging

from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from settings.conf import settings
from aiogram import Bot, Dispatcher
from bot.game_1.handlers import router as game_1_rout


async def main():
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        game_1_rout
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
