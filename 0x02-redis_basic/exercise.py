#!/usr/bin/env python3
""" redis cache """
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)
    -> Union[str, int, bytes, None]:
        """ converts data to desired format """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        """ converts to string"""
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key:str) -> Optional[int]:
        """ converts to int """
        return self.get(key, fn=int)
