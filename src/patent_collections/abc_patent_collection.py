from abc import ABCMeta

import pandas as pd


class ABCPatentCollection(metaclass=ABCMeta):
    _df: pd.DataFrame

    def dataframe(self) -> pd.DataFrame:
        return self._df
