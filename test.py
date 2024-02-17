import datetime

import redis
from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from geopy.distance import geodesic
import json
import asyncio
from handlers.registration import router
import cache_methods
from init import redis_client
from config_reader import config
import cache_methods as ch_meth
from aiogram.fsm.context import FSMContext
from bot_states import PokurimStates


def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters


async def process_users(redis_cl: redis.Redis, bot: Bot):
    while True:
        all_users_ids = redis_cl.keys()
        for user_id in all_users_ids:
            user_data = cache_methods.get_cached_value(user_id)
            if (not user_data['is_searching']) or \
                    datetime.datetime.strptime(user_data['search_datetime'],
                                               '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now() >= datetime.timedelta(
                minutes=20) or \
                    user_data['message_sent'] > 0:
                continue
            user_data['search_datetime'] = datetime.datetime.strptime(user_data['search_datetime'],
                                                                      '%Y-%m-%d %H:%M:%S.%f')
            user_coords = (user_data['latitude'], user_data['longitude'])
            nearby_user_ids = [other_user_id for other_user_id in all_users_ids
                               if user_id != other_user_id and
                               calculate_distance(user_coords, (
                                   json.loads(redis_cl.get(other_user_id).decode('utf-8'))['latitude'],
                                   json.loads(redis_cl.get(other_user_id).decode('utf-8'))['longitude'])) <= 500]

            if nearby_user_ids:
                closest_user_id = min(nearby_user_ids, key=lambda u: calculate_distance(user_coords,
                                                                                        (json.loads(
                                                                                            redis_cl.get(u).decode(
                                                                                                'utf-8'))['latitude'],
                                                                                         json.loads(
                                                                                             redis_cl.get(u).decode(
                                                                                                 'utf-8'))[
                                                                                             'longitude'])))

                closest_user_coords = (json.loads(redis_cl.get(closest_user_id).decode('utf-8'))['latitude'],
                                       json.loads(redis_cl.get(closest_user_id).decode('utf-8'))['longitude'])
                builder = InlineKeyboardBuilder()
                builder.add(InlineKeyboardButton(
                    text='Да',
                    callback_data='show'
                ))
                builder.add(InlineKeyboardButton(
                    text='Нет',
                    callback_data='dont_show'
                ))
                await bot.send_message(chat_id=user_data['chat_id'], text='Найден новый человек',
                                       reply_markup=builder.as_markup())

                nearby_user_logins = [json.loads(redis_cl.get(uid).decode('utf-8'))['login'] for uid in nearby_user_ids]
                user_data['user_ids'] = str(nearby_user_logins)
                user_data['message_sent'] = 1
                user_data['is_searching'] = False
                ch_meth.set_cached_value(user_data, user_id)
                print(closest_user_coords)
                print(user_data)

        await asyncio.sleep(60)


async def main():
    bot = Bot(config.bot_token.get_secret_value())
    await asyncio.gather(process_users(redis_client, bot))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
