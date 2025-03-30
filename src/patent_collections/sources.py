from io import StringIO
from pathlib import Path
from typing import override

import requests
import pandas as pd

from aspects.retry import Retry
from .abc_patent_collection import AbstractPatentCollection


class PatentsFromString(AbstractPatentCollection):
    _raw: str

    def __init__(self, raw: str, columns: list[str], skip_rows: int = 1):
        self._raw = raw
        self._df = pd.read_csv(StringIO(self._raw), skiprows=skip_rows)
        self._df.columns = columns


class PatentsFromFile(AbstractPatentCollection):

    def __init__(self, path: str, columns: list[str], skip_rows: int = 1, encoding: str = 'utf-8'):
        self._path = path
        with open(path, "rb") as f:
            self._raw = f.read()
        self._df = pd.read_csv(StringIO(self._raw.decode(encoding=encoding)), skiprows=skip_rows)
        self._df.columns = columns


class PatentsFromGoogle(AbstractPatentCollection):

    def __init__(self, uri: str, skip_rows: int = 1):
        self._uri = uri
        self._skip_rows = skip_rows
        self._df = pd.DataFrame()  # Empty DataFrame

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


class PatentsFile:

    def __init__(self, path: str, patents: AbstractPatentCollection, force: bool | None = None):
        if isinstance(path, str) and isinstance(patents, AbstractPatentCollection) and isinstance(force, bool):
            # Primary constructor
            assert Path(path).parent.is_dir()  # The Directory must exist. This Policy is subject to change
            self._path = path
            self._patents = patents
        elif isinstance(path, str) and isinstance(patents, AbstractPatentCollection) and force is None:
            # secondary constructor call primary
            self.__init__(
                path=path,
                patents=patents,
                force=False  # default value
            )
        else:
            raise AttributeError()

    def save(self):
        self._patents.dataframe().to_csv(self._path, index=False)
