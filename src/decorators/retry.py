import time
from functools import wraps


def retry(times=3, delay=0, exceptions=(Exception,)):
    """
    Декоратор для повторного выполнения метода при ошибках
    :param times: количество попыток
    :param delay: задержка между попытками (в секундах)
    :param exceptions: кортеж исключений для перехвата
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(func.__name__, e)
                    last_exception = e
                    if attempt < times:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
