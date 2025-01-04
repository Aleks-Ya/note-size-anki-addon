import logging
from datetime import datetime
from logging import Logger
from typing import Sequence, Optional, Callable

from anki.collection import Collection
from anki.notes import NoteId

from .cache_manager import CacheManager
from .item_id_cache import ItemIdCache
from .size_str_cache import SizeStrCache
from ..calculator.size_calculator import SizeCalculator
from ..types import SizeType, MediaFile
from ..ui.common.number_formatter import NumberFormatter
from ..ui.details_dialog.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheInitializerBackground:

    def __init__(self, cache_manager: CacheManager,
                 update_progress_callback: Callable[[str, Optional[int], Optional[int]], None],
                 update_progress_step: int = 500):
        self.__cache_manager: CacheManager = cache_manager
        self.__wants_cancel: bool = False
        self.__update_progress_callback: Callable[[str, Optional[int], Optional[int]], None] = update_progress_callback
        self.__update_progress_step: int = update_progress_step
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self, col: Collection) -> int:
        item_id_cache: ItemIdCache = self.__cache_manager.get_item_id_cache()
        size_calculator: SizeCalculator = self.__cache_manager.get_size_calculator()
        file_type_helper: FileTypeHelper = self.__cache_manager.get_file_type_helper()
        size_str_cache: SizeStrCache = self.__cache_manager.get_size_str_cache()
        log.info(f"Cache initialization started: {item_id_cache.get_cache_size()}")
        start_time: datetime = datetime.now()
        self.__update_progress("Note Size cache initializing", None, None)

        all_note_ids: Sequence[NoteId] = col.db.list("select id from notes")
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
                size_str_cache.get_note_size_str(note_id, size_type, use_cache=True)
                size_calculator.get_note_file_sizes(note_id, use_cache=True)
                note_files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
                for note_file in note_files:
                    file_type_helper.get_file_type(note_file, use_cache=True)

        self.__update_progress(f"Caching card ids...", None, None)
        item_id_cache.initialize_cache()

        self.__cache_manager.set_caches_initialized(True)

        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Cache initialization finished: notes={note_number}, "
                 f"duration_sec={duration_sec}, {item_id_cache.get_cache_size()}")
        return note_number

    def cancel(self):
        self.__wants_cancel = True

    def __update_progress(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        if value and value % self.__update_progress_step == 0:
            self.__update_progress_callback(label, value, max_value)
