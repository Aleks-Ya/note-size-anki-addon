import logging
from logging import Logger
from threading import RLock

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import NoteId, Note

from ..types import SizeStr, SizeBytes, SizeType
from ..size_calculator import SizeCalculator
from ..size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ItemIdCache:
    TOTAL_SIZE: SizeType = SizeType("total")
    TEXTS_SIZE: SizeType = SizeType("texts")
    FILES_SIZE: SizeType = SizeType("files")

    def __init__(self, col: Collection, size_calculator: SizeCalculator):
        self.lock: RLock = RLock()
        self.col: Collection = col
        self.size_calculator: SizeCalculator = size_calculator
        self.id_cache: dict[CardId, NoteId] = {}
        self.size_bytes_caches: dict[SizeType, dict[NoteId, SizeBytes]] = {ItemIdCache.TOTAL_SIZE: {},
                                                                           ItemIdCache.TEXTS_SIZE: {},
                                                                           ItemIdCache.FILES_SIZE: {}}
        self.size_str_caches: dict[SizeType, dict[NoteId, SizeStr]] = {ItemIdCache.TOTAL_SIZE: {},
                                                                       ItemIdCache.TEXTS_SIZE: {},
                                                                       ItemIdCache.FILES_SIZE: {}}

    def warm_up_cache(self):
        try:
            log.info("Warming up cache...")
            all_note_ids = self.col.find_notes("deck:*")
            for note_id in all_note_ids:
                for size_type in [ItemIdCache.TEXTS_SIZE, ItemIdCache.FILES_SIZE, ItemIdCache.TOTAL_SIZE]:
                    self.get_note_size_bytes(note_id, size_type, use_cache=True)
                    self.get_note_size_str(note_id, size_type, use_cache=True)
            all_card_ids = self.col.find_cards("deck:*")
            for card_id in all_card_ids:
                self.get_note_id_by_card_id(card_id)
            log.info(f"Cache warming up finished: notes={len(all_note_ids)}, cards={len(all_card_ids)}")
        except Exception:
            log.exception("Cache warm-up failed")

    def get_note_id_by_card_id(self, card_id: CardId) -> NoteId:
        with self.lock:
            if card_id not in self.id_cache:
                self.id_cache[card_id] = self.col.get_card(card_id).nid
            return self.id_cache[card_id]

    def get_note_size_bytes(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeBytes:
        with self.lock:
            cache: dict[NoteId, SizeBytes] = self.size_bytes_caches[size_type]
            if use_cache and note_id in cache:
                return cache[note_id]
            else:
                note: Note = self.col.get_note(note_id)
                if size_type == ItemIdCache.TOTAL_SIZE:
                    size: SizeBytes = self.size_calculator.calculate_note_size(note)
                if size_type == ItemIdCache.TEXTS_SIZE:
                    size: SizeBytes = self.size_calculator.calculate_texts_size(note)
                if size_type == ItemIdCache.FILES_SIZE:
                    size: SizeBytes = self.size_calculator.calculate_files_size(note)
                cache[note_id] = size
                return cache[note_id]

    def get_note_size_str(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeStr:
        with self.lock:
            cache: dict[NoteId, SizeStr] = self.size_str_caches[size_type]
            if use_cache and note_id in cache:
                return cache[note_id]
            else:
                size: SizeBytes = self.get_note_size_bytes(note_id, size_type, use_cache)
                cache[note_id] = SizeFormatter.bytes_to_str(size)
                return cache[note_id]
