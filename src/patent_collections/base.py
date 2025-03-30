import pandas as pd

from .abc_patent_collection import AbstractPatentCollection


class Patents(AbstractPatentCollection):

    def __init__(self, df: pd.DataFrame):
        self._df = df
