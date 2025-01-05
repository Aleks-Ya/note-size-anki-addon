import logging
from datetime import datetime
from logging import Logger
from typing import Optional, Callable

import aqt
from anki.collection import Collection

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
        self.__update_progress("Cache initializing", None, None)
        note_number: int = col.note_count()
        processed_notes: int = 0
        self.__update_progress("Cache initializing", processed_notes, note_number)
        for note_id, note_type_id, fields in col.db.execute("select id, mid, flds from notes"):
            size_calculator.initialize_note_in_caches(note_id, note_type_id, fields)
            if self.__wants_cancel:
                log.info(f"User cancelled notes cache initialization at {processed_notes}")
                return processed_notes
            self.__update_progress("Caching note sizes", processed_notes, note_number)
            for size_type in SizeType:
                size_str_cache.get_note_size_str(note_id, size_type, use_cache=True)
                note_files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
                for note_file in note_files:
                    file_type_helper.get_file_type(note_file, use_cache=True)
            processed_notes += 1

        self.__update_progress("Caching card ids...", None, None)
        item_id_cache.initialize_cache()

        self.__cache_manager.set_caches_initialized(True)

        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        if aqt.mw and aqt.mw.deckBrowser:
            aqt.mw.taskman.run_on_main(aqt.mw.deckBrowser.refresh)
        log.info(f"Cache initialization finished: notes={note_number}, "
                 f"duration_sec={duration_sec}, {item_id_cache.get_cache_size()}")
        return note_number

    def cancel(self):
        self.__wants_cancel = True

    def __update_progress(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        if value and value % self.__update_progress_step == 0:
            value_str: str = NumberFormatter.with_thousands_separator(value)
            max_value_str: str = NumberFormatter.with_thousands_separator(max_value)
            full_label: str = f"{label}: {value_str} of {max_value_str}" if max_value else label
            self.__update_progress_callback(full_label, value, max_value)
