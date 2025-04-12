import logging
import sys
from logging import Logger
from typing import Optional, NewType

from ..calculator.size_formatter import SizeFormatter
from ..common.types import SizeStr, SizeBytes, SignificantDigits, ColorName

log: Logger = logging.getLogger(__name__)


class Level:
    def __init__(self, light_theme_color: Optional[ColorName], dark_theme_color: Optional[ColorName],
                 min_size_bytes: SizeBytes, max_size_bytes: SizeBytes, min_size_str: SizeStr,
                 max_size_str: SizeStr) -> None:
        self.light_theme_color: ColorName = light_theme_color
        self.dark_theme_color: ColorName = dark_theme_color
        self.min_size_bytes: SizeBytes = min_size_bytes
        self.max_size_bytes: SizeBytes = max_size_bytes
        self.min_size_str: SizeStr = min_size_str
        self.max_size_str: SizeStr = max_size_str

    def __repr__(self) -> str:
        return (f"Level: {self.light_theme_color},{self.dark_theme_color}, {self.min_size_bytes}, "
                f"{self.max_size_bytes}, {self.min_size_str}, {self.max_size_str}")

    def __eq__(self, other) -> bool:
        return isinstance(other, Level) and \
            self.light_theme_color == other.light_theme_color and \
            self.dark_theme_color == other.dark_theme_color and \
            self.min_size_bytes == other.min_size_bytes and \
            self.max_size_bytes == other.max_size_bytes and \
            self.min_size_str == other.min_size_str and \
            self.max_size_str == other.max_size_str


LevelParserKey = NewType("LevelParserKey", str)
LevelDict = NewType("LevelDict", dict[LevelParserKey, Optional[ColorName]])


class LevelParser:
    light_theme_color_key: LevelParserKey = 'Light Theme Color'
    dark_theme_color_key: LevelParserKey = 'Dark Theme Color'
    min_size_key: LevelParserKey = 'Min Size'
    max_size_key: LevelParserKey = 'Max Size'
    __default_light_theme_color: ColorName = ColorName("LightYellow")
    __default_dark_theme_color: ColorName = ColorName("Yellow")

    def __init__(self, size_formatter: SizeFormatter) -> None:
        self.__size_formatter: SizeFormatter = size_formatter
        log.debug(f"{self.__class__.__name__} was instantiated")

    def add_level(self, levels: list[LevelDict]) -> None:
        if len(levels) > 0:
            previous_level: LevelDict = levels[len(levels) - 1]
            if len(levels) > 1:
                penultimate_level: LevelDict = levels[len(levels) - 2]
                penultimate_max_size_str: SizeStr = SizeStr(penultimate_level[self.max_size_key])
                penultimate_max_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(penultimate_max_size_str)
                new_previous_level_size_bytes: SizeBytes = SizeBytes(penultimate_max_size_bytes * 2)
                new_previous_level_size_str: SizeStr = self.__size_formatter.bytes_to_str(
                    new_previous_level_size_bytes, SignificantDigits(0))
                previous_level[self.max_size_key] = new_previous_level_size_str
            else:
                previous_level[self.max_size_key] = "100 KB"
        new_level: LevelDict = LevelDict({
            self.light_theme_color_key: self.__default_light_theme_color,
            self.dark_theme_color_key: self.__default_dark_theme_color,
            self.max_size_key: None
        })
        levels.append(new_level)

    def remove_level(self, levels: list[LevelDict], level_to_remove: int) -> None:
        if len(levels) < 2:
            return
        del levels[level_to_remove]
        last_level: LevelDict = levels[len(levels) - 1]
        last_level[self.max_size_key] = None

    def parse_levels(self, levels: list[LevelDict]) -> list[Level]:
        level_list: list[Level] = []
        for i, level in enumerate(levels):
            previous_level_max_size: str = levels[i - 1][self.max_size_key] if i > 0 else None
            level[self.min_size_key] = previous_level_max_size
            is_last: bool = i == len(levels) - 1
            level[self.max_size_key] = None if is_last else level[self.max_size_key]
            level_list.append(self.__parse_level(level))
        return level_list

    def __parse_level(self, level: LevelDict) -> Level:
        light_theme_color: Optional[ColorName] = level.get(self.light_theme_color_key, self.__default_light_theme_color)
        dark_theme_color: Optional[ColorName] = level.get(self.dark_theme_color_key, self.__default_dark_theme_color)
        min_size_opt: Optional[SizeStr] = SizeStr(level.get(self.min_size_key))
        max_size_opt: Optional[SizeStr] = SizeStr(level.get(self.max_size_key))
        min_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(min_size_opt) if min_size_opt else 0
        max_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(max_size_opt) if max_size_opt \
            else sys.maxsize
        min_size_str: SizeStr = min_size_opt if min_size_opt else '0 B'
        max_size_str: SizeStr = max_size_opt if max_size_opt else '∞'
        return Level(light_theme_color, dark_theme_color, min_size_bytes, max_size_bytes, min_size_str, max_size_str)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
