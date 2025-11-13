import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from .config import TOKEN

from .handlers.common_handlers import common_router
from .handlers.registration_handlers import reg_router
from .handlers.tea_handlers import tea_router

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    storage = MemoryStorage() 
    dp = Dispatcher(storage=storage)
    
    dp.include_router(common_router)
    dp.include_router(reg_router)
    dp.include_router(tea_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())