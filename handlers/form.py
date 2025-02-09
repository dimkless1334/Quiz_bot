from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.reply import create_cancel_form_keyboard, create_start_quiz_keyboard
from keyboards.inline import create_iline_keyboard

class Form(StatesGroup):
    name = State()
    age = State()
    language = State()

form_router = Router(name="FORM_ROUTER")

@form_router.message(F.text == "Начать опрос")
async def start_quiz(message: Message, state: FSMContext):
    await state.set_data({"history": []})
    await state.set_state(Form.name)
    await message.answer("Опрос начинается.", reply_markup=create_cancel_form_keyboard())
    await message.answer("Как тебя зовут?", reply_markup=create_iline_keyboard(quiz_back=True))


@form_router.callback_query(F.data == "quiz_back")  # Фильтр по callback_data
async def handle_back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])
    
    if not history:
        await callback.answer("Это первый шаг!")
        return
    
    previous_state = history.pop()
    await state.set_data({"history": history})
    await state.set_state(previous_state)
    
    # Возвращаемся к предыдущему вопросу
    if previous_state == Form.name:
        text = "Как тебя зовут?"
    elif previous_state == Form.age:
        text = "Сколько тебе лет?"
    elif previous_state == Form.language:
        text = "Твой любимый язык?"
    
    await callback.message.edit_text(text, reply_markup=create_iline_keyboard(quiz_back=True))
    await callback.answer()  # Убираем "часики" у кнопки

@form_router.message(F.text == "❌ Отменить опрос")
async def cancel_quiz(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос отменен.", reply_markup=create_start_quiz_keyboard())


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])
    history.append(Form.name)  # Сохраняем текущее состояние в историю
    await state.update_data(history=history, name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?", reply_markup=create_iline_keyboard(quiz_back=True))

@form_router.message(Form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!")
        return
    if int(message.text) > 130 and int(message.text) < 0:
        await message.answer("Возраст не может быть больше 150 или меньше 0")
        return
    
    data = await state.get_data()
    history = data.get("history", [])
    history.append(Form.age)  # Сохраняем текущее состояние в историю
    await state.update_data(history=history, age=int(message.text))
    await state.set_state(Form.language)
    await message.answer("Твой любимый язык программирования?",  reply_markup=create_iline_keyboard(quiz_back=True))


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


