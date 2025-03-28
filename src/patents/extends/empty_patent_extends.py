from typing import override, Any

from .abc_patent_extends import ABCPatentExtends


class EmptyGooglePatentExtends(ABCPatentExtends):

    def __init__(self) -> None:
        self._uri = ''

    @override
    def content(self) -> dict[str, Any]:
        return {}
