import os
from abc import ABC

from dotenv import load_dotenv
from multipledispatch import dispatch
from typing_extensions import override

from aspects.cachable import Cachable


class AbstractEnvironment(ABC):
    _force_load: bool

    @Cachable()
    def _load(self):
        if self._force_load:
            load_dotenv()

    def field(self, key: str) -> str:
        self._load()
        return os.getenv(key)


class Environment(AbstractEnvironment):

    @dispatch(bool)
    def __init__(self, force_load: bool):
        self._force_load = force_load

    @dispatch()
    def __init__(self):
        self.__init__(False)


class KeyListPairsEnvironment(AbstractEnvironment):
    """
    The key-value pairs environment when value is a string list.
    """

    @dispatch(str, bool)
    def __init__(self, separator: str, force_load: bool):
        """Primary constructor"""
        self._force_load = force_load
        self._separator = separator

    @dispatch(str)
    def __init__(self, separator: str):
        """Secondary constructor"""
        self.__init__(separator, False)

    @override
    def field(self, key: str) -> list[str]:
        value = super().field(key)
        return value.split(self._separator)
