import logging
from logging import Logger

from anki.notes import NoteId, Note

from ..cache.item_id_cache import ItemIdCache
from ..types import SizeStr, SizeBytes, ButtonLabel, SizeType
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ButtonFormatter:
    def __init__(self, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
        self.item_id_cache: ItemIdCache = item_id_cache
        self.size_calculator: SizeCalculator = size_calculator
        log.debug(f"{self.__class__.__name__} was instantiated")

    @staticmethod
    def get_zero_size_label() -> ButtonLabel:
        size: SizeStr = SizeFormatter.bytes_to_str(SizeBytes(0))
        label: ButtonLabel = ButtonLabel(f"Size: {size}")
        log.debug(f"Zero size label was created: {label}")
        return label

    def get_add_mode_label(self, note: Note) -> ButtonLabel:
        size: SizeStr = SizeFormatter.bytes_to_str(self.size_calculator.calculate_note_size(note, use_cache=False))
        label: ButtonLabel = ButtonLabel(f"Size: {size}")
        log.debug(f"Add mode label created for NoteId {note.id}: {label}")
        return label

    def get_edit_mode_label(self, note_id: NoteId) -> ButtonLabel:
        size: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        label: ButtonLabel = ButtonLabel(f"Size: {size}")
        log.debug(f"Edit mode label created for NoteId {note_id}: {label}")
        return label
