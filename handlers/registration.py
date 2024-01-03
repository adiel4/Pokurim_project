from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_states import PokurimStates
from database import postgres_database

router = Router()

database = postgres_database.Database('pokurim_bot', 'postgres', 'adilet321')
database.connect()


@router.message(
    PokurimStates.set_name
)
async def set_user_name(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer(text='ИМЯ ПИШЕТСЯ ТЕКСТОМ')
        return None
    else:
        await message.reply('Имя пользователя сохранено')
        await message.answer(text='Введите ваш возраст.')
        update_cond = f"user_id = {message.from_user.id}"
        data_to_update = {"username": message.text}
        database.update_data('user_table', data_to_update, update_cond)
        await state.set_state(PokurimStates.set_age)


@router.message(
    PokurimStates.set_age
)
async def set_user_age(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer(text='Тебя просят возраст указать а не файл скидвать.')
        return None
    else:
        try:
            age = int(message.text)
        except:
            await message.answer(text='Писать желательно цифрами')
            return None
        else:
            if 17 < age < 99:
                await message.answer(text='Ваш возраст сохранен')
                await message.answer(text='Прошу кратко описать свои предпочтения')
                update_cond = f"user_id = {message.from_user.id}"
                data_to_update = {"user_age": message.text}
                database.update_data('user_table', data_to_update, update_cond)
                await state.set_state(PokurimStates.set_prefs)
            else:
                await message.answer(text='Про возраст пиздеть не надо')
                return None


@router.message(
    PokurimStates.set_prefs
)
async def set_user_prefs(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer(text='Пожалуйста опишите свои предпочтения')
        return None
    else:
        await message.reply('Ваши пожелания сохранены. Добро пожаловать в бот "Покурим"')
        update_cond = f"user_id = {message.from_user.id}"
        data_to_update = {"user_prefs": message.text}
        database.update_data('user_table', data_to_update, update_cond)
        await state.set_state(PokurimStates.set_prefs)
        await state.set_state(PokurimStates.idle)
