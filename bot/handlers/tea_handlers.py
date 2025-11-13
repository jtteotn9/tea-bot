import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..fsm.states import AddTeaForm
from ..keyboards import inline_keyboards as kb
from ..db import queries as db

tea_router = Router()

@tea_router.message(Command("add_tea"))
async def cmd_add_tea(message: Message, state: FSMContext):
    if not db.get_user(message.from_user.id):
        await message.answer("Пожалуйста, сначала зарегистрируйтесь с помощью /start.")
        return

    await message.answer(
        "Отлично! Начинаем добавлять чай.\n\nВыберите тип чая:", 
        reply_markup=kb.get_tea_types_keyboard()
    )
    await state.set_state(AddTeaForm.waiting_for_type)


@tea_router.callback_query(AddTeaForm.waiting_for_type, F.data.startswith("tea_type:"))
async def process_tea_type(callback: CallbackQuery, state: FSMContext):
    tea_type = callback.data.split(":", 1)[1] 
    
    await state.update_data(tea_type=tea_type)
    
    await callback.answer(f"Тип: {tea_type}")
    await callback.message.edit_reply_markup(reply_markup=None)
    
    await callback.message.answer("Теперь, пожалуйста, отправьте фотографию этого чая 📸.")
    await state.set_state(AddTeaForm.waiting_for_photo)


@tea_router.message(AddTeaForm.waiting_for_photo, F.photo)
async def process_tea_photo(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Фото получил! Загружаю в хранилище...")
    
    photo = message.photo[-1]
    
    file_info = await bot.get_file(photo.file_id)
    
    downloaded_file_io = await bot.download_file(file_info.file_path)
    
    file_bytes = downloaded_file_io.read()
    
    file_name = f"user_{message.from_user.id}/{photo.file_id}.jpg"
    
    public_url = db.upload_tea_photo(file_name, file_bytes)

    if public_url:
        await state.update_data(photo_url=public_url)
        await message.answer("Фото загружено! 👍\n\nТеперь введите название чая (например, 'Те Гуань Инь'):")
        await state.set_state(AddTeaForm.waiting_for_name)
    else:
        await message.answer("Ошибка загрузки фото. Попробуйте отправить фото еще раз.")

@tea_router.message(AddTeaForm.waiting_for_photo)
async def process_tea_photo_invalid(message: Message):
     await message.answer("Пожалуйста, отправьте именно фотографию 🖼️. Если передумали, нажмите /cancel.")


@tea_router.message(AddTeaForm.waiting_for_name, F.text)
async def process_tea_name(message: Message, state: FSMContext):
    await state.update_data(tea_name=message.text)
    
    await message.answer(
        "Почти готово.\n\nПоставьте оценку (от 1 до 5):", 
        reply_markup=kb.get_tea_rating_keyboard()
    )
    await state.set_state(AddTeaForm.waiting_for_rating)


@tea_router.callback_query(AddTeaForm.waiting_for_rating, F.data.startswith("tea_rating:"))
async def process_tea_rating(callback: CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(":", 1)[1])
    await state.update_data(rating=rating)
    
    await callback.answer(f"Оценка: {rating} ⭐️")
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    await callback.message.answer("Отлично! Теперь введите цену за 100 грамм (только цифры):")
    await state.set_state(AddTeaForm.waiting_for_price)


@tea_router.message(AddTeaForm.waiting_for_price, F.text)
async def process_tea_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.replace(",", ".")) 
        await state.update_data(price=price)
        
        await message.answer(f"Цена: {price} руб.\n\nИ последний вопрос: где вы купили этот чай?")
        await state.set_state(AddTeaForm.waiting_for_location)
        
    except ValueError:
        await message.answer("Пожалуйста, введите цену только цифрами (например: 350.50 или 400).")

@tea_router.message(AddTeaForm.waiting_for_price)
async def process_tea_price_invalid(message: Message):
     await message.answer("Пожалуйста, введите цену цифрами.")


@tea_router.message(AddTeaForm.waiting_for_location, F.text)
async def process_tea_location(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(location=message.text)
    
    tea_data = await state.get_data()
    user_id = message.from_user.id
    
    data_to_insert = {
        "user_id": user_id,
        "tea_type": tea_data.get("tea_type"),
        "photo_url": tea_data.get("photo_url"),
        "name": tea_data.get("tea_name"),
        "rating": tea_data.get("rating"),
        "price": tea_data.get("price"),
        "purchase_location": tea_data.get("location")
    }

    if db.add_tea_log(data_to_insert):
        confirmation_text = (
            "✅ <b>Чай успешно добавлен!</b>\n\n"
            f"<b>Тип:</b> {tea_data.get('tea_type')}\n"
            f"<b>Название:</b> {tea_data.get('tea_name')}\n"
            f"<b>Оценка:</b> {tea_data.get('rating')} ⭐️\n"
            f"<b>Цена (100г):</b> {tea_data.get('price')} руб.\n"
            f"<b>Место:</b> {tea_data.get('location')}"
        )
        
        await bot.send_photo(
            chat_id=user_id,
            photo=tea_data.get("photo_url"),
            caption=confirmation_text,
            reply_markup=kb.get_my_teas_keyboard()
        )
    else:
        await message.answer("Критическая ошибка сохранения в БД. Попробуйте позже.")
        
    await state.clear()


@tea_router.message(Command("my_teas"))
@tea_router.callback_query(F.data == "show_my_teas")
async def cmd_my_teas(message_or_callback: CallbackQuery, bot: Bot):
    user_id = message_or_callback.from_user.id
    
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.answer("Загружаю твои чаи...")

    teas = db.get_user_teas(user_id)

    if not teas:
        await bot.send_message(user_id, "У тебя пока нет добавленных чаев. Начни с /add_tea ☕️")
        return

    await bot.send_message(user_id, "<b>Вот твои последние 5 чаев:</b>\n")
    
    for tea in teas:
        caption = (
            f"<b>{tea['name']}</b>\n\n"
            f"<b>Тип:</b> {tea['tea_type']}\n"
            f"<b>Оценка:</b> {tea['rating']} ⭐️\n"
            f"<b>Цена (100г):</b> {tea.get('price') or 'Не указана'} руб.\n"
            f"<b>Место:</b> {tea.get('purchase_location') or 'Не указано'}"
        )
        
        try:
            await bot.send_photo(
                chat_id=user_id, 
                photo=tea['photo_url'], 
                caption=caption
            )
        except Exception as e:
            logging.error(f"Не удалось отправить фото чая: {e}")