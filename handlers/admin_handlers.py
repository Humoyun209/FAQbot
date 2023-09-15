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
        await cb.message.answer(text=f"<b>Мурожаатчи</b>: {state.full_name} \n\n<b>СТИР рақами</b>: {state.stir} \n\n<b>Мурожаат мазмуни</b>: {state.text}",
                                parse_mode='HTML')
    if not len(list(data)):
        await cb.message.answer(text="Кўрилган мурожаат хатлари мавжуд эмас")
    await cb.answer()
    

@router.callback_query(F.data == 'not_viewed', check_is_admin)
async def get_only_news(cb: CallbackQuery):
    data = BaseManager.select_data(Statement, is_new=True)
    for state in data:
        await cb.message.answer(text=f"<b>Мурожаатчи</b>: {state.full_name} \n\n<b>СТИР рақами</b>: {state.stir} \n\n<b>Мурожаат мазмуни</b>: {state.text} \n\n<b>Шаҳар (туман) номи</b>: {state.city} \n\n<b>Яшаш манзили</b>: {state.address} \n\n<b>Корхона номи</b>: {state.company}  \n\n<b>Фаолият тури</b>: {state.career} \n\n<b>Тел</b>: {state.phone} \n\n<b>Ижрога масул ташкилот</b>: {state.organization} \n\nЯратилган вакти: {state.created}",
                                parse_mode='HTML', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f'statement_{state.id}')]]))
    if not len(list(data)):
        await cb.message.answer(text="Кўрилмаган мурожаат хатлари мавжуд эмас")
    
    await cb.answer()


@router.callback_query(F.data.regexp("statement_\d+"), check_is_admin)
async def update_statement(cb: CallbackQuery):
    statement_id = int(cb.data[10:])
    try:
        StatementManager.update_one_data(id=statement_id)
    except Exception as e:
        pass
    await cb.answer("Тасдиқланди ✅")
    
    