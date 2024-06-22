from enum import Enum
from typing import NewType

SizeBytes = NewType("SizeBytes", int)
MediaFile = NewType("MediaFile", str)
ButtonLabel = NewType("ButtonLabel", str)
SizeStr = NewType("SizeStr", str)
ShortFilename = NewType("ShortFilename", str)
FieldName = NewType("FieldName", str)
FieldContent = NewType("FieldContent", str)
FileContent = NewType("FileContent", str)


class SizeType(Enum):
    TOTAL = "total"
    TEXTS = "texts"
    FILES = "files"
