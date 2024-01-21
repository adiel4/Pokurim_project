from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot_states import PokurimStates
from init import database, sample_data, main_keyboard
import cache_methods as ch_meth

router = Router()


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    user_name = database.select_data('user_table', columns='username', condition=f'user_id = {message.from_user.id}')
    if len(user_name) < 1:
        data_to_insert = {'user_id': message.from_user.id, 'chat_id': message.chat.id}
        database.insert_data(table='user_table', data=data_to_insert)
        await message.answer(
            text='Добро пожаловать в бота который поможет найти собеседника и вместе покурить.')
        await message.answer(text='Пожалуйста введите имя пользователя.')
        await state.set_state(PokurimStates.set_name)
    else:
        await message.answer(text=f'Добро пожаловать {user_name[0][0]} в бота "Покурим"')
        await message.answer(text='Выберите действие:', reply_markup=main_keyboard)
        await state.set_state(PokurimStates.idle)
        user_data = sample_data
        user_data.update({"prefs": database.select_data('user_table', columns='user_prefs',
                                                        condition=f'user_id = {message.from_user.id}')[0][0]})
        user_data.update({"chat_id": database.select_data('user_table', columns='chat_id',
                                                          condition=f'user_id = {message.from_user.id}')[0][0]})
        print(user_data)
        ch_meth.set_cached_value(user_data, str(message.from_user.id))


@router.message(Command(commands=['help']))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Бот простой. Помочь ничем не могу.')
