from enum import Enum
from typing import NewType

SizeBytes = NewType("SizeBytes", int)
FilesNumber = NewType("FilesNumber", int)
NotesNumber = NewType("NotesNumber", int)
MediaFile = NewType("MediaFile", str)
SizeStr = NewType("SizeStr", str)
ShortFilename = NewType("ShortFilename", str)
FieldName = NewType("FieldName", str)
FieldContent = NewType("FieldContent", str)
FileContent = NewType("FileContent", str)


class FileType(Enum):
    OTHER = 0
    IMAGE = 1
    AUDIO = 2
    VIDEO = 3


class SizeType(Enum):
    TOTAL = "total"
    TEXTS = "texts"
    FILES = "files"


class FileSize:
    def __init__(self, size: SizeBytes, exists: bool = True) -> None:
        self.size: SizeBytes = size
        self.exists: bool = exists

    def __hash__(self):
        return hash((self.size, self.exists))

    def __eq__(self, __other):
        return type(self) == type(__other) and self.size == __other.size and self.exists == __other.exists

    def __repr__(self):
        return f"FileSize(size={self.size},exists={self.exists})"
