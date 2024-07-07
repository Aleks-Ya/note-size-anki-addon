import logging
from datetime import datetime
from logging import Logger
from threading import RLock
from typing import Sequence

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import NoteId

from ..config.config import Config
from ..types import SizeStr, SizeBytes, SizeType, size_types
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ItemIdCache:

    def __init__(self, col: Collection, size_calculator: SizeCalculator, config: Config):
        self.__warmup_enabled: bool = config.cache_warm_up_enabled()
        self.__lock: RLock = RLock()
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        self.__id_cache: dict[CardId, NoteId] = {}
        self.__size_bytes_caches: dict[SizeType, dict[NoteId, SizeBytes]] = {SizeType.TOTAL: {},
                                                                             SizeType.TEXTS: {},
                                                                             SizeType.FILES: {}}
        self.__size_str_caches: dict[SizeType, dict[NoteId, SizeStr]] = {SizeType.TOTAL: {},
                                                                         SizeType.TEXTS: {},
                                                                         SizeType.FILES: {}}
        self.__total_texts_size: SizeBytes = SizeBytes(0)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def warm_up_cache(self) -> None:
        try:
            if not self.__warmup_enabled:
                log.info("Cache warmup is disabled")
                return
            log.info("Warming up cache...")
            start_time: datetime = datetime.now()
            all_note_ids: Sequence[NoteId] = self.__col.find_notes("deck:*")
            for note_id in all_note_ids:
                for size_type in size_types:
                    self.get_note_size_bytes(note_id, size_type, use_cache=True)
                    self.get_note_size_str(note_id, size_type, use_cache=True)
            all_card_ids: Sequence[int] = self.__col.find_cards("deck:*")
            for card_id in all_card_ids:
                self.get_note_id_by_card_id(card_id)
            end_time: datetime = datetime.now()
            duration_sec: int = round((end_time - start_time).total_seconds())
            size_bytes_cache_lengths: str = str([f"{cache[0]}={len(cache[1].keys())}"
                                                 for cache in self.__size_bytes_caches.items()])
            size_str_cache_lengths: str = str([f"{cache[0]}={len(cache[1].keys())}"
                                               for cache in self.__size_str_caches.items()])
            log.info(f"Cache warming up finished: notes={len(all_note_ids)}, cards={len(all_card_ids)}, "
                     f"duration_sec={duration_sec}, size_bytes_cache_lengths={size_bytes_cache_lengths}, "
                     f"size_str_cache_lengths={size_str_cache_lengths}, id_cache_length={len(self.__id_cache.keys())}")
        except Exception:
            log.exception("Cache warm-up failed")

    def get_note_id_by_card_id(self, card_id: CardId) -> NoteId:
        with self.__lock:
            if card_id not in self.__id_cache:
                self.__id_cache[card_id] = self.__col.get_card(card_id).nid
            return self.__id_cache[card_id]

    def get_note_size_bytes(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeBytes:
        with self.__lock:
            cache: dict[NoteId, SizeBytes] = self.__size_bytes_caches[size_type]
            if use_cache and note_id in cache:
                return cache[note_id]
            else:
                if size_type == SizeType.TOTAL:
                    size: SizeBytes = SizeBytes(self.get_note_size_bytes(note_id, SizeType.TEXTS, use_cache) +
                                                self.get_note_size_bytes(note_id, SizeType.FILES, use_cache))
                if size_type == SizeType.TEXTS:
                    size: SizeBytes = self.__size_calculator.calculate_texts_size(self.__col.get_note(note_id))
                    self.__update_total_texts_size(cache[note_id] if note_id in cache else 0, size)
                if size_type == SizeType.FILES:
                    size: SizeBytes = self.__size_calculator.calculate_files_size(self.__col.get_note(note_id),
                                                                                  use_cache)
                cache[note_id] = size
                return cache[note_id]

    def get_note_size_str(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeStr:
        with self.__lock:
            cache: dict[NoteId, SizeStr] = self.__size_str_caches[size_type]
            if use_cache and note_id in cache:
                return cache[note_id]
            else:
                size: SizeBytes = self.get_note_size_bytes(note_id, size_type, use_cache)
                cache[note_id] = SizeFormatter.bytes_to_str(size)
                return cache[note_id]

    def get_total_texts_size(self) -> SizeBytes:
        with self.__lock:
            return self.__total_texts_size

    def refresh_note(self, note_id: NoteId):
        for size_type in size_types:
            self.get_note_size_str(note_id, size_type, use_cache=False)

    def evict_note(self, note_id: NoteId):
        with self.__lock:
            old_size: SizeBytes = self.__size_bytes_caches[SizeType.TEXTS][note_id]
            self.__update_total_texts_size(old_size, SizeBytes(0))
            for cache in self.__size_bytes_caches.values():
                if note_id in cache:
                    del cache[note_id]
            for cache in self.__size_str_caches.values():
                if note_id in cache:
                    del cache[note_id]
            for cid, nid in self.__id_cache.items():
                if nid == note_id and note_id in self.__id_cache:
                    del self.__id_cache[cid]

    def __update_total_texts_size(self, old_size: SizeBytes, new_size: SizeBytes) -> None:
        self.__total_texts_size = SizeBytes(self.__total_texts_size - old_size + new_size)
