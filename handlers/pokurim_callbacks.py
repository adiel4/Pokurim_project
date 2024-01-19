from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, ReplyKeyboardRemove
import cache_methods as ch_meth
from bot_states import PokurimStates
from init import redis_client, main_keyboard

router = Router()


@router.callback_query(F.data.lower() == 'back')
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Можем начинать поиск?', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('jig'), PokurimStates.set_lighter)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    user_data = ch_meth.get_cached_value(str(callback_query.from_user.id))
    lighter = user_data.get("lighter")
    match callback_query.data.lower():
        case 'yes_jig':
            await callback_query.message.answer('Подожжешь?', reply_markup=main_keyboard)
        case 'no_jig':
            await callback_query.message.answer('А как поджигать?', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('sig'), PokurimStates.set_cigars)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    user_data = ch_meth.get_cached_value(str(callback_query.from_user.id))
    cigars = user_data.get("cigarretes")
    match callback_query.data.lower():
        case 'yes_sig':
            await callback_query.message.answer('Значит поделишься?', reply_markup=main_keyboard)
            user_data.update('cigarretes', True)
            ch_meth.set_cached_value(callback_query.from_user.id, user_data)
        case 'no_sig':
            await callback_query.message.answer('Значит будем стрелять?', reply_markup=main_keyboard)
            user_data.update('cigarretes', False)
            ch_meth.set_cached_value(callback_query.from_user.id, user_data)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('prefs'), PokurimStates.idle)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    match callback_query.data.lower():
        case 'yes_prefs':
            await callback_query.message.answer('Введите ваши предпочтения', reply_markup=ReplyKeyboardRemove())
            await state.set_state(PokurimStates.set_prefs)
        case 'no_prefs':
            await callback_query.message.answer('Возвращаемся обратно', reply_markup=main_keyboard)
            await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower() == 'cancel', PokurimStates.search)
async def cancel_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Поиск отменен', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)
