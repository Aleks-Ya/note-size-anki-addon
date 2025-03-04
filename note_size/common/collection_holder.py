from typing import Optional

from anki.collection import Collection


class CollectionHolder:
    def __init__(self):
        self.__col: Optional[Collection] = None

    def set_collection(self, col: Collection) -> None:
        self.__col = col

    def col(self) -> Collection:
        return self.__col
