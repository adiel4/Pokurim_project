from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from bot_states import PokurimStates
from init import redis_client, main_keyboard

router = Router()


@router.callback_query(F.data.lower() == 'back')
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Можем начинать поиск?', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('jig'), PokurimStates.set_lighter)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    match callback_query.data.lower():
        case 'yes_jig':
            await callback_query.message.answer('Подожжешь?', reply_markup=main_keyboard)
        case 'no_jig':
            await callback_query.message.answer('А как поджигать?', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('sig'), PokurimStates.set_cigars)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    match callback_query.data.lower():
        case 'yes_sig':
            await callback_query.message.answer('Значит поделишься?', reply_markup=main_keyboard)
        case 'no_sig':
            await callback_query.message.answer('Значит будем стрелять?', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower() == 'cancel', PokurimStates.search)
async def cancel_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Поиск отменен', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)
