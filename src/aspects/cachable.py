from functools import wraps
from typing import Callable


class Cachable:
    """
    Cachable is a decorator that calls the decorated function once.

    Usage:
        @Cachable
        def some_method(self): ...
    """
    cache = {}

    def __new__(cls, forever: bool = False) -> Callable:
        """

        :param forever: useless parameter created for illustrate
            how we can parameterize the decorator as a class in the python
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = cls._packed_key(args, kwargs)
                if key not in cls.cache:
                    cls.cache[key] = func(*args, **kwargs)
                return cls.cache[key]

            return wrapper
        return decorator

    @classmethod
    def _packed_key(cls, args, kwargs):
        return args, frozenset(kwargs.items())


if __name__ == '__main__':

    @Cachable(True)
    def mem(a, b) -> int:
        return a ** b

    print(mem(100, 100))
    print(mem(100, 100))
    print(mem(1000, 1000))
    print(mem(1000, 1000))
    print(mem(1000, 1000))
    print(mem(1000, 1000))
