from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.types import Message
from config import load_data
from database import Statement, Users
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from filters import check_name, get_str_numbers

from models.managers import BaseManager
from fsm import FSMFillForm


router: Router = Router()


@router.message(Command(commands=["start"]), StateFilter(default_state))
async def process_start(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    config = load_data()
    try:
        BaseManager.insert_data(
            Users,
            **{
                "id": user_id,
                "username": username,
                "is_admin": True if message.from_user.id == config.admin_id else False,
            },
        )
    except Exception as e:
        pass

    btn_viewed = InlineKeyboardButton(text="Ko'rilganlar", callback_data="viewed")
    btn_not_viewed = InlineKeyboardButton(
        text="Ko'rilmaganlar", callback_data="not_viewed"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn_viewed, btn_not_viewed]])

    if message.from_user.id == config.admin_id:
        await message.answer(
            text="Admin panelga xush kelibsiz!\n\nSiz tomoningizdan ko'rilgan yoki ko'rilmagan murojaat xatlarini tanlash uchun quyidagi tugmalardan biriga bosing",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=f'Assalomu aleykum,\nBuxoro hokimligi murojaat botiga xush kelibsiz!!!\nMurojaat xati yuborish uchun "Anketa to\'ldirish" tugmasiga bosing\n\nMurojaat uchun raqamlar: {get_str_numbers()}',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Anketa to'ldirish")]],
                resize_keyboard=True,
            ),
            parse_mode='HTML'
        )


@router.message(Command(commands=["cancel"]), ~StateFilter(default_state))
async def process_cancel_in_machine_state(message: Message, state: FSMContext):
    await message.answer(
        "Malumotlar saqlanmadi, \nqaytadan to'dirish uchun /start buyrug'ini yuboring"
    )
    await state.clear()


@router.message(F.text == "Anketa to'ldirish", StateFilter(default_state))
async def start_filling_form(message: Message, state: FSMContext):
    await message.answer(
        text="Iltimos, yashash shahar(tuman)ingzni yuboring\n\n Anketa yuborishni to'xtatish uchun /cancel",
    )
    await state.set_state(FSMFillForm.fill_city)


@router.message(StateFilter(FSMFillForm.fill_city))
async def process_fill_text(message: Message, state: FSMContext):
    await message.answer("Barakalla, \niltimos, yashash manzilingizni kiriting")
    await state.update_data(city=message.text)
    await state.set_state(FSMFillForm.fill_address)


@router.message(StateFilter(FSMFillForm.fill_address))
async def process_fill_text(message: Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    await message.answer("Barakalla, \n iltimos, korxonangiz nomini kiriting")
    await state.update_data(address=message.text)
    await state.set_state(FSMFillForm.fill_company)


@router.message(StateFilter(FSMFillForm.fill_company))
async def process_fill_text(message: Message, state: FSMContext):
    await message.answer("Faoliyat turini kiriting: ")
    await state.update_data(company=message.text)
    await state.set_state(FSMFillForm.fill_career)


@router.message(StateFilter(FSMFillForm.fill_career))
async def process_fill_text(message: Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    await message.answer("STIR raqamini kiriting")
    await state.update_data(career=message.text)
    await state.set_state(FSMFillForm.fill_STIR)


@router.message(StateFilter(FSMFillForm.fill_STIR))
async def process_fill_full_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    await message.answer("Barakalla, \n iltimos, ism-sharifingizni kiriting")
    await state.update_data(stir=message.text)
    await state.set_state(FSMFillForm.fill_full_name)


@router.message(StateFilter(FSMFillForm.fill_full_name), check_name)
async def process_fill_full_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    await message.answer("iltimos, murojaat mazmunini kiriting kiriting")
    await state.update_data(full_name=message.text)
    await state.set_state(FSMFillForm.fill_text)


@router.message(StateFilter(FSMFillForm.fill_full_name))
async def process_error_fill_full_name(message: Message):
    await message.answer(
        "Ism notog'ri kiritildi, \n Iltimos ismingizni qaytadan kiriting\n\nAnketa yuborishni to'xtatish uchun /cancel"
    )


@router.message(StateFilter(FSMFillForm.fill_text))
async def process_fill_text(message: Message, state: FSMContext):
    contact_button = KeyboardButton(text="Raqamni yuborish", request_contact=True)
    await message.answer(
        "Barakalla, \niltimos, telefon raqamingizni yuboring",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[contact_button]], resize_keyboard=True, one_time_keyboard=True
        ),
    )
    await state.update_data(text=message.text)
    await state.set_state(FSMFillForm.fill_phone)


@router.message(StateFilter(FSMFillForm.fill_phone), F.contact)
async def process_fill_phone(message: Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    await message.answer(
        "Barakalla, \niltimos, ijroga masul tashkilotni kiriting\n\nAnketa yuborishni to'xtatish uchun /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(FSMFillForm.fill_organization)


@router.message(StateFilter(FSMFillForm.fill_phone))
async def process_error_fill_phone(message: Message):
    await message.answer(
        "Telefon raqami noto'g'ri kiritildi, \n Iltimos telefon raqamingizni qaytadan kiriting. \n\nAnketa yuborishni to'xtatish uchun /cancel"
    )


@router.message(StateFilter(FSMFillForm.fill_organization))
async def process_fill_text(message: Message, state: FSMContext):
    await state.update_data(organization=message.text)

    user_data = await state.get_data()
    print(user_data)
    user_data["user_id"] = message.from_user.id

    current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    await message.answer(
        text=f"<b>Murojaatchi</b>: {user_data['full_name']} \n\n<b>STIR raqami</b>: {user_data['stir']} \n\n<b>Murojaat mazmuni</b>: {user_data['text']} \n\n<b>Shahar (tuman) nomi</b>: {user_data['city']} \n\n<b>Manzil MFY, qishloq, ko'cha</b>: {user_data['address']} \n\n<b>Korxona nomi</b>: {user_data['company']} \n\n<b>Faoliyat turi</b>: {user_data['career']}\n\n<b>Tel</b>: {user_data['phone']} \n\n<b>Ijroga masul tashkilot</b>: {user_data['organization']}\n\nYartilgan vaqti: {current_date}",
        parse_mode="HTML",
    )
    await message.answer(
        text="Murojaatingiz uchun rahmat, \n barcha ma'lumotlar saqlandi"
    )
    try:
        BaseManager.insert_data(Statement, **user_data)
    except Exception as e:
        print(e)
    await state.clear()

# @router.message()
# async def ech0_message(message: Message):
#     await message.answer("Echo message working....")