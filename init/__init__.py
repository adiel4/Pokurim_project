import redis

from database import postgres_database

redis_client = redis.Redis(host='localhost', port='6379', db=0)

database = postgres_database.Database('pokurim_bot', 'postgres', 'adilet321')
database.connect()