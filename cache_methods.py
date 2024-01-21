import datetime
import json
from datetime import timedelta
from init import redis_client
import decimal


def get_cached_value(name):
    value_str = redis_client.get(name)
    if not value_str:
        return None
    value_arr = json.loads(value_str)
    return value_arr


def set_cached_value(value_arr, name: str):
    value_str = json.dumps(value_arr, default=decimal_encoder)
    name = name.decode('utf-8') if isinstance(name, bytes) else name
    print("Setting key:", name)
    redis_client.set(name, value_str)
    return value_arr


def delete_cached_value(key):
    try:
        redis_client.delete(key)
        return 1
    except:
        return 0


def set_cached_value_by_days(value_arr, name: str, expire_days: int):
    value_str = json.dumps(value_arr, default=decimal_encoder)
    redis_client.set(name, value_str)
    redis_client.expire(name, timedelta(days=expire_days))
    return value_arr


def set_cached_value_by_minutes(value_arr, name: str, expire_minutes: int):
    value_str = json.dumps(value_arr, default=decimal_encoder)
    redis_client.set(name, value_str, ex=timedelta(minutes=expire_minutes))
    return value_arr


def decimal_encoder(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)  # Convert Decimal to string representation
    elif isinstance(obj, datetime.date):
        return str(obj)
    elif isinstance(obj, datetime.datetime):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable.{obj}")
