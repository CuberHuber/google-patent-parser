from abc import ABC, abstractmethod
from typing import Any


class AbstractPatentExtends(ABC):
    _uri: str

    def __dict__(self) -> dict:
        return self.content()

    def __getitem__(self, item: str) -> Any:
        return self.content().get(item)

    @abstractmethod
    def content(self) -> dict[str, Any]:
        raise NotImplementedError()
