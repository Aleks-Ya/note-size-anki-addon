import logging
from logging import Logger
from typing import Any, Sequence

from anki.collection import Collection
from anki.notes import Note, NoteId

from .note_helper import NoteHelper
from ..cache.cache import Cache
from ..cache.media_cache import MediaCache
from ..types import SizeBytes, MediaFile, SizeType

log: Logger = logging.getLogger(__name__)


class _Caches:
    size_caches: dict[SizeType, dict[NoteId, SizeBytes]] = {}
    note_files_cache: dict[NoteId, set[MediaFile]] = {}
    note_file_sizes_cache: dict[NoteId, dict[MediaFile, SizeBytes]] = {}


class SizeCalculator(Cache):

    def __init__(self, col: Collection, media_cache: MediaCache):
        super().__init__()
        self.__col: Collection = col
        self.__caches: _Caches = _Caches()
        self.__media_cache: MediaCache = media_cache
        self.invalidate_cache()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def cache_id(self) -> str:
        return "size_calculator"

    def calculate_note_size(self, note: Note, size_type: SizeType, use_cache: bool) -> SizeBytes:
        with self._lock:
            cache: dict[NoteId, SizeBytes] = self.__caches.size_caches[size_type]
            if NoteHelper.is_note_saved(note) and use_cache and note.id in cache:
                return cache[note.id]
            else:
                if size_type == SizeType.TOTAL:
                    texts_size: SizeBytes = self.calculate_note_size(note, SizeType.TEXTS, use_cache)
                    files_size: SizeBytes = self.calculate_note_size(note, SizeType.FILES, use_cache)
                    size: SizeBytes = SizeBytes(texts_size + files_size)
                if size_type == SizeType.TEXTS:
                    size: SizeBytes = SizeBytes(sum([len(field.encode()) for field in note.fields]))
                if size_type == SizeType.FILES:
                    size: SizeBytes = SizeBytes(
                        sum([size for size in self.calculate_note_file_sizes(note, use_cache).values()]))
                cache[note.id] = size
                return size

    def get_note_size(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeBytes:
        with self._lock:
            cache: dict[NoteId, SizeBytes] = self.__caches.size_caches[size_type]
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in cache:
                return cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_size(note, size_type, use_cache)

    def calculate_note_file_sizes(self, note: Note, use_cache: bool) -> dict[MediaFile, SizeBytes]:
        with self._lock:
            cache: dict[NoteId, dict[MediaFile, SizeBytes]] = self.__caches.note_file_sizes_cache
            if NoteHelper.is_note_saved(note) and use_cache and note.id in cache:
                return cache[note.id]
            else:
                file_sizes: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
                for file in self.calculate_note_files(note, use_cache):
                    size: SizeBytes = self.__media_cache.get_file_size(file, use_cache)
                    file_sizes[file] = size
                cache[note.id] = file_sizes
                return file_sizes

    def get_note_file_sizes(self, note_id: NoteId, use_cache: bool) -> dict[MediaFile, SizeBytes]:
        with self._lock:
            cache: dict[NoteId, dict[MediaFile, SizeBytes]] = self.__caches.note_file_sizes_cache
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in cache:
                return cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_file_sizes(note, use_cache)

    def calculate_note_files(self, note: Note, use_cache: bool) -> set[MediaFile]:
        with self._lock:
            cache: dict[NoteId, set[MediaFile]] = self.__caches.note_files_cache
            if NoteHelper.is_note_saved(note) and use_cache and note.id in cache:
                return cache[note.id]
            else:
                all_files: set[MediaFile] = set[MediaFile]()
                for field in note.fields:
                    files: list[MediaFile] = self.__col.media.files_in_str(note.mid, field)
                    all_files.update(files)
                cache[note.id] = all_files
                return all_files

    def get_note_files(self, note_id: NoteId, use_cache: bool) -> set[MediaFile]:
        with self._lock:
            cache: dict[NoteId, set[MediaFile]] = self.__caches.note_files_cache
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in cache:
                return cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_files(note, use_cache)

    def calculate_size_of_files(self, files: set[MediaFile], use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([self.__media_cache.get_file_size(file, use_cache) for file in files]))

    def get_notes_size(self, note_ids: Sequence[NoteId], size_type: SizeType, use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([self.get_note_size(note_id, size_type, use_cache) for note_id in note_ids]))

    def get_notes_file_sizes(self, note_ids: Sequence[NoteId], use_cache: bool) -> dict[MediaFile, SizeBytes]:
        file_sizes: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
        for note_id in note_ids:
            note_file_sizes: dict[MediaFile, SizeBytes] = self.get_note_file_sizes(note_id, use_cache)
            file_sizes.update(note_file_sizes)
        return file_sizes

    def get_notes_files(self, note_ids: Sequence[NoteId], use_cache: bool) -> set[MediaFile]:
        notes_files: set[MediaFile] = set()
        for note_id in note_ids:
            notes_files.update(self.get_note_files(note_id, use_cache))
        return notes_files

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            for size_type in SizeType:
                cache: dict[NoteId, SizeBytes] = self.__caches.size_caches[size_type]
                if note_id in cache:
                    del cache[note_id]
            if note_id in self.__caches.note_file_sizes_cache:
                del self.__caches.note_file_sizes_cache[note_id]
            if note_id in self.__caches.note_files_cache:
                del self.__caches.note_files_cache[note_id]

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__caches.size_caches = {SizeType.TOTAL: {}, SizeType.TEXTS: {}, SizeType.FILES: {}}
            self.__caches.note_files_cache.clear()
            self.__caches.note_file_sizes_cache.clear()

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__caches.size_caches, self.__caches.note_files_cache, self.__caches.note_file_sizes_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]):
        with self._lock:
            self.__caches.size_caches = caches[0]
            self.__caches.note_files_cache = caches[1]
            self.__caches.note_file_sizes_cache = caches[2]
            log.info(f"Caches were read dict list")

    def get_cache_size(self) -> int:
        size: int = 0
        for cache in self.__caches.size_caches.values():
            size += len(cache.keys())
        size += len(self.__caches.note_files_cache.keys())
        size += len(self.__caches.note_file_sizes_cache.keys())
        return size
