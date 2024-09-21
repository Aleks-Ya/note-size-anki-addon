import logging
from logging import Logger
from typing import Any, Sequence

from anki.collection import Collection
from anki.notes import Note, NoteId

from .note_helper import NoteHelper
from ..cache.cache import Cache
from ..cache.media_cache import MediaCache
from ..types import SizeBytes, MediaFile

log: Logger = logging.getLogger(__name__)


class SizeCalculator(Cache):

    def __init__(self, col: Collection, media_cache: MediaCache):
        super().__init__()
        self.__col: Collection = col
        self.__note_total_size_cache: dict[NoteId, SizeBytes] = {}
        self.__note_texts_size_cache: dict[NoteId, SizeBytes] = {}
        self.__note_files_size_cache: dict[NoteId, SizeBytes] = {}
        self.__note_files_cache: dict[NoteId, set[MediaFile]] = {}
        self.__note_file_sizes_cache: dict[NoteId, dict[MediaFile, SizeBytes]] = {}
        self.__media_cache: MediaCache = media_cache
        log.debug(f"{self.__class__.__name__} was instantiated")

    def cache_id(self) -> str:
        return "size_calculator"

    def calculate_note_total_size(self, note: Note, use_cache: bool) -> SizeBytes:
        with self._lock:
            if NoteHelper.is_note_saved(note) and use_cache and note.id in self.__note_total_size_cache:
                return self.__note_total_size_cache[note.id]
            else:
                size: SizeBytes = SizeBytes(
                    self.calculate_note_texts_size(note, use_cache) + self.calculate_note_files_size(note, use_cache))
                self.__note_total_size_cache[note.id] = size
                return size

    def get_note_total_size(self, note_id: NoteId, use_cache: bool) -> SizeBytes:
        with self._lock:
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in self.__note_total_size_cache:
                return self.__note_total_size_cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_total_size(note, use_cache)

    def calculate_note_texts_size(self, note: Note, use_cache: bool) -> SizeBytes:
        with self._lock:
            if NoteHelper.is_note_saved(note) and use_cache and note.id in self.__note_texts_size_cache:
                return self.__note_texts_size_cache[note.id]
            else:
                size: SizeBytes = SizeBytes(sum([len(field.encode()) for field in note.fields]))
                self.__note_texts_size_cache[note.id] = size
                return size

    def get_note_texts_size(self, note_id: NoteId, use_cache: bool) -> SizeBytes:
        with self._lock:
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in self.__note_texts_size_cache:
                return self.__note_texts_size_cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_texts_size(note, use_cache)

    def calculate_note_files_size(self, note: Note, use_cache: bool) -> SizeBytes:
        with self._lock:
            if NoteHelper.is_note_saved(note) and use_cache and note.id in self.__note_files_size_cache:
                return self.__note_files_size_cache[note.id]
            else:
                size: SizeBytes = SizeBytes(
                    sum([size for size in self.calculate_note_file_sizes(note, use_cache).values()]))
                self.__note_files_size_cache[note.id] = size
                return size

    def get_note_files_size(self, note_id: NoteId, use_cache: bool) -> SizeBytes:
        with self._lock:
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in self.__note_files_size_cache:
                return self.__note_files_size_cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_files_size(note, use_cache)

    def calculate_note_file_sizes(self, note: Note, use_cache: bool) -> dict[MediaFile, SizeBytes]:
        with self._lock:
            if NoteHelper.is_note_saved(note) and use_cache and note.id in self.__note_file_sizes_cache:
                return self.__note_file_sizes_cache[note.id]
            else:
                file_sizes: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
                for file in self.calculate_note_files(note, use_cache):
                    size: SizeBytes = self.__media_cache.get_file_size(file, use_cache)
                    file_sizes[file] = size
                self.__note_file_sizes_cache[note.id] = file_sizes
                return file_sizes

    def get_note_file_sizes(self, note_id: NoteId, use_cache: bool) -> dict[MediaFile, SizeBytes]:
        with self._lock:
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in self.__note_file_sizes_cache:
                return self.__note_file_sizes_cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_file_sizes(note, use_cache)

    def calculate_note_files(self, note: Note, use_cache: bool) -> set[MediaFile]:
        with self._lock:
            if NoteHelper.is_note_saved(note) and use_cache and note.id in self.__note_files_cache:
                return self.__note_files_cache[note.id]
            else:
                all_files: set[MediaFile] = set[MediaFile]()
                for field in note.fields:
                    files: list[MediaFile] = self.__col.media.files_in_str(note.mid, field)
                    all_files.update(files)
                self.__note_files_cache[note.id] = all_files
                return all_files

    def get_note_files(self, note_id: NoteId, use_cache: bool) -> set[MediaFile]:
        with self._lock:
            if NoteHelper.is_note_id_saved(note_id) and use_cache and note_id in self.__note_files_cache:
                return self.__note_files_cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                return self.calculate_note_files(note, use_cache)

    def calculate_size_of_files(self, files: set[MediaFile], use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([self.__media_cache.get_file_size(file, use_cache) for file in files]))

    def get_notes_total_size(self, note_ids: Sequence[NoteId], use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([self.get_note_total_size(note_id, use_cache) for note_id in note_ids]))

    def get_notes_texts_size(self, note_ids: Sequence[NoteId], use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([self.get_note_texts_size(note_id, use_cache) for note_id in note_ids]))

    def get_notes_files_size(self, note_ids: Sequence[NoteId], use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([size for size in self.get_notes_file_sizes(note_ids, use_cache).values()]))

    def get_notes_file_sizes(self, note_ids: Sequence[NoteId], use_cache: bool) -> dict[MediaFile, SizeBytes]:
        file_sizes: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
        for note_id in note_ids:
            note_file_sizes: dict[MediaFile, SizeBytes] = self.get_note_file_sizes(note_id, use_cache)
            file_sizes.update(note_file_sizes)
        return file_sizes

    def get_notes_files(self, note_ids: Sequence[NoteId], use_cache: bool) -> list[MediaFile]:
        notes_files: set[MediaFile] = set()
        for note_id in note_ids:
            notes_files.update(self.get_note_files(note_id, use_cache))
        return list(notes_files)

    def evict_note(self, note_id: NoteId) -> None:
        with self._lock:
            if note_id in self.__note_total_size_cache:
                del self.__note_total_size_cache[note_id]
            if note_id in self.__note_texts_size_cache:
                del self.__note_texts_size_cache[note_id]
            if note_id in self.__note_files_size_cache:
                del self.__note_files_size_cache[note_id]
            if note_id in self.__note_files_cache:
                del self.__note_files_cache[note_id]
            if note_id in self.__note_file_sizes_cache:
                del self.__note_file_sizes_cache[note_id]

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__note_total_size_cache.clear()
            self.__note_texts_size_cache.clear()
            self.__note_files_size_cache.clear()
            self.__note_files_cache.clear()
            self.__note_file_sizes_cache.clear()

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__note_total_size_cache, self.__note_texts_size_cache, self.__note_files_size_cache,
                self.__note_files_cache, self.__note_file_sizes_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]):
        with self._lock:
            self.__note_total_size_cache = caches[0]
            self.__note_texts_size_cache = caches[1]
            self.__note_files_size_cache = caches[2]
            self.__note_files_cache = caches[3]
            self.__note_file_sizes_cache = caches[4]
            log.info(f"Caches were read dict list")
