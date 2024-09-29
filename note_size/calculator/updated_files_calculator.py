import logging
from logging import Logger
from typing import Sequence, Any

from anki.collection import Collection
from anki.notes import NoteId

from ..cache.cache import Cache
from ..cache.media_cache import MediaCache
from ..types import MediaFile
from ..calculator.size_calculator import SizeCalculator

log: Logger = logging.getLogger(__name__)


class UpdatedFilesCalculator(Cache):

    def __init__(self, col: Collection, size_calculator: SizeCalculator, media_cache: MediaCache) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        self.__file_note_ids_cache: dict[MediaFile, set[NoteId]] = {}
        self.__media_cache: MediaCache = media_cache
        self.invalidate_cache()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for media_file in self.__file_note_ids_cache.keys():
                if note_id in self.__file_note_ids_cache[media_file]:
                    self.__file_note_ids_cache[media_file].remove(note_id)

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__file_note_ids_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]) -> None:
        with self._lock:
            self.__file_note_ids_cache = caches[0]
            log.info(f"Caches were read dict list")

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__file_note_ids_cache.clear()

    def get_notes_having_updated_files(self) -> set[NoteId]:
        updated_note_ids: set[NoteId] = set[NoteId]()
        if self.is_initialized():
            log.debug("Refreshing notes having updated files started")
            updated_files: set[MediaFile] = self.__media_cache.get_updated_files()
            for updated_file in updated_files:
                note_ids: set[NoteId] = self.__note_ids_by_file(updated_file)
                updated_note_ids.update(note_ids)
        else:
            log.debug("Skip refreshing notes having updated files because ItemIdCache is not initialized")
        return updated_note_ids

    def get_cache_size(self) -> int:
        return len(self.__file_note_ids_cache)

    def __note_ids_by_file(self, file: MediaFile, use_cache: bool = True) -> set[NoteId]:
        with self._lock:
            if use_cache and file in self.__file_note_ids_cache:
                return self.__file_note_ids_cache[file]
            else:
                note_ids: Sequence[NoteId] = self.__col.find_notes("deck:*")
                for note_id in note_ids:
                    files: set[MediaFile] = self.__size_calculator.get_note_files(note_id, use_cache)
                    for file in files:
                        if file in self.__file_note_ids_cache:
                            self.__file_note_ids_cache[file].add(note_id)
                        else:
                            self.__file_note_ids_cache[file] = {note_id}
            return self.__file_note_ids_cache[file]
