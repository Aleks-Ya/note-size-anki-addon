import logging
from logging import Logger

from anki.notes import NoteId, Note

from .button_label import ButtonLabel
from ....cache.item_id_cache import ItemIdCache
from ....config.config import Config
from ....config.level_parser import Level, LevelParser
from ....types import SizeStr, SizeBytes, SizeType
from ....calculator.size_calculator import SizeCalculator
from ....calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ButtonFormatter:
    def __init__(self, item_id_cache: ItemIdCache, size_calculator: SizeCalculator, config: Config) -> None:
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
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_total_size(note, use_cache=False)
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
        if self.__config.get_size_button_color_enabled():
            color_levels: list[Level] = LevelParser.parse_levels(self.__config.get_size_button_color_levels())
            for level in color_levels:
                if level.min_size_bytes <= size < level.max_size_bytes:
                    return level.color
        return ""
