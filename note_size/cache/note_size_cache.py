import logging
from logging import Logger
from typing import Sequence, Any

from anki.notes import NoteId

from .cache import Cache
from ..calculator.bytes_note_size_cache import BytesNoteSizeCache
from .bytes_size_cache import BytesSizeCache
from ..common.types import SizeStr, SizeBytes, SizeType, SignificantDigits

log: Logger = logging.getLogger(__name__)


class NoteSizeCache(Cache):

    def __init__(self, bytes_note_size_cache: BytesNoteSizeCache, bytes_size_cache: BytesSizeCache) -> None:
        super().__init__()
        self.__bytes_note_size_cache: BytesNoteSizeCache = bytes_note_size_cache
        self.__bytes_size_cache: BytesSizeCache = bytes_size_cache
        self.__note_size_caches: dict[SizeType, dict[NoteId, dict[SignificantDigits, SizeStr]]] = {}
        self.invalidate_cache()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_notes_size_str(self, note_ids: Sequence[NoteId], size_type: SizeType, significant_digits: SignificantDigits,
                           use_cache: bool, ) -> SizeStr:
        with self._lock:
            size: SizeBytes = self.__bytes_note_size_cache.get_notes_size(note_ids, size_type, use_cache)
            return self.__bytes_size_cache.bytes_to_str(size, significant_digits)

    def get_note_size_str(self, note_id: NoteId, size_type: SizeType, significant_digits: SignificantDigits,
                          use_cache: bool) -> SizeStr:
        with self._lock:
            cache: dict[NoteId, dict[SignificantDigits, SizeStr]] = self.__note_size_caches[size_type]
            if use_cache and note_id in cache and significant_digits in cache[note_id]:
                return cache[note_id][significant_digits]
            else:
                size: SizeBytes = self.__bytes_note_size_cache.get_note_size(note_id, size_type, use_cache)
                if note_id not in cache:
                    cache[note_id] = {}
                cache[note_id][significant_digits] = self.__bytes_size_cache.bytes_to_str(size, significant_digits)
                return cache[note_id][significant_digits]

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for cache in self.__note_size_caches.values():
                if note_id in cache:
                    del cache[note_id]

    def as_dict_list(self) -> list[dict[Any, Any]]:
        with self._lock:
            return [self.__note_size_caches]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]) -> None:
        with self._lock:
            self.__note_size_caches = caches[0]
            log.info("Cache was read from dict list")

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__note_size_caches = {SizeType.TOTAL: {}, SizeType.TEXTS: {}, SizeType.FILES: {}}

    def get_cache_size(self) -> int:
        with self._lock:
            size: int = 0
            for cache in self.__note_size_caches.values():
                size += len(cache.keys())
            return size

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
