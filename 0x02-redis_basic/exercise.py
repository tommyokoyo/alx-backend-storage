#!/usr/bin/env python3
"""
    Cache class
"""
import redis
from typing import Union
from uuid import uuid4


class Cache:
    def __init__(self):
        self._redis = redis.Redis(host='192.168.184.131', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key
