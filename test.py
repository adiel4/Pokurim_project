import redis
from aiogram import Bot
from geopy.distance import geodesic
import json
import asyncio
from handlers.registration import router
import cache_methods
from init import redis_client


def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters


async def process_users(redis_client: redis.Redis, bot: Bot):
    while True:
        all_users_ids = redis_client.keys()

        for user_id in all_users_ids:
            user_data = cache_methods.get_cached_value(user_id)
            user_coords = (user_data['latitude'], user_data['longitude'])
            nearby_user_ids = [other_user_id for other_user_id in all_users_ids
                               if user_id != other_user_id and
                               calculate_distance(user_coords, (
                                   json.loads(redis_client.get(other_user_id).decode('utf-8'))['latitude'],
                                   json.loads(redis_client.get(other_user_id).decode('utf-8'))['longitude'])) <= 500]

            if nearby_user_ids:
                # Выбор пользователя, который ближе ко всем остальным
                closest_user_id = min(nearby_user_ids, key=lambda u: calculate_distance(user_coords,
                                                                                        (json.loads(
                                                                                            redis_client.get(u).decode(
                                                                                                'utf-8'))['latitude'],
                                                                                         json.loads(
                                                                                             redis_client.get(u).decode(
                                                                                                 'utf-8'))[
                                                                                             'longitude'])))

                closest_user_coords = (json.loads(redis_client.get(closest_user_id).decode('utf-8'))['latitude'],
                                       json.loads(redis_client.get(closest_user_id).decode('utf-8'))['longitude'])

                # Отправка сообщения в Telegram

                print(closest_user_coords)
                # Здесь можно добавить дополнительные действия, например, обновление информации в Redis

        # Пауза перед следующей итерацией
        await asyncio.sleep(60)
