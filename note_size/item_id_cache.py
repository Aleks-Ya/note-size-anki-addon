import logging
from logging import Logger
from threading import RLock

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import Note, NoteId

from .types import SizeStr, SizeBytes
from .size_calculator import SizeCalculator
from .size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ItemIdCache:

    def __init__(self, col: Collection, size_calculator: SizeCalculator):
        self.col: Collection = col
        self.size_calculator: SizeCalculator = size_calculator
        self.id_cache: dict[CardId, NoteId] = {}
        self.size_bytes_cache: dict[NoteId, SizeBytes] = {}
        self.size_str_cache: dict[NoteId, SizeStr] = {}
        self.id_cache_lock: RLock = RLock()
        self.size_bytes_cache_lock: RLock = RLock()
        self.size_str_lock: RLock = RLock()

    def warm_up_cache(self):
        try:
            log.info("Warming up cache...")
            all_note_ids = self.col.find_notes("deck:*")
            for note_id in all_note_ids:
                self.get_note_size(note_id, use_cache=True)
                self.get_note_size_str(note_id, use_cache=True)
            all_card_ids = self.col.find_cards("deck:*")
            for card_id in all_card_ids:
                self.get_note_id_by_card_id(card_id)
            log.info(f"Cache warming up finished: notes={len(all_note_ids)}, cards={len(all_card_ids)}")
        except Exception:
            log.exception("Cache warm-up failed")

    def get_note_id_by_card_id(self, card_id: CardId) -> NoteId:
        with self.id_cache_lock:
            if card_id not in self.id_cache:
                self.id_cache[card_id] = self.col.get_card(card_id).nid
            return self.id_cache[card_id]

    def get_note_size(self, note_id: NoteId, use_cache: bool) -> SizeBytes:
        with self.size_bytes_cache_lock:
            if use_cache and note_id in self.size_bytes_cache:
                return self.size_bytes_cache[note_id]
            else:
                note: Note = self.col.get_note(note_id)
                self.size_bytes_cache[note_id] = self.size_calculator.calculate_note_size(note)
                return self.size_bytes_cache[note_id]

    def get_note_size_str(self, note_id: NoteId, use_cache: bool) -> SizeStr:
        with self.size_str_lock:
            if use_cache and note_id in self.size_str_cache:
                return self.size_str_cache[note_id]
            else:
                size: SizeBytes = self.get_note_size(note_id, use_cache)
                self.size_str_cache[note_id] = SizeFormatter.bytes_to_str(size)
                return self.size_str_cache[note_id]
