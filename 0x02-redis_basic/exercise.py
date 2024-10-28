#!/usr/bin/env python3
""" redis cache """
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ counts the calls to method"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ saves called methods """
    input_keys = f"{method.__qualname__}:inputs"
    output_keys = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args):
        """ wrapper function """
        self._redis.rpush(input_keys, str(args))
        result = method(self, *args)
        self._redis.rpush(output_keys, str(result))

        return result

    return wrapper


class Cache:
    """ a redis cache """
    def __init__(self):
        # Connect to Redis and clear the database
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, int, bytes, None]:
        """ Retrieve data from Redis and apply an transformatiin """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        """ Retrieve data as a string """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """ Retrieve data as an integer """
        return self.get(key, fn=int)


def replay(func):
    """ replays function calls """
    _redis = redis.Redis(host='localhost', port=6379, db=0)
    name = func.__qualname__

    ret_value = _redis.get(f"{name}")
    try:
        ret_value = int(ret_value.decode('utf-8'))
    except Exception:
        ret_value = 0

    inputs = _redis.lrange(f"{name}:inputs", 0, -1)
    outputs = _redis.lrange(f"{name}:outputs", 0, -1)

    print(f"{name} was called {ret_value} times:")
    for inp, output in zip(inputs, outputs):
        try:
            inp = inp.decode('utf-8')
        except Exception:
            input = ""
        try:
            output = output.decode('utf-8')
        except Exception:
            output = ""
        print(f"{name}(*{inp}) -> {output}")
