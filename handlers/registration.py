import datetime

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import cache_methods as ch_meth
from bot_states import PokurimStates
from init import database, redis_client, main_keyboard, sample_data

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
        try:
            database.update_data('user_table', data_to_update, update_cond)
        except:
            await message.reply('Возникла ошибка попробуйте снова.')
            return None
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
                try:
                    database.update_data('user_table', data_to_update, update_cond)
                except:
                    await message.reply('Возникла ошибка попробуйте снова.')
                    return None
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
        await message.reply('Ваши пожелания сохранены.')
        update_cond = f"user_id = {message.from_user.id}"
        data_to_update = {"user_prefs": message.text}
        try:
            database.update_data('user_table', data_to_update, update_cond)
        except:
            await message.reply('Возникла ошибка попробуйте снова.')
            return None
        user_data = sample_data
        user_data["prefs"] = message.text
        user_data['login'] = message.from_user.username
        ch_meth.set_cached_value(user_data, str(message.from_user.id))

        await message.answer(text='Выберите действие:', reply_markup=main_keyboard)
        await state.set_state(PokurimStates.idle)


@router.message(
    PokurimStates.idle
)
async def ans_idle(message: Message, state: FSMContext):
    user_data = ch_meth.get_cached_value(str(message.from_user.id))
    match message.text.lower():
        case 'настройки':
            kb = [
                [
                    KeyboardButton(text="Предпочтения"),
                    KeyboardButton(text="Есть зажигалка?"),

                ], [
                    KeyboardButton(text="Есть сиги?"),
                    KeyboardButton(text="Назад")
                ]
            ]
            keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
            await message.answer('Давайте менять настройки', reply_markup=keyboard)
        case 'есть сиги?':
            cigars = user_data.get("cigarettes")
            await message.answer('У вас ' + ("есть сигареты" if cigars else "нет сигарет"),
                                 reply_markup=ReplyKeyboardRemove())
            await state.set_state(PokurimStates.set_cigars)
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(
                text='Да',
                callback_data='yes_sig'
            ))
            builder.add(InlineKeyboardButton(
                text='Нет',
                callback_data='no_sig'
            ))
            builder.add(InlineKeyboardButton(
                text='Назад',
                callback_data='back'
            ))
            await message.answer('Есть сиги?', reply_markup=builder.as_markup())
        case 'есть зажигалка?':
            lighter = user_data.get('lighter')
            await message.answer('У вас ' + ("есть зажигалка" if lighter else "нет зажигалки"),
                                 reply_markup=ReplyKeyboardRemove())
            await state.set_state(PokurimStates.set_lighter)
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(
                text='Да',
                callback_data='yes_jig'
            ))
            builder.add(InlineKeyboardButton(
                text='Нет',
                callback_data='no_jig'
            ))
            builder.add(InlineKeyboardButton(
                text='Назад',
                callback_data='back'
            ))
            await message.answer('Есть зажигалка?', reply_markup=builder.as_markup())
        case 'назад':
            await message.answer('Можем начинать поиск?', reply_markup=main_keyboard)
        case 'поиск':
            kb = [
                [
                    KeyboardButton(text="Передать", request_location=True)],
                [KeyboardButton(text="Не передавать")
                 ],
            ]
            keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
            await message.answer('Передать?', reply_markup=keyboard)
            await state.set_state(PokurimStates.set_coords)
        case 'отмена':
            await message.answer('Поиск отменен', reply_markup=main_keyboard)
            await state.set_state(PokurimStates.idle)
        case 'предпочтения':
            user_prefs = database.select_data('user_table', columns='user_prefs',
                                              condition=f'user_id = {message.from_user.id}')
            await message.reply(f"Ваши предпочтения: {user_prefs[0][0]}")
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(
                text='Да',
                callback_data='yes_prefs'
            ))
            builder.add(InlineKeyboardButton(
                text='Нет',
                callback_data='no_prefs'
            ))
            builder.add(InlineKeyboardButton(
                text='Назад',
                callback_data='back'
            ))
            await message.answer('Хотите поменять свои предпочтения?', reply_markup=builder.as_markup())
        case _:
            await message.reply('Бот в разработке просим чуточку подождать')


@router.message(
    PokurimStates.set_coords
)
async def set_coords(message: Message, state: FSMContext):
    user_data = ch_meth.get_cached_value(str(message.from_user.id))
    if message.content_type == ContentType.LOCATION:
        await message.answer('Геопозиция получена', reply_markup=ReplyKeyboardRemove())
        latitude = message.location.latitude
        longitude = message.location.longitude
        user_data['latitude'] = latitude
        user_data['longitude'] = longitude
        user_data['is_searching'] = True
        user_data['search_datetime'] = datetime.datetime.now()
        ch_meth.set_cached_value(user_data, str(message.from_user.id))
        await message.delete()
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        ))
        await message.answer('Начинаем поиск..', reply_markup=builder.as_markup())
        await state.set_state(PokurimStates.search)
        print(user_data)
    elif message.text.lower() == 'не передавать':
        await message.answer('Поиск отменен', reply_markup=main_keyboard)
        await state.set_state(PokurimStates.idle)
