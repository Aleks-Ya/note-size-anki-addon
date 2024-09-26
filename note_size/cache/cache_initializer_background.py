import logging
from datetime import datetime
from logging import Logger
from typing import Sequence, Optional, Callable

from anki.collection import Collection
from anki.notes import NoteId

from .cache import Cache
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter
from ..types import SizeType, MediaFile
from ..ui.common.number_formatter import NumberFormatter
from ..ui.details_dialog.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheInitializerBackground:

    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache, size_calculator: SizeCalculator,
                 size_formatter: SizeFormatter, file_type_helper: FileTypeHelper,
                 update_progress_callback: Callable[[str, Optional[int], Optional[int]], None],
                 update_progress_step: int = 500):
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__caches: list[Cache] = [self.__media_cache, self.__item_id_cache, self.__size_formatter,
                                      self.__size_calculator, self.__file_type_helper]
        self.__wants_cancel: bool = False
        self.__update_progress_callback: Callable[[str, Optional[int], Optional[int]], None] = update_progress_callback
        self.__update_progress_step: int = update_progress_step
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self, col: Collection) -> int:
        log.info(f"Cache initialization started: {self.__item_id_cache.get_size()}")
        start_time: datetime = datetime.now()
        self.__update_progress("Note Size cache initializing", None, None)

        all_note_ids: Sequence[NoteId] = col.find_notes("deck:*")
        note_number: int = len(all_note_ids)
        note_number_str: str = NumberFormatter.with_thousands_separator(note_number)
        self.__update_progress("Note Size cache initializing", 0, note_number)
        for i, note_id in enumerate(all_note_ids):
            if self.__wants_cancel:
                log.info(f"User cancelled notes cache initialization at {i}")
                return i
            i_str: str = NumberFormatter.with_thousands_separator(i)
            self.__update_progress(f"Caching note sizes: {i_str} of {note_number_str}", i, note_number)
            for size_type in SizeType:
                self.__item_id_cache.get_note_size_str(note_id, size_type, use_cache=True)
                self.__size_calculator.get_note_file_sizes(note_id, use_cache=True)
                note_files: set[MediaFile] = self.__size_calculator.get_note_files(note_id, use_cache=True)
                for note_file in note_files:
                    self.__file_type_helper.get_file_type(note_file, use_cache=True)

        all_card_ids: Sequence[int] = col.find_cards("deck:*")
        card_number: int = len(all_card_ids)
        card_number_str: str = NumberFormatter.with_thousands_separator(card_number)
        for i, card_id in enumerate(all_card_ids):
            if self.__wants_cancel:
                log.info(f"User cancelled cards cache initialization at {i}")
                return note_number + i
            i_str: str = NumberFormatter.with_thousands_separator(i)
            self.__update_progress(f"Caching card sizes: {i_str} of {card_number_str}", i, card_number)
            self.__item_id_cache.get_note_id_by_card_id(card_id)

        for cache in self.__caches:
            cache.set_initialized(True)

        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Cache initialization finished: notes={note_number}, cards={card_number}, "
                 f"duration_sec={duration_sec}, {self.__item_id_cache.get_size()}")
        return note_number + card_number

    def cancel(self):
        self.__wants_cancel = True

    def __update_progress(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        if value and value % self.__update_progress_step == 0:
            self.__update_progress_callback(label, value, max_value)
