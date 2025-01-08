import logging
from logging import Logger

from anki.collection import Collection
from anki.notes import NoteId

from ..types import SizeBytes, MediaFile, FilesNumber, NotesNumber
from ..calculator.size_calculator import SizeCalculator

log: Logger = logging.getLogger(__name__)


class UsedFilesCalculator:

    def __init__(self, col: Collection, size_calculator: SizeCalculator) -> None:
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_used_files_size(self, use_cache: bool) -> (SizeBytes, FilesNumber, NotesNumber):
        note_ids: list[NoteId] = self.__col.db.list("select id from notes")
        files: set[MediaFile] = self.__size_calculator.get_notes_files(note_ids, use_cache)
        files_size: SizeBytes = self.__size_calculator.calculate_size_of_files(files, use_cache)
        return files_size, FilesNumber(len(files)), NotesNumber(len(note_ids))
