import logging
from logging import Logger

from anki.notes import NoteId, Note

from ..cache.item_id_cache import ItemIdCache
from ..types import SizeStr, SizeBytes, ButtonLabel
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ButtonFormatter:
    def __init__(self, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
        self.item_id_cache: ItemIdCache = item_id_cache
        self.size_calculator: SizeCalculator = size_calculator

    @staticmethod
    def get_zero_size_label() -> ButtonLabel:
        size: SizeStr = SizeFormatter.bytes_to_str(SizeBytes(0))
        return ButtonLabel(f"Size: {size}")

    def get_add_mode_label(self, note: Note) -> ButtonLabel:
        size: SizeStr = SizeFormatter.bytes_to_str(self.size_calculator.calculate_note_size(note))
        return ButtonLabel(f"Size: {size}")

    def get_edit_mode_label(self, note_id: NoteId) -> ButtonLabel:
        size: SizeStr = self.item_id_cache.get_note_size_str(note_id, ItemIdCache.TOTAL_SIZE, use_cache=False)
        return ButtonLabel(f"Size: {size}")
