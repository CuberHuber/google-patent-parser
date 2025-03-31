from io import StringIO
from typing import override

from multipledispatch import dispatch
import requests
import pandas as pd

from aspects.cachable import Cachable
from aspects.retry import Retry
from .abc_patent_collection import AbstractPatentCollection


class PatentsInString(AbstractPatentCollection):
    _raw: str

    @dispatch(str, list, int)
    def __init__(self, raw: str, columns: list[str], skip_rows: int):
        self._raw = raw
        self._columns = columns
        self._skip_rows = skip_rows
        self._df = pd.DataFrame()

    @dispatch(str, list)
    def __init__(self, raw: str, columns: list[str]):
        self.__init__(raw, columns, 0)

    @override
    @Cachable(True)
    def dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(StringIO(self._raw), skiprows=self._skip_rows)
        df.columns = self._columns
        return df


class PatentsInFile(AbstractPatentCollection):

    @dispatch(str, list, int, str)
    def __init__(self, path: str, columns: list[str], skip_rows: int, encoding: str):
        self._path = path
        self._columns = columns
        self._encoding = encoding
        self._skip_rows = skip_rows

    @dispatch(str, list, int)
    def __init__(self, path: str, columns: list[str], skip_rows: int):
        self.__init__(path, columns, skip_rows, 'utf-8')

    @dispatch(str, list)
    def __init__(self, path: str, columns: list[str]):
        self.__init__(path, columns, 0)

    @override
    def dataframe(self) -> pd.DataFrame:
        with open(self._path, "rb") as f:
            _raw = f.read()
            self._df = pd.read_csv(StringIO(_raw.decode(encoding=self._encoding)), skiprows=self._skip_rows)
            self._df.columns = self._columns
        return self._df


class PatentsInGoogle(AbstractPatentCollection):

    @dispatch(str, int)
    def __init__(self, uri: str, skip_rows: int):
        self._uri = uri
        self._skip_rows = skip_rows
        self._df = pd.DataFrame()

    @dispatch(str)
    def __init(self, uri: str):
        self.__init__(uri, 1)

    @Retry(times=3, delay=3)
    def _content(self) -> bytes:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(self._uri, headers=headers)
        response.raise_for_status()
        return response.content

    @override
    def dataframe(self) -> pd.DataFrame:
        return pd.read_csv(StringIO(self._content().decode()), skiprows=self._skip_rows)
