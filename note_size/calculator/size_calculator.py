import logging
from logging import Logger

from anki.notes import Note

from ..cache.media_cache import MediaCache
from ..types import SizeBytes, MediaFile

log: Logger = logging.getLogger(__name__)


class SizeCalculator:

    def __init__(self, media_cache: MediaCache):
        self.media_cache: MediaCache = media_cache

    def calculate_note_size(self, note: Note) -> SizeBytes:
        return SizeBytes(SizeCalculator.calculate_texts_size(note) + self.calculate_files_size(note))

    @staticmethod
    def calculate_texts_size(note: Note) -> SizeBytes:
        return SizeBytes(sum([len(field.encode('utf-8')) for field in note.fields]))

    def calculate_files_size(self, note: Note) -> SizeBytes:
        return SizeBytes(sum([size for size in self.file_sizes(note).values()]))

    def file_sizes(self, note: Note) -> dict[MediaFile, SizeBytes]:
        all_files: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
        for field in note.fields:
            files: list[str] = note.col.media.files_in_str(note.mid, field)
            sizes: dict[MediaFile, SizeBytes] = {}
            for file in files:
                sizes[MediaFile(file)] = self.media_cache.get_file_size(MediaFile(file), use_cache=True)
            all_files.update(sizes)
        return all_files

    @staticmethod
    def sort_by_size_desc(file_sizes: dict[MediaFile, SizeBytes]) -> dict[MediaFile, SizeBytes]:
        return dict(sorted(file_sizes.items(), key=lambda item: item[1], reverse=True))
