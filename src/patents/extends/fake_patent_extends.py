from typing import override, Any

from .abc_patent_extends import AbstractPatentExtends


class FakeGooglePatentExtends(AbstractPatentExtends):

    def __init__(self) -> None:
        self._uri = 'fake'

    @override
    def content(self) -> dict[str, Any]:
        return {
            'fake': 'fake'
        }
