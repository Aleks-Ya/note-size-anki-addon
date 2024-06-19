from enum import Enum
from typing import NewType

SizeBytes = NewType("SizeBytes", int)
MediaFile = NewType("MediaFile", str)
ButtonLabel = NewType("ButtonLabel", str)
SizeStr = NewType("SizeStr", str)
ShortFilename = NewType("ShortFilename", str)


class SizeType(Enum):
    TOTAL = "total"
    TEXTS = "texts"
    FILES = "files"
