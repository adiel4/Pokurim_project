from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot_states import PokurimStates
from init import database

router = Router()


@router.message(
    PokurimStates.set_name
)
async def set_user_name(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer(text='ИМЯ ПИШЕТСЯ ТЕКСТОМ')
        return None
    else:
        if message.text.lower() == 'адель':
            await message.reply('Добро пожаловать падаван')
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
        await message.answer(text='Тебя просят возраст указать а не файл скидывать.')
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

        kb = [
            [
                KeyboardButton(text="Поиск"),
                KeyboardButton(text="Настройки")
            ],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
        await message.answer(text='Выберите действие:', reply_markup=keyboard)
        await state.set_state(PokurimStates.idle)


@router.message(
    PokurimStates.idle
)
async def ans_idle(message: Message, state: FSMContext):
    match message.text.lower():
        case 'настройки':
            kb = [
                [
                    KeyboardButton(text="Предпочтения"),
                    KeyboardButton(text="Есть зажигалка?"),
                    KeyboardButton(text="Есть сиги?")
                ],
            ]
            keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
            await message.answer('Давайте менять настройки', reply_markup=keyboard)
        case 'поиск':
            kb = [
                [
                    KeyboardButton(text="Отмена"),
                ],
            ]
            keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
            await message.answer('Поехали искать', reply_markup=keyboard)
        case 'отмена':
            kb = [
                [
                    KeyboardButton(text="Поиск"),
                    KeyboardButton(text="Настройки")
                ],
            ]
            keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
            await message.answer('Поиск отменен', reply_markup=keyboard)
            await state.set_state(PokurimStates.idle)
        case _:
            await message.reply('Бот в разработке просим чуточку подождать')