from typing import override

import pandas as pd
from tqdm import tqdm

from aspects.cachable import Cachable
from patents.abc_patent import ABCPatent
from patents.extends.google_patent_extends import GooglePatentExtends
from patents.google_patent import GooglePatent
from .abc_patent_collection import ABCPatentCollection


class Limited(ABCPatentCollection):

    def __init__(self, patents: ABCPatentCollection, limit: int):
        self._df = patents.dataframe()
        self._patents = patents
        self._number = limit

    @override
    @Cachable
    def dataframe(self) -> pd.DataFrame:
        return self._df.head(self._number)


class WithNotNullField(ABCPatentCollection):

    def __init__(self, patents: ABCPatentCollection, key: str):
        self._df = patents.dataframe()
        self._patents = patents
        self._key = key

    @override
    @Cachable
    def dataframe(self) -> pd.DataFrame:
        return self._df[self._df[self._key].notna()].copy(True)


class OnlyWithKeys(ABCPatentCollection):

    def __init__(self, patents: ABCPatentCollection, keys: list[str]):
        self._patents = patents
        self._df = patents.dataframe()
        self._keys = keys

    @override
    @Cachable
    def dataframe(self) -> pd.DataFrame:
        return self._df[self._keys].copy(True)


class WithRenamedColumn(ABCPatentCollection):

    def __init__(self, patents: ABCPatentCollection, old: str, new: str):
        self._patents = patents
        self._old = old
        self._new = new
        self._df = patents.dataframe().rename(
            columns={
                old: new
            }
        )


class WithExtendsColumn(ABCPatentCollection):

    def __init__(self, patents: ABCPatentCollection):
        # Primary constructor
        self._patents = patents

    @override
    @Cachable
    def dataframe(self) -> pd.DataFrame:
        result = []
        for _, row in tqdm(self._patents.dataframe().iterrows()):
            patent = self._patent(row)
            result.append(patent)
        return pd.DataFrame(result)

    def _patent(self, row: pd.Series) -> ABCPatent:
        patent = GooglePatent(
            row.to_dict().get('uri'),
            row.to_dict(),
            GooglePatentExtends(
                row.to_dict().get('uri')
            )
        ).with_extends()
        return patent
