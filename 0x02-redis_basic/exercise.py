#!/usr/bin/env python3
"""
    Cache class
"""
import redis
from typing import Union, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
        decorator for counting how many times
        a function was called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
            wrapper for decorator functionality
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
        Cache class
    """
    def __init__(self):
        """
            initialize
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Stores the input data in redis server
            using a unique identifier
            :param data:
            :return: key
        """
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """
            Reading from redis and recovering data
            :param key:
            :param fn: Callable
            :return: Data
        """
        data = self._redis.get(key)
        if data:
            if fn:
                return fn(data)
            else:
                return data
        else:
            return None

    def get_str(self, key: str) -> Union[str, None]:
        """
            parametize a value from redis to str
            :param key:
            :return:
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
            parametize a value from redis to str
            :param key:
            :return:
        """
        return self.get(key, fn=int)
