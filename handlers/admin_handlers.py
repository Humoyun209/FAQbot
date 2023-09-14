from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from config import load_data
from database import Statement
from models.managers import BaseManager, StatementManager

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


router: Router = Router()
config: Bot = load_data()

check_is_admin = lambda message: message.from_user.id == config.admin_id


@router.callback_query(F.data == 'viewed', check_is_admin)
async def get_only_news(cb: CallbackQuery):
    data = BaseManager.select_data(Statement, is_new=False)
    for state in data:
        await cb.message.answer(text=f"<b>Murojaatchi</b>: {state.full_name} \n\n<b>STIR raqami</b>: {state.stir} \n\n<b>Murojaat mazmuni</b>: {state.text}",
                                parse_mode='HTML')
    if not len(list(data)):
        await cb.message.answer(text="Ko'rilgan murojaat xatlari mavjud emas")
    await cb.answer()
    

@router.callback_query(F.data == 'not_viewed', check_is_admin)
async def get_only_news(cb: CallbackQuery):
    data = BaseManager.select_data(Statement, is_new=True)
    for state in data:
        await cb.message.answer(text=f"<b>Murojaatchi</b>: {state.full_name} \n\n<b>STIR raqami</b>: {state.stir} \n\n<b>Murojaat mazmuni</b>: {state.text} \n\n<b>Shahar (tuman)</b>: {state.city} \n\n<b>Manzili MFY, ko'cha</b>: {state.address} \n\n<b>Korxona nomi</b>: {state.company}  \n\n<b>Faoliyat turi</b>: {state.career} \n\n<b>Tel</b>: {state.phone} \n\n<b>Ijroga masul tashkilot</b>: {state.organization} \n\nYaratilgan vaqti: {state.created}",
                                parse_mode='HTML', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f'statement_{state.id}')]]))
    if not len(list(data)):
        await cb.message.answer(text="Ko'rilmagan murojaat xatlari mavjud emas")
    
    await cb.answer()


@router.callback_query(F.data.regexp("statement_\d+"), check_is_admin)
async def update_statement(cb: CallbackQuery):
    statement_id = int(cb.data[10:])
    try:
        StatementManager.update_one_data(id=statement_id)
    except Exception as e:
        pass
    await cb.answer("Tasdiqlandi ✅")
    
    