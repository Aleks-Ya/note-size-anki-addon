import logging
from logging import Logger

from anki.collection import Collection
from anki.notes import NoteId

from ..cache.media_cache import MediaCache
from ..types import SizeBytes, MediaFile, FilesNumber, NotesNumber
from ..calculator.size_calculator import SizeCalculator

log: Logger = logging.getLogger(__name__)


class UsedFiles:
    def __init__(self, used_files_size: SizeBytes, used_files_number: FilesNumber, missing_files_number: FilesNumber,
                 used_notes_numbers: NotesNumber) -> None:
        self.used_files_size: SizeBytes = used_files_size
        self.used_files_number: FilesNumber = used_files_number
        self.missing_files_number: FilesNumber = missing_files_number
        self.used_notes_numbers: NotesNumber = used_notes_numbers

    def __eq__(self, __value):
        return self.__dict__ == __value.__dict__


class UsedFilesCalculator:

    def __init__(self, col: Collection, size_calculator: SizeCalculator, media_cache: MediaCache) -> None:
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        self.__media_cache: MediaCache = media_cache
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_used_files_size(self, use_cache: bool) -> UsedFiles:
        note_ids: list[NoteId] = self.__col.db.list("select id from notes")
        files: set[MediaFile] = self.__size_calculator.get_notes_files(note_ids, use_cache)
        missing_files_number: FilesNumber = self.__media_cache.get_missing_files_number(files, use_cache)
        files_size: SizeBytes = self.__size_calculator.calculate_size_of_files(files, use_cache)
        return UsedFiles(files_size, FilesNumber(len(files)), missing_files_number, NotesNumber(len(note_ids)))
