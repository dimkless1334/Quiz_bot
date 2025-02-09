import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.form import form_router
from handlers.user import user_router
from aiogram.fsm.storage.memory import MemoryStorage 
from database import init_db

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(form_router, user_router)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот отключен!")