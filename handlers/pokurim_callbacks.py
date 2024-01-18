from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from database import database as db
from bot_states import PokurimStates
from init import database

router = Router()


@router.callback_query(F.data.lower() == 'back')
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    kb = [
        [
            KeyboardButton(text="Поиск"),
            KeyboardButton(text="Настройки")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    await callback_query.message.answer('Можем начинать поиск?', reply_markup=keyboard)
    await state.set_state(PokurimStates.idle)


@router.callback_query(F.data.lower().contains('jig'), PokurimStates.set_lighter)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    match callback_query.data.lower():
        case 'yes_jig':
            await callback_query.message.answer('Подожжешь?')
        case 'no_jig':
            await callback_query.message.answer('А как поджигать?')


@router.callback_query(F.data.lower().contains('sig'), PokurimStates.set_cigars)
async def process_callback_button1(callback_query: CallbackQuery, state: FSMContext):
    match callback_query.data.lower():
        case 'yes_sig':
            await callback_query.message.answer('Значит поделишься?')
        case 'no_sig':
            await callback_query.message.answer('Значит будем стрелять?')
