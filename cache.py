import time

_cache = {}

def get_cached(key: str, ttl: int = 300):
    entry = _cache.get(key)
    if entry and time.time() - entry["ts"] < ttl:
        return entry["data"]
    return None

def set_cached(key: str, data):
    _cache[key] = {"data": data, "ts": time.time()}