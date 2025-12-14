from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import START_GIF
from bot.db import queries as db
from bot.fsm.states import RegistrationForm
from bot.keyboards.user_keyboards import get_main_menu_keyboard

common_router = Router()

@common_router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer_animation(
        animation=START_GIF,
        caption="Привет, я бот, который помогает отслеживать разные чаи!"
    )

    user = db.get_user(user_id)

    if user:
        await message.answer(
                f"{user.get('name', 'ты')}, уже зарегестрирован!",
                reply_markup=get_main_menu_keyboard()
                )
        await state.clear()
    else:
        await message.answer("Заполни форму регистрации")
        await message.answer("Выбери себе имя:")
        await state.set_state(RegistrationForm.waiting_for_name)

@common_router.message(Command('/cancel'), F.state != None)
async def handle_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=get_main_menu_keyboard()
    )
