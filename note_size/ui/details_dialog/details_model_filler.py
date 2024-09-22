import logging
from logging import Logger

from anki.notes import Note

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

    def __total_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_total_size(note, use_cache=False)
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Total note size: {size}"

    def __texts_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_texts_size(note, use_cache=False)
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Texts size: {size}"

    def __files_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__size_calculator.calculate_note_files_size(note, use_cache=False)
        size: SizeStr = self.__size_formatter.bytes_to_str(size_bytes)
        return f"Files size: {size}"

    def __file_sizes(self, note: Note) -> dict[MediaFile, SizeBytes]:
        return self.__size_calculator.calculate_note_file_sizes(note, use_cache=False)
