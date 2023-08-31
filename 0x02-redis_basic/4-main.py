Cache = __import__('exercise').Cache
from exercise import replay

cache = Cache()

cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)


