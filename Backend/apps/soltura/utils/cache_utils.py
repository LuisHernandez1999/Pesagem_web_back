import time
import functools
import hashlib
import json


def memoize_with_ttl(ttl_seconds: int = 300):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(dto):
            key_str = json.dumps(dto.__dict__, sort_keys=True, default=str)
            key_hash = hashlib.sha256(key_str.encode()).hexdigest()
            now = time.time()

            if key_hash in cache:
                value, timestamp = cache[key_hash]
                if now - timestamp < ttl_seconds:
                    return value

            result = func(dto)
            cache[key_hash] = (result, now)
            return result

        return wrapper

    return decorator
