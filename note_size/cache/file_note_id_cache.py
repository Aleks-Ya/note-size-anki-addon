import logging
from logging import Logger
from typing import Sequence, Any

from anki.collection import Collection
from anki.notes import NoteId

from .cache import Cache
from .media_cache import MediaCache
from ..types import SizeBytes, MediaFile, FilesNumber
from ..calculator.size_calculator import SizeCalculator

log: Logger = logging.getLogger(__name__)


class FileNoteIdCache(Cache):

    def __init__(self, col: Collection, size_calculator: SizeCalculator, media_cache: MediaCache) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        self.__file_note_ids_cache: dict[MediaFile, set[NoteId]] = {}
        self.__media_cache: MediaCache = media_cache
        self.invalidate_cache()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def cache_id(self) -> str:
        return "item_id_cache"

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for media_file in self.__file_note_ids_cache.keys():
                if note_id in self.__file_note_ids_cache[media_file]:
                    self.__file_note_ids_cache[media_file].remove(note_id)
            self.__size_calculator.evict_note(note_id)

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__file_note_ids_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]) -> None:
        with self._lock:
            self.__file_note_ids_cache = caches[0]
            log.info(f"Caches were read dict list")

    def get_used_files_size(self, use_cache: bool) -> (SizeBytes, FilesNumber):
        note_ids: Sequence[NoteId] = self.__col.find_notes("deck:*")
        files: set[MediaFile] = self.__size_calculator.get_notes_files(note_ids, use_cache)
        files_size: SizeBytes = self.__size_calculator.calculate_size_of_files(files, use_cache)
        return files_size, FilesNumber(len(files))

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__file_note_ids_cache.clear()

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
