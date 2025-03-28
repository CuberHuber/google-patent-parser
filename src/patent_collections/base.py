import pandas as pd

from .abc_patent_collection import ABCPatentCollection


class Patents(ABCPatentCollection):

    def __init__(self, df: pd.DataFrame):
        self._df = df
