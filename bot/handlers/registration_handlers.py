from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..fsm.states import RegistrationForm
from ..keyboards.inline_keyboards import get_gender_keyboard
from ..db import queries as db
from ..config import WOMEN

reg_router = Router()

@reg_router.message(RegistrationForm.waiting_for_name)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        f"Отлично, {message.text}! Теперь скажи какого ты пола:",
        reply_markup=get_gender_keyboard()
    )
    await state.set_state(RegistrationForm.waiting_for_gender)

@reg_router.callback_query(RegistrationForm.waiting_for_gender, F.data.startswith("gender_"))
async def proccess_gender_press(callback: CallbackQuery, state: FSMContext):
    gender_value = "Человек" if callback.data == "gender_male" else "Ж*нщина"
    
    await callback.answer(f"Выбран пол: {gender_value}")
    if gender_value == "Ж*нщина":
        await callback.message.answer_animation(
            animation=WOMEN,
            caption="ААААААААА Ж*НЩИНА"
            )
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.update_data(gender=gender_value)
    
    user_data = await state.get_data()
    user_id = callback.from_user.id 
    user_data["user_id"] = user_id

    if db.add_user(user_data):
        await callback.message.answer(
            "Ура, регистрация завершилась\n"
            f"Имя: {user_data['name']}\n"
            f"Пол: {user_data['gender']}"
        )
    else:
        await callback.message.answer(f"Что-то пошло не так(")
    
    await state.clear()

@reg_router.message(RegistrationForm.waiting_for_gender)
async def proccess_gender_invalid(message: Message):
    await message.answer("Пожалуйста, выбери пол, нажав на одну из кнопок выше. 👆")