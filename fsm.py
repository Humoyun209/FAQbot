from aiogram.fsm.state import StatesGroup, State

class FSMFillForm(StatesGroup):
    fill_city = State()
    fill_address = State()
    fill_company = State()
    fill_career = State()
    fill_STIR = State()
    fill_full_name = State()
    fill_text = State()
    fill_phone = State()
    fill_organization = State()
    