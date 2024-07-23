import logging
import sys
from logging import Logger
from typing import Optional

from anki.notes import NoteId, Note

from .button_label import ButtonLabel
from ..cache.item_id_cache import ItemIdCache
from ..config.config import Config
from ..types import SizeStr, SizeBytes, SizeType
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class Level:
    def __init__(self, color: str, min_size: SizeBytes, max_size: SizeBytes):
        self.color: str = color
        self.min_size: SizeBytes = min_size
        self.max_size: SizeBytes = max_size


class ButtonFormatter:
    def __init__(self, item_id_cache: ItemIdCache, size_calculator: SizeCalculator, config: Config):
        self.__config: Config = config
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_zero_size_label(self) -> ButtonLabel:
        size_bytes: SizeBytes = SizeBytes(0)
        size: SizeStr = SizeFormatter.bytes_to_str(size_bytes)
        color: str = self.__get_color(size_bytes)
        label: ButtonLabel = ButtonLabel(f"{size}", color)
        log.debug(f"Zero size label was created: {label}")
        return label

    def get_add_mode_label(self, note: Note) -> ButtonLabel:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_size(note, use_cache=False)
        size_str: SizeStr = SizeFormatter.bytes_to_str(size_bytes)
        color: str = self.__get_color(size_bytes)
        label: ButtonLabel = ButtonLabel(f"{size_str}", color)
        log.debug(f"Add mode label created for NoteId {note.id}: {label}")
        return label

    def get_edit_mode_label(self, note_id: NoteId) -> ButtonLabel:
        size_bytes: SizeBytes = self.__item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
        size_str: SizeStr = self.__item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        color: str = self.__get_color(size_bytes)
        label: ButtonLabel = ButtonLabel(f"{size_str}", color)
        log.debug(f"Edit mode label created for NoteId {note_id}: {label}")
        return label

    def __get_color(self, size: SizeBytes) -> str:
        if self.__config.size_button_color_enabled():
            color_levels: list[Level] = self.__parse_levels(self.__config.size_button_color_levels())
            for level in color_levels:
                if level.min_size <= size < level.max_size:
                    return level.color
        return ""

    @staticmethod
    def __parse_levels(levels: list[dict[str, str]]) -> list[Level]:
        levels_list: list[Level] = []
        for level in levels:
            color: str = level.get("Color")
            min_size_str: Optional[SizeStr] = SizeStr(level.get("Min Size"))
            max_size_str: Optional[SizeStr] = SizeStr(level.get("Max Size"))
            min_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(min_size_str) if min_size_str else 0
            max_size_bytes: SizeBytes = SizeFormatter.str_to_bytes(max_size_str) if max_size_str \
                else sys.maxsize
            levels_list.append(Level(color, min_size_bytes, max_size_bytes))
        return levels_list
