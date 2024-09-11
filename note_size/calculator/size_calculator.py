import logging
from logging import Logger
from typing import Any

from anki.collection import Collection
from anki.notes import Note, NoteId

from ..cache.cache import Cache
from ..cache.media_cache import MediaCache
from ..types import SizeBytes, MediaFile

log: Logger = logging.getLogger(__name__)


class SizeCalculator(Cache):

    def __init__(self, col: Collection, media_cache: MediaCache):
        super().__init__()
        self.__col: Collection = col
        self.__note_files_cache: dict[NoteId, list[MediaFile]] = {}
        self.__media_cache: MediaCache = media_cache
        log.debug(f"{self.__class__.__name__} was instantiated")

    def cache_id(self) -> str:
        return "size_calculator"

    def calculate_note_total_size(self, note: Note, use_cache: bool) -> SizeBytes:
        return SizeBytes(
            SizeCalculator.calculate_note_texts_size(note) + self.calculate_note_files_size(note, use_cache))

    @staticmethod
    def calculate_note_texts_size(note: Note) -> SizeBytes:
        return SizeBytes(sum([len(field.encode()) for field in note.fields]))

    def calculate_note_files_size(self, note: Note, use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([size for size in self.note_file_sizes(note, use_cache).values()]))

    def note_file_sizes(self, note: Note, use_cache: bool) -> dict[MediaFile, SizeBytes]:
        file_sizes: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
        for file in self.note_files(note, use_cache):
            size: SizeBytes = self.__media_cache.get_file_size(file, use_cache)
            file_sizes[file] = size
        return file_sizes

    def note_files(self, note: Note, use_cache: bool) -> list[MediaFile]:
        with self._lock:
            if use_cache and note.id in self.__note_files_cache:
                return self.__note_files_cache[note.id]
            else:
                all_files: list[MediaFile] = list[MediaFile]()
                for field in note.fields:
                    files: list[MediaFile] = self.__col.media.files_in_str(note.mid, field)
                    all_files += files
                self.__note_files_cache[note.id] = all_files
                return all_files

    def calculate_size_of_files(self, files: set[MediaFile], use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([self.__media_cache.get_file_size(file, use_cache) for file in files]))

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            if note_id in self.__note_files_cache:
                del self.__note_files_cache[note_id]

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__note_files_cache.clear()

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__note_files_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]):
        with self._lock:
            self.__note_files_cache = caches[0]
            log.info(f"Caches were read dict list")
