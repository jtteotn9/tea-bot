from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Returns main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Добавить чай 🍵"),
                KeyboardButton(text="Мои чаи 📋"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
