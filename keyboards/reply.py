from aiogram.utils.keyboard import ReplyKeyboardBuilder



cancel_form_button = {
    "text": "❌ Отменить опрос"
}

start_quiz_button = {
    "text": "Начать опрос"
}

def create_start_quiz_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text=start_quiz_button["text"])

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def create_cancel_form_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text=cancel_form_button["text"])

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)