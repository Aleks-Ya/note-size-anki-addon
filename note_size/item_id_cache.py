import logging
from logging import Logger

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import Note, NoteId

from .size_calculator import SizeCalculator
from .size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ItemIdCache:
    id_cache: dict[CardId, NoteId] = {}
    note_size_cache: dict[NoteId, int] = {}
    note_human_str_cache: dict[NoteId, str] = {}

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

    def get_note_size(self, note_id: NoteId, use_cache: bool) -> int:
        if use_cache and note_id in self.note_size_cache:
            return self.note_size_cache[note_id]
        else:
            note: Note = self.col.get_note(note_id)
            self.note_size_cache[note_id] = SizeCalculator.calculate_note_size(note)
            return self.note_size_cache[note_id]

    def get_note_human_str(self, note_id: NoteId, use_cache: bool) -> str:
        if use_cache and note_id in self.note_human_str_cache:
            return self.note_human_str_cache[note_id]
        else:
            size: int = self.get_note_size(note_id, use_cache)
            self.note_human_str_cache[note_id] = SizeFormatter.bytes_to_human_str(size)
            return self.note_human_str_cache[note_id]

    def total_text_size_str(self, note: Note) -> str:
        return SizeFormatter.bytes_to_human_str(SizeCalculator.total_text_size(note))

    def total_file_size_str(self, note: Note) -> str:
        return SizeFormatter.bytes_to_human_str(SizeCalculator.total_file_size(note))

    def file_size_to_human_string(self, file: str, size: int, max_length: int) -> tuple[str, str]:
        return SizeFormatter.file_size_to_human_string(file, size, max_length)
