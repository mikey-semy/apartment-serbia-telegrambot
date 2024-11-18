import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {func.__name__!r}: {end_time - start_time} sec")
        return value
    return wrapper_timer