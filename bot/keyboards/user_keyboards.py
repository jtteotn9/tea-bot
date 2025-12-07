from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Returns main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/add_tea"),
                KeyboardButton(text="Мои чаи 📋"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
