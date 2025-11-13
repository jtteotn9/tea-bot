from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_gender_keyboard() -> InlineKeyboardMarkup:
    """Returns gender"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Человек👍", callback_data="gender_male"))
    builder.add(InlineKeyboardButton(text="Ж*нщина👎", callback_data="gender_female"))
    builder.adjust(2)
    return builder.as_markup()

def get_tea_types_keyboard() -> InlineKeyboardMarkup:
    """Returns keyboard select tea type"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Зеленый 🌿", callback_data="tea_type:Зеленый"))
    builder.add(InlineKeyboardButton(text="Красный ☕️", callback_data="tea_type:Красный"))
    builder.add(InlineKeyboardButton(text="Улун 🐲", callback_data="tea_type:Улун"))
    builder.add(InlineKeyboardButton(text="Пуэр 🟫", callback_data="tea_type:Пуэр"))
    builder.add(InlineKeyboardButton(text="Белый 🤍", callback_data="tea_type:Белый"))
    builder.add(InlineKeyboardButton(text="Шен Пуэр🍵", callback_data="tea_type:Шен Пуэр"))
    builder.adjust(3)
    return builder.as_markup()

def get_tea_rating_keyboard() -> InlineKeyboardMarkup:
    """Returns tea mark"""
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.add(InlineKeyboardButton(text=f"⭐️ {i}", callback_data=f"tea_rating:{i}"))
    builder.adjust(5)
    return builder.as_markup()

def get_my_teas_keyboard() -> InlineKeyboardMarkup:
    """Returns check teas mark"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Посмотреть мои чаи 🍵", callback_data="show_my_teas"))
    return builder.as_markup()