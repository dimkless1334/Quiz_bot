from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.reply import create_cancel_form_keyboard, create_start_quiz_keyboard

class Form(StatesGroup):
    name = State()
    age = State()
    language = State()

form_router = Router(name="FORM_ROUTER")

@form_router.message(F.text == "Начать опрос")
async def start_quiz(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Как тебя зовут?", reply_markup=create_cancel_form_keyboard())


@form_router.message(F.text == "❌ Отменить опрос")
async def cancel_quiz(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос отменен.", reply_markup=create_start_quiz_keyboard())


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")

@form_router.message(Form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!")
        return
    if int(message.text) > 130 and int(message.text) < 0:
        await message.answer("Возраст не может быть больше 150 или меньше 0")
        return
    
    await state.update_data(age=int(message.text))
    await state.set_state(Form.language)
    await message.answer("Твой любимый язык программирования?")


@form_router.message(Form.language)
async def process_language(message: Message, state: FSMContext):
    await state.update_data(language=message.text)
    data = await state.get_data()
    await message.answer(
        "📝 Ваши ответы:\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Язык: {data["language"]}",
        reply_markup=create_start_quiz_keyboard()
    )
    await state.clear()

@form_router.message(F.text == "❌ Отменить опрос")
async def cancel_quiz(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос отменен.", reply_markup=create_start_quiz_keyboard())