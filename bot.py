import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import postgres_database

from config_reader import config
from handlers import common, registration, pokurim_callbacks
from init import redis_client
from test import process_users


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())
    dp.include_router(common.router)
    dp.include_router(registration.router)
    dp.include_router(pokurim_callbacks.router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        redis_client.flushall()
    except ConnectionError:
        print('Error while connecting to redis')
        exit()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
