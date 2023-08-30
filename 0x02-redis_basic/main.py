"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis(host='192.168.184.131', port=6379, db=0)
print(local_redis.get(key))
