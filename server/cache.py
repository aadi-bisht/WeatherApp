import time

cache = {}

def get(key):
    entry = cache.get(key)
    if entry:
        value, timestamp = entry
        if time.time() - timestamp < 300:
            print('Returned from cache')
            return value
    return None

def set(key, value):
    cache[key] = (value, time.time())

