import ast

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
    match callback_query.data.lower():
        case 'yes_jig':
            user_data['lighter'] = True
        case 'no_jig':
            user_data['lighter'] = False
    ch_meth.set_cached_value(user_data, str(callback_query.from_user.id))
    await callback_query.message.answer('Настройки сохранены. Можем начинать поиск?', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('sig'), PokurimStates.set_cigars)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    user_data = ch_meth.get_cached_value(str(callback_query.from_user.id))
    match callback_query.data.lower():
        case 'yes_sig':
            user_data['cigarettes'] = True
        case 'no_sig':
            user_data['cigarettes'] = False
    ch_meth.set_cached_value(user_data, str(callback_query.from_user.id))
    await callback_query.message.answer('Настройки сохранены. Можем начинать поиск?', reply_markup=main_keyboard)
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
    user_data = ch_meth.get_cached_value(str(callback.from_user.id))
    user_data['is_searching'] = False
    ch_meth.set_cached_value(user_data, str(callback.from_user.id))
    print(user_data)
    await callback.message.answer('Поиск отменен', reply_markup=main_keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('show'), PokurimStates.search)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    user_data = ch_meth.get_cached_value(str(callback_query.from_user.id))
    my_list = ast.literal_eval(user_data['user_ids'])
    match callback_query.data.lower():
        case 'show':
            for ids in my_list:
                await callback_query.message.answer(text=f'Найден пользователь: @{ids}')
            await callback_query.message.answer('Поиск прерван, вы в главном меню.', reply_markup=main_keyboard)
            await state.set_state(PokurimStates.idle)
            pass
        case 'dont_show':
            await callback_query.message.answer('Поиск прерван, вы в главном меню.', reply_markup=main_keyboard)
            await state.set_state(PokurimStates.idle)
            pass
        case _:
            pass
