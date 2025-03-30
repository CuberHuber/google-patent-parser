import time
from functools import wraps
from typing import Callable, Any


class Retry:
    """
    A decorator that retries executing of a function N times with M delay
    """

    def __new__(cls, times=3, delay=0, exceptions=(Exception,)) -> Callable:
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(1, times + 1):
                    try:
                        print("Attempt {}".format(attempt))
                        return func(*args, **kwargs)
                    except exceptions as e:
                        print(func.__name__, e)
                        last_exception = e
                        if attempt < times:
                            time.sleep(delay)
                raise last_exception

            return wrapper

        return decorator


if __name__ == '__main__':
    @Retry(3, 1)
    def mem(a, b) -> int:
        return a ** b


    print(mem(100, 100))
    print(mem(100, '100'))
