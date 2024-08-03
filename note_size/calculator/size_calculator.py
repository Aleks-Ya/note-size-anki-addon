import logging
from logging import Logger

from anki.notes import Note

from ..cache.media_cache import MediaCache
from ..types import SizeBytes, MediaFile

log: Logger = logging.getLogger(__name__)


class SizeCalculator:

    def __init__(self, media_cache: MediaCache):
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
        for file in self.note_files(note):
            size: SizeBytes = self.__media_cache.get_file_size(file, use_cache=use_cache)
            file_sizes[file] = size
        return file_sizes

    @staticmethod
    def note_files(note: Note) -> list[MediaFile]:
        all_files: list[MediaFile] = list[MediaFile]()
        for field in note.fields:
            files: list[MediaFile] = note.col.media.files_in_str(note.mid, field)
            all_files += files
        return all_files

    @staticmethod
    def sort_by_size_desc(file_sizes: dict[MediaFile, SizeBytes]) -> dict[MediaFile, SizeBytes]:
        return dict(sorted(file_sizes.items(), key=lambda item: item[1], reverse=True))
