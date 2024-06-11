import logging
import os
from logging import Logger
from typing import NewType

from anki.notes import Note

log: Logger = logging.getLogger(__name__)

SizeBytes = NewType("SizeBytes", int)
MediaFile = NewType("MediaFile", str)


class SizeCalculator:

    @staticmethod
    def calculate_note_size(note: Note) -> SizeBytes:
        return SizeBytes(SizeCalculator.calculate_texts_size(note) + SizeCalculator.calculate_files_size(note))

    @staticmethod
    def calculate_texts_size(note: Note) -> SizeBytes:
        return SizeBytes(sum([len(field.encode('utf-8')) for field in note.fields]))

    @staticmethod
    def calculate_files_size(note: Note) -> SizeBytes:
        return SizeBytes(sum([size for size in SizeCalculator.file_sizes(note).values()]))

    @staticmethod
    def file_sizes(note: Note) -> dict[MediaFile, SizeBytes]:
        all_files: dict[MediaFile, SizeBytes] = dict[MediaFile, SizeBytes]()
        for field in note.fields:
            files: list[str] = note.col.media.files_in_str(note.mid, field)
            sizes: dict[MediaFile, SizeBytes] = {}
            for file in files:
                full_path: str = os.path.join(note.col.media.dir(), file)
                if os.path.exists(full_path):
                    sizes[MediaFile(file)] = SizeBytes(os.path.getsize(full_path))
                else:
                    log.warning(f"File absents: {full_path}")
                    sizes[MediaFile(file)] = SizeBytes(0)
            all_files.update(sizes)
        return all_files

    @staticmethod
    def sort_by_size_desc(file_sizes: dict[MediaFile, SizeBytes]) -> dict[MediaFile, SizeBytes]:
        return dict(sorted(file_sizes.items(), key=lambda item: item[1], reverse=True))
