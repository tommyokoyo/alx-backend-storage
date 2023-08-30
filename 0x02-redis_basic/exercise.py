#!/usr/bin/env python3
"""
    Cache class
"""
import redis
from typing import Union
from uuid import uuid4


class Cache:
    def __int__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key
