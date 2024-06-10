import logging
from logging import Logger

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import Note, NoteId

from .size_calculator import SizeCalculator, SizeBytes, MediaFile
from .size_formatter import SizeFormatter, SizeStr, ShortFilename

log: Logger = logging.getLogger(__name__)


class ItemIdCache:
    id_cache: dict[CardId, NoteId] = {}
    note_size_cache: dict[NoteId, SizeBytes] = {}
    note_human_str_cache: dict[NoteId, SizeStr] = {}

    def __init__(self, col: Collection):
        self.col: Collection = col

    def warm_up_cache(self):
        try:
            log.info("Warming up cache...")
            all_note_ids = self.col.find_notes("deck:*")
            for note_id in all_note_ids:
                self.get_note_size(note_id, use_cache=True)
                self.get_note_human_str(note_id, use_cache=True)
            all_card_ids = self.col.find_cards("deck:*")
            for card_id in all_card_ids:
                self.get_note_id_by_card_id(card_id)
            log.info(f"Cache warming up finished: notes={len(all_note_ids)}, cards={len(all_card_ids)}")
        except Exception:
            log.exception("Cache warm-up failed")

    def get_note_id_by_card_id(self, card_id: CardId) -> NoteId:
        if card_id not in self.id_cache:
            self.id_cache[card_id] = self.col.get_card(card_id).nid
        return self.id_cache[card_id]

    def get_note_size(self, note_id: NoteId, use_cache: bool) -> SizeBytes:
        if use_cache and note_id in self.note_size_cache:
            return self.note_size_cache[note_id]
        else:
            note: Note = self.col.get_note(note_id)
            self.note_size_cache[note_id] = SizeCalculator.calculate_note_size(note)
            return self.note_size_cache[note_id]

    def get_note_human_str(self, note_id: NoteId, use_cache: bool) -> SizeStr:
        if use_cache and note_id in self.note_human_str_cache:
            return self.note_human_str_cache[note_id]
        else:
            size: SizeBytes = self.get_note_size(note_id, use_cache)
            self.note_human_str_cache[note_id] = SizeFormatter.bytes_to_human_str(size)
            return self.note_human_str_cache[note_id]

    @staticmethod
    def get_note_size_str(note: Note) -> SizeStr:
        return SizeFormatter.bytes_to_human_str(SizeCalculator.calculate_note_size(note))

    @staticmethod
    def get_total_text_size(note: Note) -> SizeStr:
        return SizeFormatter.bytes_to_human_str(SizeCalculator.total_text_size(note))

    @staticmethod
    def get_total_file_size(note: Note) -> SizeStr:
        return SizeFormatter.bytes_to_human_str(SizeCalculator.total_file_size(note))

    @staticmethod
    def file_size_to_str(file: MediaFile, size: SizeBytes, max_length: int) -> tuple[ShortFilename, SizeStr]:
        return SizeFormatter.file_size_to_human_string(file, size, max_length)
