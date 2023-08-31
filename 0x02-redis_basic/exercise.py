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


def call_history(method: Callable) -> Callable:
    """
        decorator that stores the history of input and
        outputs of a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
            wrapper for decorator functionality
        """
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    """
        Displays the history of a function calls
        :param method:
        :return:
    """
    input_key = f'{method.__qualname__}:inputs'
    output_key = f'{method.__qualname__}:outputs'
    redis_instance = redis.Redis()

    number_of_calls = redis_instance.get(method.__qualname__)
    input_history = redis_instance.lrange(input_key, 0, -1)
    output_history = redis_instance.lrange(output_key, 0, -1)

    print('Cache.store was called {} times:'.format(
        number_of_calls.decode('utf-8')))
    for input_data, output_data in zip(input_history, output_history):
        print(f"{method.__qualname__}"
              f"(*{input_data.decode('utf-8')}) -> "
              f"{output_data.decode('utf-8')}")


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

    @call_history
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

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
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
