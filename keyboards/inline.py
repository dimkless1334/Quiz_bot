from aiogram.utils.keyboard import InlineKeyboardBuilder

quiz_back_button = {
    "text": "Назад",
    "callback_data": "quiz_back"
}

def create_iline_keyboard(quiz_back: bool):
    builder = InlineKeyboardBuilder()
    if quiz_back:
        builder.button(text=quiz_back_button["text"], callback_data=quiz_back_button["callback_data"])

    builder.adjust(2)
    return builder.as_markup()