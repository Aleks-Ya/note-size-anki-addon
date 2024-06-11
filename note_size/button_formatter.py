import logging
from logging import Logger
from typing import NewType

from anki.notes import NoteId, Note

from .item_id_cache import ItemIdCache
from .size_calculator import SizeBytes, SizeCalculator
from .size_formatter import SizeStr, SizeFormatter

log: Logger = logging.getLogger(__name__)

ButtonLabel = NewType("ButtonLabel", str)


class ButtonFormatter:
    def __init__(self, item_id_cache: ItemIdCache):
        self.item_id_cache: ItemIdCache = item_id_cache

    @staticmethod
    def get_zero_size_label() -> ButtonLabel:
        size: SizeStr = SizeFormatter.bytes_to_str(SizeBytes(0))
        return ButtonLabel(f"Size: {size}")

    @staticmethod
    def get_add_mode_label(note: Note) -> ButtonLabel:
        size: SizeStr = SizeFormatter.bytes_to_str(SizeCalculator.calculate_note_size(note))
        return ButtonLabel(f"Size: {size}")

    def get_edit_mode_label(self, note_id: NoteId) -> ButtonLabel:
        size: SizeStr = self.item_id_cache.get_note_size_str(note_id, use_cache=False)
        return ButtonLabel(f"Size: {size}")
