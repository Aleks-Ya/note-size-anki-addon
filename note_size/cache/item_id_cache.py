import logging
from logging import Logger
from typing import Sequence, Any

from anki.collection import Collection
from anki.notes import NoteId
from anki.cards import CardId

from .cache import Cache
from .media_cache import MediaCache
from ..types import SizeStr, SizeBytes, SizeType, MediaFile, FilesNumber
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class _Caches:
    id_cache: dict[CardId, NoteId] = {}
    size_str_caches: dict[SizeType, dict[NoteId, SizeStr]] = {}
    file_note_ids_cache: dict[MediaFile, set[NoteId]] = {}


class ItemIdCache(Cache):

    def __init__(self, col: Collection, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                 media_cache: MediaCache) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__caches: _Caches = _Caches()
        self.__media_cache: MediaCache = media_cache
        self.invalidate_cache()
        self.__initialized: bool = False
        log.debug(f"{self.__class__.__name__} was instantiated")

    def cache_id(self) -> str:
        return "item_id_cache"

    def get_note_id_by_card_id(self, card_id: CardId) -> NoteId:
        with self._lock:
            if card_id not in self.__caches.id_cache:
                self.__caches.id_cache[card_id] = self.__col.get_card(card_id).nid
            return self.__caches.id_cache[card_id]

    def get_note_ids_by_card_ids(self, card_ids: Sequence[CardId]) -> Sequence[NoteId]:
        return list({self.get_note_id_by_card_id(card_id) for card_id in card_ids})

    def get_notes_size_str(self, note_ids: Sequence[NoteId], size_type: SizeType, use_cache: bool) -> SizeStr:
        return self.__size_formatter.bytes_to_str(self.__size_calculator.get_notes_size(note_ids, size_type, use_cache))

    def get_note_size_str(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeStr:
        with self._lock:
            cache: dict[NoteId, SizeStr] = self.__caches.size_str_caches[size_type]
            if use_cache and note_id in cache:
                return cache[note_id]
            else:
                size: SizeBytes = self.__size_calculator.get_note_size(note_id, size_type, use_cache)
                cache[note_id] = self.__size_formatter.bytes_to_str(size)
                return cache[note_id]

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for cache in self.__caches.size_str_caches.values():
                if note_id in cache:
                    del cache[note_id]
            for cid, nid in list(self.__caches.id_cache.items()):
                if nid == note_id and note_id in self.__caches.id_cache:
                    del self.__caches.id_cache[cid]
            self.__size_calculator.evict_note(note_id)

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__caches.id_cache, self.__caches.size_str_caches, self.__caches.file_note_ids_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]) -> None:
        with self._lock:
            self.__caches.id_cache = caches[0]
            self.__caches.size_str_caches = caches[1]
            self.__caches.file_note_ids_cache = caches[2]
            log.info(f"Caches were read dict list")

    def get_used_files_size(self, use_cache: bool) -> (SizeBytes, FilesNumber):
        note_ids: Sequence[NoteId] = self.__col.find_notes("deck:*")
        files: set[MediaFile] = self.__size_calculator.get_notes_files(note_ids, use_cache)
        files_size: SizeBytes = self.__size_calculator.calculate_size_of_files(files, use_cache)
        return files_size, FilesNumber(len(files))

    def __size_str_cache_lengths(self) -> str:
        return str([f"{cache[0]}={len(cache[1].keys())}" for cache in self.__caches.size_str_caches.items()])

    def get_size(self) -> str:
        return (f"size_str_cache_lengths={self.__size_str_cache_lengths()}, "
                f"id_cache_length={len(self.__caches.id_cache.keys())}, "
                f"file_note_ids_cache={len(self.__caches.file_note_ids_cache.keys())}")

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__caches.id_cache.clear()
            self.__caches.size_str_caches = {SizeType.TOTAL: {}, SizeType.TEXTS: {}, SizeType.FILES: {}}
            self.__caches.file_note_ids_cache.clear()

    def refresh_notes_having_updated_files(self) -> None:
        if self.is_initialized():
            log.debug("Refreshing notes having updated files started")
            updated_files: set[MediaFile] = self.__media_cache.get_updated_files()
            counter: int = 0
            for updated_file in updated_files:
                updated_note_ids: set[NoteId] = self.__note_ids_by_file(updated_file)
                for note_id in updated_note_ids:
                    self.evict_note(note_id)
                    counter += 1
            log.debug(f"Refreshing notes having updated files finished: "
                      f"refreshed {counter} notes with {len(updated_files)} files")
        else:
            log.debug("Skip refreshing notes having updated files because ItemIdCache is not initialized")

    def __note_ids_by_file(self, file: MediaFile, use_cache: bool = True) -> set[NoteId]:
        with self._lock:
            if use_cache and file in self.__caches.file_note_ids_cache:
                return self.__caches.file_note_ids_cache[file]
            else:
                note_ids: Sequence[NoteId] = self.__col.find_notes("deck:*")
                for note_id in note_ids:
                    files: set[MediaFile] = self.__size_calculator.get_note_files(note_id, use_cache)
                    for file in files:
                        if file in self.__caches.file_note_ids_cache:
                            self.__caches.file_note_ids_cache[file].add(note_id)
                        else:
                            self.__caches.file_note_ids_cache[file] = {note_id}
            return self.__caches.file_note_ids_cache[file]
