from abc import ABC
from collections import UserDict
from typing import override, Any


class ABCPatent(ABC, UserDict):
    _uri: str

    @override
    def __getitem__(self, item) -> Any:
        return self.data.get(item)

    # TODO: Mutable object is a terrable practice!!!!
    # def __setitem__(self, key, value) -> None:
    #     raise RuntimeError("GooglePatent objects are immutable")
