from .abc_patent import ABCPatent
from .extends.abc_patent_extends import ABCPatentExtends
from .extends.empty_patent_extends import EmptyGooglePatentExtends


class GooglePatent(ABCPatent):
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

    def __init__(self, uri: str, row: dict | None = None, extends: ABCPatentExtends | None = None):
        if isinstance(uri, str) and isinstance(row, dict) and isinstance(extends, ABCPatentExtends):
            # primary constructor
            assert row.get("uri") is not None and row.get("uri") == uri
            super().__init__(row)
            self._extends = extends
            self._uri = uri

        elif isinstance(uri, str) and isinstance(row, dict) and extends is None:
            # secondary constructor call prima
            self.__init__(
                uri=uri,
                row=row,
                extends=EmptyGooglePatentExtends(),
            )

        elif isinstance(uri, str) and row is None and extends is None:
            # secondary constructor
            self.__init__(
                uri=uri,
                row={'uri': uri},
                extends=EmptyGooglePatentExtends(),
            )

        else:
            raise AttributeError('uri must be str')

    def with_extends(self) -> ABCPatent:
        return GooglePatent(
            uri=self._uri,
            row={**self.data, **self._extends.content()},
            extends=self._extends
        )
