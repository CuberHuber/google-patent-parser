from pathlib import Path

from multipledispatch import dispatch

from .abc_patent_collection import AbstractPatentCollection


class PatentsToFile:

    @dispatch(str, AbstractPatentCollection, bool)
    def __init__(self, path: str, patents: AbstractPatentCollection, force: bool):
        """Primary constructor"""
        assert Path(path).parent.is_dir()  # The Directory must exist. This Policy is subject to change
        self._path = path
        self._patents = patents
        self._force = force

    @dispatch(str, AbstractPatentCollection)
    def __init__(self, path: str, patents: AbstractPatentCollection):
        """Secondary constructor"""
        self.__init__(
            path=path,
            patents=patents,
            force=False
        )

    def save(self):
        self._patents.dataframe().to_csv(self._path, index=False)
