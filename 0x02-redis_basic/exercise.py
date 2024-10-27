#!/usr/bin/env python3
""" redis cache """
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    key = f"{method.__qualname__}"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment call count for the given method
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    def __init__(self):
        # Connect to Redis and clear the database
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        # Generate a unique key and store data
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, int, bytes, None]:
        """ Retrieve data from Redis and apply an optional transformation function """
        data = self._redis.get(key)

        if data is None:
            return None

        # Apply transformation function if provided
        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        """ Retrieve data as a string """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """ Retrieve data as an integer """
        return self.get(key, fn=int)

