from multipledispatch import dispatch

from .abc_patent import AbstractPatent
from .extends.abc_patent_extends import AbstractPatentExtends
from .extends.empty_patent_extends import EmptyGooglePatentExtends


class GooglePatent(AbstractPatent):
    """

    ---
    :Example:

    # row is a dict with fields
    row = {'uri': 'https://patents.google.com/patent/US11984124B2/en'}

    # Simple use
    gp = GooglePatent(row.get('uri'))
    print(gp)

    # strict uri and row params
    gp2 = GooglePatent(row.get('uri'), row)
    print(gp2)

    # full primary constructor used with extends
    gp3 = GooglePatent(row.get('uri'), row, GooglePatentExtends(row.get('uri')))
    print(gp3)

    # This example shows how to retrieve a patent with extended fields.
    wg3 = gp3.with_extends()
    d_wg3 = dict(wg3)
    print(d_wg3)

    """

    @dispatch(str, dict, AbstractPatentExtends)
    def __init__(self, uri: str, row: dict, extends: AbstractPatentExtends):
        # primary constructor
        assert row.get("uri") is not None and row.get("uri") == uri
        super().__init__(row)
        self._extends = extends
        self._uri = uri

    @dispatch(str, dict)
    def __init__(self, uri: str, row: dict):
        # secondary constructor call prima
        if row.get("uri") != uri:
            row['uri'] = uri

        self.__init__(uri, row, EmptyGooglePatentExtends())

    @dispatch(str)
    def __init__(self, uri: str):
        # secondary constructor
        self.__init__(uri, {'uri': uri}, EmptyGooglePatentExtends())

    def with_extends(self) -> AbstractPatent:
        return GooglePatent(
            self._uri,
            {**self.data, **self._extends.content()},
            self._extends
        )
