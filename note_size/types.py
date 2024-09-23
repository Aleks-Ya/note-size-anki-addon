from enum import Enum
from typing import NewType

SizeBytes = NewType("SizeBytes", int)
FilesNumber = NewType("FilesNumber", int)
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
