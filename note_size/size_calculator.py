import logging
import os
from logging import Logger
from typing import NewType

from anki.notes import Note

log: Logger = logging.getLogger(__name__)

SizeBytes = NewType("SizeBytes", int)


class SizeCalculator:

    @staticmethod
    def calculate_note_size(note: Note) -> SizeBytes:
        return SizeBytes(SizeCalculator.total_text_size(note) + SizeCalculator.total_file_size(note))

    @staticmethod
    def total_text_size(note: Note) -> SizeBytes:
        return SizeBytes(sum([len(field) for field in note.fields]))

    @staticmethod
    def total_file_size(note: Note) -> SizeBytes:
        return SizeBytes(sum([size for size in SizeCalculator.file_sizes(note).values()]))

    @staticmethod
    def file_sizes(note: Note) -> dict[str, SizeBytes]:
        all_files: dict[str, SizeBytes] = dict[str, SizeBytes]()
        for field in note.fields:
            files: list[str] = note.col.media.files_in_str(note.mid, field)
            sizes: dict[str, SizeBytes] = {}
            for file in files:
                full_path: str = os.path.join(note.col.media.dir(), file)
                if os.path.exists(full_path):
                    sizes[file] = SizeBytes(os.path.getsize(full_path))
                else:
                    log.warning(f"File absents: {full_path}")
                    sizes[file] = SizeBytes(0)
            all_files.update(sizes)
        return all_files

    @staticmethod
    def sort_by_size_desc(file_sizes: dict[str, SizeBytes]) -> dict[str, SizeBytes]:
        return dict(sorted(file_sizes.items(), key=lambda item: item[1], reverse=True))
