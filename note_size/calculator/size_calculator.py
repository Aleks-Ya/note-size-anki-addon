import logging
from logging import Logger
from threading import RLock

from anki.collection import Collection
from anki.notes import Note, NoteId

from ..cache.media_cache import MediaCache
from ..types import SizeBytes, MediaFile

log: Logger = logging.getLogger(__name__)


class SizeCalculator:

    def __init__(self, col: Collection, media_cache: MediaCache):
        self.__lock: RLock = RLock()
        self.__col: Collection = col
        self.__note_files_cache: dict[NoteId, list[MediaFile]] = {}
        self.__media_cache: MediaCache = media_cache
        log.debug(f"{self.__class__.__name__} was instantiated")

    def calculate_note_size(self, note: Note, use_cache: bool) -> SizeBytes:
        return SizeBytes(SizeCalculator.calculate_texts_size(note) + self.calculate_files_size(note, use_cache))

    @staticmethod
    def calculate_texts_size(note: Note) -> SizeBytes:
        return SizeBytes(sum([len(field.encode()) for field in note.fields]))

    def calculate_files_size(self, note: Note, use_cache: bool) -> SizeBytes:
        return SizeBytes(sum([size for size in self.file_sizes(note, use_cache).values()]))

    def file_sizes(self, note: Note, use_cache: bool) -> dict[MediaFile, SizeBytes]:
        file_sizes: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
        for file in self.note_files(note, use_cache):
            size: SizeBytes = self.__media_cache.get_file_size(file, use_cache)
            file_sizes[file] = size
        return file_sizes

    def note_files(self, note: Note, use_cache: bool) -> list[MediaFile]:
        with self.__lock:
            if use_cache and note.id in self.__note_files_cache:
                return self.__note_files_cache[note.id]
            else:
                all_files: list[MediaFile] = list[MediaFile]()
                for field in note.fields:
                    files: list[MediaFile] = self.__col.media.files_in_str(note.mid, field)
                    all_files += files
                self.__note_files_cache[note.id] = all_files
                return all_files

    def calculate_size_of_files(self, files: set[MediaFile], use_cache: bool):
        return SizeBytes(sum([self.__media_cache.get_file_size(file, use_cache) for file in files]))

    def evict_note(self, note_id: NoteId):
        with self.__lock:
            if note_id in self.__note_files_cache:
                del self.__note_files_cache[note_id]
