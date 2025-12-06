from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from ..config import START_GIF 
from ..fsm.states import RegistrationForm
from ..db import queries as db

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
        await message.answer(f"{user.get('name', 'ты')}, уже зарегестрирован!")
        await state.clear()
    else:
        await message.answer("Заполни форму регистрации")
        await message.answer("Выбери себе имя:")
        await state.set_state(RegistrationForm.waiting_for_name)

@common_router.message(Command('cancel'), F.state != None) 
async def handle_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=ReplyKeyboardRemove()
    )
