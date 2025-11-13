from aiogram.fsm.state import State, StatesGroup

class RegistrationForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_gender = State()

class AddTeaForm(StatesGroup):
    waiting_for_type = State()
    waiting_for_review = State()
    waiting_for_photo = State()
    waiting_for_name = State()
    waiting_for_rating = State()
    waiting_for_price = State()
    waiting_for_location = State()