import logging
from logging import Logger
from typing import Sequence, Any

from anki.collection import Collection
from anki.notes import NoteId
from anki.cards import CardId

from .cache import Cache
from .media_cache import MediaCache
from ..types import SizeBytes, MediaFile, FilesNumber
from ..calculator.size_calculator import SizeCalculator

log: Logger = logging.getLogger(__name__)


class _Caches:
    id_cache: dict[CardId, NoteId] = {}
    file_note_ids_cache: dict[MediaFile, set[NoteId]] = {}


class ItemIdCache(Cache):

    def __init__(self, col: Collection, size_calculator: SizeCalculator, media_cache: MediaCache) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        self.__caches: _Caches = _Caches()
        self.__media_cache: MediaCache = media_cache
        self.invalidate_cache()
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

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for cid, nid in list(self.__caches.id_cache.items()):
                if nid == note_id and note_id in self.__caches.id_cache:
                    del self.__caches.id_cache[cid]
            self.__size_calculator.evict_note(note_id)

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__caches.id_cache, self.__caches.file_note_ids_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]) -> None:
        with self._lock:
            self.__caches.id_cache = caches[0]
            self.__caches.file_note_ids_cache = caches[1]
            log.info(f"Caches were read dict list")

    def get_used_files_size(self, use_cache: bool) -> (SizeBytes, FilesNumber):
        note_ids: Sequence[NoteId] = self.__col.find_notes("deck:*")
        files: set[MediaFile] = self.__size_calculator.get_notes_files(note_ids, use_cache)
        files_size: SizeBytes = self.__size_calculator.calculate_size_of_files(files, use_cache)
        return files_size, FilesNumber(len(files))

    def get_size_str(self) -> str:
        return (f"id_cache_length={len(self.__caches.id_cache.keys())}, "
                f"file_note_ids_cache={len(self.__caches.file_note_ids_cache.keys())}")

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__caches.id_cache.clear()
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

    def get_cache_size(self) -> int:
        size: int = 0
        size += len(self.__caches.id_cache.keys())
        size += len(self.__caches.file_note_ids_cache.keys())
        return size

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
