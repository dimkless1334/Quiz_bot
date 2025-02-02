from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import create_start_quiz_keyboard

user_router = Router(name="USER_ROUTER")


@user_router.message(F.text == "/start")
async def commandStart(message: Message):
    await message.answer("Привет! Пройди опрос!", reply_markup=create_start_quiz_keyboard())