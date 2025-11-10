import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, ReplyKeyboardRemove, 
    CallbackQuery, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder 
# -------------------------------------
from aiogram.client.default import DefaultBotProperties

from supabase import create_client, Client
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SUPABASE_URL = getenv('SUPABASE_URL')
SUPABASE_KEY = getenv('SUPABASE_KEY')
TOKEN = getenv('TOKEN')
GIF = getenv('GIF')
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logging.info(f"Инициализация прошла успешно")
except Exception as e:
    logging.error(f"Ошибка инициализации Supabase: {e}")
    sys.exit(1)

class RegistrationForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_gender = State()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer_animation(
        animation=GIF,
        caption="Я бот, который помогает отслеживать чаи!"
    )
    try:
        response = supabase.table('users').select('name').eq('user_id', user_id).execute()

        if response.data:
            user_name = response.data[0].get('name', 'пользователь')
            await message.answer(f"А ничо тот факт, что {user_name}, уже зарегестрирован???")
            await state.clear()
        else:
            await message.answer("Оставь надежду всяк входящий и заполни форму регистрации")
            await message.answer("Кто ты?!?!?!??!?!?!:")
            await state.set_state(RegistrationForm.waiting_for_name)
    except Exception as e:
        await message.answer(f"Все сломалось, я обязательно это починю")
        logging.error(f"Ошибка БД при '/start': {e}")

@dp.message(Command('cancel'), F.state != None) 
async def handle_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "ОТБОЙ РЕГИСТРАЦИИ",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(RegistrationForm.waiting_for_name)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Человек",
        callback_data="gender_male"
    ))
    builder.add(InlineKeyboardButton(
        text="Ж*нщина",
        callback_data="gender_female"
    ))
    builder.adjust(2)

    await message.answer(
        f"Отлично, {message.text}! Теперь скажи какого ты пола:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(RegistrationForm.waiting_for_gender)

@dp.callback_query(RegistrationForm.waiting_for_gender, F.data.startswith("gender_"))
async def proccess_gender_press(callback: CallbackQuery, state: FSMContext):
    gender_value = "Человек" if callback.data == "gender_male" else "Ж*нщина"
    
    await callback.answer(f"Выбран пол: {gender_value}")
    
    await callback.message.edit_reply_markup(reply_markup=None)

    await state.update_data(gender=gender_value)
    
    user_data = await state.get_data()
    user_id = callback.from_user.id

    try:
        data_to_insert = {
            "user_id": user_id,
            "name": user_data.get('name'),
            "gender": user_data.get('gender')
        }
        
        supabase.table('users').insert(data_to_insert).execute()

        await callback.message.answer(
            "Ура, ты зарегестрировался\n"
            f"Имя: {user_data['name']}\n"
            f"Пол: {user_data['gender']}"
        )
    except Exception as e:
        await callback.message.answer(f"Что-то пошло не так(")
        logging.error(f"Ошибка: {e}")
    finally:
        await state.clear()

@dp.message(RegistrationForm.waiting_for_gender)
async def proccess_gender_invalid(message: Message):
    await message.answer("Пожалуйста, выбери пол, нажав на одну из кнопок выше. 👆")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())