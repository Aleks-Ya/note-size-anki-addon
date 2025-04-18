import logging
from logging import Logger
from typing import Sequence, Any

from anki.notes import NoteId

from .cache import Cache
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter
from ..common.types import SizeStr, SizeBytes, SizeType, SignificantDigits

log: Logger = logging.getLogger(__name__)


class SizeStrCache(Cache):

    def __init__(self, size_calculator: SizeCalculator, size_formatter: SizeFormatter) -> None:
        super().__init__()
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__size_str_caches: dict[SizeType, dict[NoteId, dict[SignificantDigits, SizeStr]]] = {}
        self.invalidate_cache()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_notes_size_str(self, note_ids: Sequence[NoteId], size_type: SizeType, significant_digits: SignificantDigits,
                           use_cache: bool, ) -> SizeStr:
        with self._lock:
            size: SizeBytes = self.__size_calculator.get_notes_size(note_ids, size_type, use_cache)
            return self.__size_formatter.bytes_to_str(size, significant_digits)

    def get_note_size_str(self, note_id: NoteId, size_type: SizeType, significant_digits: SignificantDigits,
                          use_cache: bool) -> SizeStr:
        with self._lock:
            cache: dict[NoteId, dict[SignificantDigits, SizeStr]] = self.__size_str_caches[size_type]
            if use_cache and note_id in cache and significant_digits in cache[note_id]:
                return cache[note_id][significant_digits]
            else:
                size: SizeBytes = self.__size_calculator.get_note_size(note_id, size_type, use_cache)
                if note_id not in cache:
                    cache[note_id] = {}
                cache[note_id][significant_digits] = self.__size_formatter.bytes_to_str(size, significant_digits)
                return cache[note_id][significant_digits]

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for cache in self.__size_str_caches.values():
                if note_id in cache:
                    del cache[note_id]

    def as_dict_list(self) -> list[dict[Any, Any]]:
        with self._lock:
            return [self.__size_str_caches]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]) -> None:
        with self._lock:
            self.__size_str_caches = caches[0]
            log.info("Cache was read from dict list")

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__size_str_caches = {SizeType.TOTAL: {}, SizeType.TEXTS: {}, SizeType.FILES: {}}

    def get_cache_size(self) -> int:
        with self._lock:
            size: int = 0
            for cache in self.__size_str_caches.values():
                size += len(cache.keys())
            return size

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
