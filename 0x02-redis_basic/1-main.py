import redis
Cache = __import__('exercise').Cache

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

local_redis = redis.Redis()

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    print(local_redis.get(key))
    assert cache.get(key, fn=fn) == value
