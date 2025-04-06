import logging
from logging import Logger

from anki.notes import NoteId, Note

from .editor_button_label import EditorButtonLabel
from ....cache.size_str_cache import SizeStrCache
from ....config.config import Config
from ....config.level_parser import Level, LevelParser
from ....common.types import SizeStr, SizeBytes, SizeType, SignificantDigits, ColorName
from ....calculator.size_calculator import SizeCalculator
from ....calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class EditorButtonFormatter:
    def __init__(self, size_str_cache: SizeStrCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                 level_parser: LevelParser, config: Config) -> None:
        self.__config: Config = config
        self.__size_str_cache: SizeStrCache = size_str_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__level_parser: LevelParser = level_parser
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_zero_size_label(self) -> EditorButtonLabel:
        size_bytes: SizeBytes = SizeBytes(0)
        significant_digits: SignificantDigits = self.__config.get_size_button_significant_digits()
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes, significant_digits)
        color: ColorName = self.__get_color(size_bytes)
        label: EditorButtonLabel = EditorButtonLabel(f"{size}", color)
        log.debug(f"Zero size label was created: {label}")
        return label

    def get_add_mode_label(self, note: Note) -> EditorButtonLabel:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=False)
        significant_digits: SignificantDigits = self.__config.get_size_button_significant_digits()
        size_str: SizeStr = self.__size_formatter.bytes_to_str(size_bytes, significant_digits)
        color: ColorName = self.__get_color(size_bytes)
        label: EditorButtonLabel = EditorButtonLabel(f"{size_str}", color)
        log.debug(f"Add mode label created for NoteId {note.id}: {label}")
        return label

    def get_edit_mode_label(self, note_id: NoteId) -> EditorButtonLabel:
        size_bytes: SizeBytes = self.__size_calculator.get_note_size(note_id, SizeType.TOTAL, use_cache=False)
        significant_digits: SignificantDigits = self.__config.get_size_button_significant_digits()
        size_str: SizeStr = self.__size_str_cache.get_note_size_str(
            note_id, SizeType.TOTAL, significant_digits, use_cache=False)
        color: ColorName = self.__get_color(size_bytes)
        label: EditorButtonLabel = EditorButtonLabel(f"{size_str}", color)
        log.debug(f"Edit mode label created for NoteId {note_id}: {label}")
        return label

    def __get_color(self, size: SizeBytes) -> ColorName:
        if self.__config.get_size_button_color_enabled():
            color_levels: list[Level] = self.__level_parser.parse_levels(self.__config.get_size_button_color_levels())
            for level in color_levels:
                if level.min_size_bytes <= size < level.max_size_bytes:
                    return level.light_theme_color
        return ColorName("")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
