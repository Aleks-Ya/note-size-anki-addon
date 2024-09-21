import logging
from datetime import datetime
from logging import Logger
from typing import Sequence

from anki.notes import Note, NoteId

from .details_model import DetailsModel
from ...calculator.size_calculator import SizeCalculator
from ...calculator.size_formatter import SizeFormatter
from ...types import SizeStr, SizeBytes, MediaFile

log: Logger = logging.getLogger(__name__)


class DetailsModelFiller:

    def __init__(self, size_calculator: SizeCalculator, size_formatter: SizeFormatter):
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter

    def prepare_note_model(self, note: Note) -> DetailsModel:
        model: DetailsModel = DetailsModel()
        model.total_note_size_text = self.__total_note_size(note)
        model.texts_note_size_text = self.__texts_note_size(note)
        model.files_note_size_text = self.__files_note_size(note)
        model.file_sizes = self.__file_sizes(note)
        return model

    def prepare_notes_model(self, note_ids: Sequence[NoteId]) -> DetailsModel:
        start_time: datetime = datetime.now()
        model: DetailsModel = DetailsModel()
        model.total_note_size_text = self.__total_notes_size(note_ids)
        model.texts_note_size_text = self.__texts_notes_size(note_ids)
        model.files_note_size_text = self.__files_notes_size(note_ids)
        model.file_sizes = self.__size_calculator.get_notes_file_sizes(note_ids, use_cache=True)
        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Model preparation duration sec: {duration_sec}")
        return model

    def __total_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_total_size(note, use_cache=False)
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Total note size: {size}"

    def __total_notes_size(self, note_ids: Sequence[NoteId]) -> str:
        size_bytes: SizeBytes = self.__size_calculator.get_notes_total_size(note_ids, use_cache=True)
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Total size of {len(note_ids)} notes: {size}"

    def __texts_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_texts_size(note, use_cache=False)
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Texts size: {size}"

    def __texts_notes_size(self, note_ids: Sequence[NoteId]) -> str:
        size_bytes: SizeBytes = self.__size_calculator.get_notes_texts_size(note_ids, use_cache=True)
        size_str: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Texts size of {len(note_ids)} notes: {size_str}"

    def __files_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_files_size(note, use_cache=False)
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Files size: {size}"

    def __files_notes_size(self, note_ids: Sequence[NoteId]) -> str:
        files_number: int = len(self.__size_calculator.get_notes_files(note_ids, use_cache=True))
        size_bytes: SizeBytes = self.__size_calculator.get_notes_files_size(note_ids, use_cache=True)
        size_str: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Size of {files_number} files in {len(note_ids)} notes: {size_str}"

    def __file_sizes(self, note: Note) -> dict[MediaFile, SizeBytes]:
        return self.__size_calculator.calculate_note_file_sizes(note, use_cache=False)
