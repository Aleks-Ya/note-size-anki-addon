import logging
import sys
from logging import Logger
from typing import Optional, NewType

from ..calculator.size_formatter import SizeFormatter
from ..common.types import SizeStr, SizeBytes, SizePrecision

log: Logger = logging.getLogger(__name__)


class Level:
    def __init__(self, color: str, min_size_bytes: SizeBytes, max_size_bytes: SizeBytes,
                 min_size_str: SizeStr, max_size_str: SizeStr) -> None:
        self.color: str = color
        self.min_size_bytes: SizeBytes = min_size_bytes
        self.max_size_bytes: SizeBytes = max_size_bytes
        self.min_size_str: SizeStr = min_size_str
        self.max_size_str: SizeStr = max_size_str

    def __repr__(self) -> str:
        return (f"Level: {self.color}, {self.min_size_bytes}, {self.max_size_bytes}, "
                f"{self.min_size_str}, {self.max_size_str}")

    def __eq__(self, other) -> bool:
        return isinstance(other, Level) and \
            self.color == other.color and \
            self.min_size_bytes == other.min_size_bytes and \
            self.max_size_bytes == other.max_size_bytes and \
            self.min_size_str == other.min_size_str and \
            self.max_size_str == other.max_size_str


LevelDict = NewType("LevelDict", dict[str, Optional[str]])


class LevelParser:
    __color_key: str = 'Color'
    __min_size_key: str = 'Min Size'
    __max_size_key: str = 'Max Size'

    def __init__(self, size_formatter: SizeFormatter) -> None:
        self.__size_formatter: SizeFormatter = size_formatter
        log.debug(f"{self.__class__.__name__} was instantiated")

    def add_level(self, levels: list[LevelDict]) -> None:
        if len(levels) > 0:
            previous_level: LevelDict = levels[len(levels) - 1]
            if len(levels) > 1:
                penultimate_level: LevelDict = levels[len(levels) - 2]
                penultimate_max_size_str: SizeStr = SizeStr(penultimate_level[self.__max_size_key])
                penultimate_max_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(penultimate_max_size_str)
                new_previous_level_size_bytes: SizeBytes = SizeBytes(penultimate_max_size_bytes * 2)
                new_previous_level_size_str: SizeStr = self.__size_formatter.bytes_to_str(
                    new_previous_level_size_bytes, SizePrecision(0))
                previous_level[self.__max_size_key] = new_previous_level_size_str
            else:
                previous_level[self.__max_size_key] = "100 KB"
        new_level: LevelDict = LevelDict({
            self.__color_key: "Yellow",
            self.__max_size_key: None
        })
        levels.append(new_level)

    def remove_level(self, levels: list[LevelDict], level_to_remove: int) -> None:
        if len(levels) < 2:
            return
        del levels[level_to_remove]
        last_level: LevelDict = levels[len(levels) - 1]
        last_level[self.__max_size_key] = None

    def parse_levels(self, levels: list[LevelDict]) -> list[Level]:
        level_list: list[Level] = []
        for i, level in enumerate(levels):
            previous_level_max_size: str = levels[i - 1][self.__max_size_key] if i > 0 else None
            level[self.__min_size_key] = previous_level_max_size
            is_last: bool = i == len(levels) - 1
            level[self.__max_size_key] = None if is_last else level[self.__max_size_key]
            level_list.append(self.__parse_level(level))
        return level_list

    def __parse_level(self, level: LevelDict) -> Level:
        color: str = level.get("Color")
        min_size_opt: Optional[SizeStr] = SizeStr(level.get(self.__min_size_key))
        max_size_opt: Optional[SizeStr] = SizeStr(level.get(self.__max_size_key))
        min_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(min_size_opt) if min_size_opt else 0
        max_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(max_size_opt) if max_size_opt \
            else sys.maxsize
        min_size_str: SizeStr = min_size_opt if min_size_opt else '0 B'
        max_size_str: SizeStr = max_size_opt if max_size_opt else '∞'
        return Level(color, min_size_bytes, max_size_bytes, min_size_str, max_size_str)
