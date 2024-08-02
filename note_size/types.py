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


class SizeType(Enum):
    TOTAL = "total"
    TEXTS = "texts"
    FILES = "files"


size_types: list[SizeType] = [SizeType.TEXTS, SizeType.FILES, SizeType.TOTAL]
