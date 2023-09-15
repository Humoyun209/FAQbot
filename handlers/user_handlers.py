from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButtonPollType,
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
    print(user_id)
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

    btn_viewed = InlineKeyboardButton(text="Кўрилганлар", callback_data="viewed")
    btn_not_viewed = InlineKeyboardButton(
        text="Кўрилмаганлар", callback_data="not_viewed"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn_viewed, btn_not_viewed]])

    if message.from_user.id == config.admin_id:
        await message.answer(
            text="Админ панелга хуш келибсиз!\n\nСиз томонингиздан кўрилган ёки кўрилмаган мурожаат хатларини танлаш учун қуйидаги тугмалардан бирига босинг",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=f"   Вилоят ҳокимлигида саноат корхоналарини ҳар томонлама қўллаб-қувватлаш, энергия ресурслари билан таъминлаш, маҳсулотлар таннархини пасайтириш, маҳсулот сотиш ва транспорт логистика масалалари билан боғлиқ муаммоларни тезкор ҳал этиш бўйича штаб.\n\nМурожаат учун ракамлар:\n{get_str_numbers()}",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Анкета тўлдириш")]],
                resize_keyboard=True,
            ),
            parse_mode="HTML",
        )


@router.message(Command(commands=["cancel"]), ~StateFilter(default_state))
async def process_cancel_in_machine_state(message: Message, state: FSMContext):
    await message.answer(
        "Малумотлар сақланмади, \nқайтадан тўлдириш учун /start буйруғини юборинг"
    )
    await state.clear()


@router.message(F.text == "Анкета тўлдириш", StateFilter(default_state))
async def start_filling_form(message: Message, state: FSMContext):
    await message.answer(
        text="Яшаш шаҳар(туман)ингзни юборинг\n\nАнкета юборишни тўхтатиш учун /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(FSMFillForm.fill_city)


@router.message(StateFilter(FSMFillForm.fill_city))
async def process_fill_text(message: Message, state: FSMContext):
    await message.answer(
        "Яшаш манзилингизни киритинг\n\n Анкета юборишни тўхтатиш учун /cancel"
    )
    await state.update_data(city=message.text)
    await state.set_state(FSMFillForm.fill_address)


@router.message(StateFilter(FSMFillForm.fill_address))
async def process_fill_text(message: Message, state: FSMContext):
    await message.answer(
        "Корхонангиз номини киритинг\n\n Анкета юборишни тўхтатиш учун /cancel"
    )
    await state.update_data(address=message.text)
    await state.set_state(FSMFillForm.fill_company)


@router.message(StateFilter(FSMFillForm.fill_company))
async def process_fill_text(message: Message, state: FSMContext):
    await message.answer(
        "Фаолият турини киритинг\n\n Анкета юборишни тўхтатиш учун /cancel"
    )
    await state.update_data(company=message.text)
    await state.set_state(FSMFillForm.fill_career)


@router.message(StateFilter(FSMFillForm.fill_career))
async def process_fill_text(message: Message, state: FSMContext):
    await message.answer(
        "СТИР рақамини киритинг\n\n Анкета юборишни тўхтатиш учун /cancel"
    )
    await state.update_data(career=message.text)
    await state.set_state(FSMFillForm.fill_STIR)


@router.message(StateFilter(FSMFillForm.fill_STIR))
async def process_fill_full_name(message: Message, state: FSMContext):
    await message.answer(
        "Исм-шарифингизни киритинг\n\n Анкета юборишни тўхтатиш учун /cancel"
    )
    await state.update_data(stir=message.text)
    await state.set_state(FSMFillForm.fill_full_name)


@router.message(StateFilter(FSMFillForm.fill_full_name), check_name)
async def process_fill_full_name(message: Message, state: FSMContext):
    await message.answer(
        "Мурожаат мазмунини киритинг киритинг\n\n Анкета юборишни тўхтатиш учун /cancel"
    )
    await state.update_data(full_name=message.text)
    await state.set_state(FSMFillForm.fill_text)


@router.message(StateFilter(FSMFillForm.fill_full_name))
async def process_error_fill_full_name(message: Message):
    await message.answer(
        "Исм нотўғри киритилди, \n Илтимос исмингизни қайтадан киритинг\n\nАнкета юборишни тўхтатиш учун /cancel"
    )


@router.message(StateFilter(FSMFillForm.fill_text))
async def process_fill_text(message: Message, state: FSMContext):
    contact_button = KeyboardButton(text="Raqamni yuborish", request_contact=True)
    await message.answer(
        "Телефон рақамингизни юборинг\n\nАнкета юборишни тўхтатиш учун /cancel",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[contact_button]], resize_keyboard=True, one_time_keyboard=True
        ),
    )
    await state.update_data(text=message.text)
    await state.set_state(FSMFillForm.fill_phone)


@router.message(StateFilter(FSMFillForm.fill_phone), F.contact)
async def process_fill_phone(message: Message, state: FSMContext):
    await message.answer(
        "Ижрога масул ташкилотни киритинг\n\nАнкета юборишни тўхтатиш учун /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(FSMFillForm.fill_organization)


@router.message(StateFilter(FSMFillForm.fill_phone))
async def process_error_fill_phone(message: Message):
    await message.answer(
        "Телефон рақами нотўғри киритилди, \n Илтимос телефон рақамингизни қайтадан киритинг\n\nАнкета юборишни тўхтатиш учун /cancel"
    )


@router.message(StateFilter(FSMFillForm.fill_organization))
async def process_fill_text(message: Message, state: FSMContext):
    await state.update_data(organization=message.text)

    user_data = await state.get_data()
    user_data["user_id"] = message.from_user.id

    current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    await message.answer(
        text=f"<b>Мурожаатчи</b>: {user_data['full_name']} \n\n<b>СТИР рақами</b>: {user_data['stir']} \n\n<b>Мурожаат мазмуни</b>: {user_data['text']} \n\n<b>Шаҳар (туман) номи</b>: {user_data['city']} \n\n<b>Яшаш манзили</b>: {user_data['address']} \n\n<b>Корхона номи</b>: {user_data['company']} \n\n<b>Фаолият тури</b>: {user_data['career']}\n\n<b>Тел</b>: {user_data['phone']} \n\n<b>Ижрога масул ташкилот</b>: {user_data['organization']}\n\nЯртилган вақти: {current_date}",
        parse_mode="HTML",
    )
    await message.answer(
        text="Мурожаатингиз учун раҳмат, \nбарча маълумотлар сақланди"
    )
    try:
        BaseManager.insert_data(Statement, **user_data)
    except Exception as e:
        print(e)
    await state.clear()
