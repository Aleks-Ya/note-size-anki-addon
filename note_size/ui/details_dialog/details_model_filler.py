import logging
from datetime import datetime
from logging import Logger
from typing import Sequence

from anki.notes import Note, NoteId

from .details_model import DetailsModel
from ...core.common.number_formatter import NumberFormatter
from ...cache.media_cache import MediaCache
from ...cache.bytes_note_size_cache import BytesNoteSizeCache
from ...cache.bytes_size_cache import BytesSizeCache
from ...config.config import Config
from ...core.common.types import SizeStr, SizeBytes, MediaFile, SizeType, FileSize, SignificantDigits

log: Logger = logging.getLogger(__name__)


class DetailsModelFiller:

    def __init__(self, bytes_note_size_cache: BytesNoteSizeCache, bytes_size_cache: BytesSizeCache, media_cache: MediaCache,
                 config: Config):
        self.__bytes_note_size_cache: BytesNoteSizeCache = bytes_note_size_cache
        self.__bytes_size_cache: BytesSizeCache = bytes_size_cache
        self.__media_cache: MediaCache = media_cache
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

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
        model.file_sizes = self.__bytes_note_size_cache.get_notes_file_sizes(note_ids, use_cache=True)
        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Model preparation duration sec: {duration_sec}")
        return model

    def __total_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__bytes_note_size_cache.calculate_note_size(note, SizeType.TOTAL, use_cache=False)
        significant_digits: SignificantDigits = self.__config.get_browser_significant_digits()
        size: SizeStr = self.__bytes_size_cache.bytes_to_str(size_bytes, significant_digits)
        return f"Total note size: {size}"

    def __total_notes_size(self, note_ids: Sequence[NoteId]) -> str:
        size_bytes: SizeBytes = self.__bytes_note_size_cache.get_notes_size(note_ids, SizeType.TOTAL, use_cache=True)
        significant_digits: SignificantDigits = self.__config.get_browser_significant_digits()
        size: SizeStr = self.__bytes_size_cache.bytes_to_str(size_bytes, significant_digits)
        note_number_str: str = NumberFormatter.with_thousands_separator(len(note_ids))
        return f"Total size of {note_number_str} notes: {size}"

    def __texts_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__bytes_note_size_cache.calculate_note_size(note, SizeType.TEXTS, use_cache=False)
        significant_digits: SignificantDigits = self.__config.get_browser_significant_digits()
        size: SizeStr = self.__bytes_size_cache.bytes_to_str(size_bytes, significant_digits)
        return f"Texts size: {size}"

    def __texts_notes_size(self, note_ids: Sequence[NoteId]) -> str:
        size_bytes: SizeBytes = self.__bytes_note_size_cache.get_notes_size(note_ids, SizeType.TEXTS, use_cache=True)
        significant_digits: SignificantDigits = self.__config.get_browser_significant_digits()
        size_str: SizeStr = self.__bytes_size_cache.bytes_to_str(size_bytes, significant_digits)
        note_number_str: str = NumberFormatter.with_thousands_separator(len(note_ids))
        return f"Texts size of {note_number_str} notes: {size_str}"

    def __files_note_size(self, note: Note) -> str:
        size_bytes: SizeBytes = self.__bytes_note_size_cache.calculate_note_size(note, SizeType.FILES, use_cache=False)
        significant_digits: SignificantDigits = self.__config.get_browser_significant_digits()
        size: SizeStr = self.__bytes_size_cache.bytes_to_str(size_bytes, significant_digits)
        files: set[MediaFile] = self.__bytes_note_size_cache.calculate_note_files(note, use_cache=False)
        files_number_str: str = NumberFormatter.with_thousands_separator(len(files))
        exist_files_number, missing_files_number = self.__media_cache.get_missing_files_number(files, use_cache=True)
        existing_files_number_str: str = NumberFormatter.with_thousands_separator(exist_files_number)
        missing_files_number_str: str = NumberFormatter.with_thousands_separator(missing_files_number)
        return (f"Size of {files_number_str} files "
                f"({existing_files_number_str} existing and {missing_files_number_str} missing): {size}")

    def __files_notes_size(self, note_ids: Sequence[NoteId]) -> str:
        files: set[MediaFile] = self.__bytes_note_size_cache.get_notes_files(note_ids, use_cache=True)
        files_number_str: str = NumberFormatter.with_thousands_separator(len(files))
        size_bytes: SizeBytes = self.__bytes_note_size_cache.get_notes_size(note_ids, SizeType.FILES, use_cache=True)
        significant_digits: SignificantDigits = self.__config.get_browser_significant_digits()
        size_str: SizeStr = self.__bytes_size_cache.bytes_to_str(size_bytes, significant_digits)
        note_number_str: str = NumberFormatter.with_thousands_separator(len(note_ids))
        exist_files_number, missing_files_number = self.__media_cache.get_missing_files_number(files, use_cache=True)
        existing_files_number_str: str = NumberFormatter.with_thousands_separator(exist_files_number)
        missing_files_number_str: str = NumberFormatter.with_thousands_separator(missing_files_number)
        return (f"Size of {files_number_str} files "
                f"({existing_files_number_str} existing and {missing_files_number_str} missing) "
                f"in {note_number_str} notes: {size_str}")

    def __file_sizes(self, note: Note) -> dict[MediaFile, FileSize]:
        return self.__bytes_note_size_cache.calculate_note_file_sizes(note, use_cache=False)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
