from typing import Callable


def only_once(func: Callable) -> Callable:
    attr_name = f'_lazy_{func.__name__}'

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, attr_name):
            result = func(self, *args, **kwargs)
            setattr(self, attr_name, result)
        return getattr(self, attr_name)
    return wrapper
