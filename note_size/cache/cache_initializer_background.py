import logging
from datetime import datetime
from logging import Logger
from typing import Optional, Callable

from anki.collection import Collection
from aqt.deckbrowser import DeckBrowser
from aqt.taskman import TaskManager

from .cache_manager import CacheManager
from .cache_storage import CacheStorage
from .item_id_cache import ItemIdCache
from .size_str_cache import SizeStrCache
from ..calculator.size_calculator import SizeCalculator
from ..config.config import Config
from ..types import SizeType, MediaFile, SizePrecision
from ..ui.common.number_formatter import NumberFormatter
from ..ui.details_dialog.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheInitializerBackground:

    def __init__(self, cache_storage: CacheStorage, cache_manager: CacheManager, deck_browser: DeckBrowser,
                 task_manager: TaskManager, config: Config,
                 update_progress_callback: Callable[[str, Optional[int], Optional[int]], None],
                 update_progress_step: int = 1000):
        self.__cache_storage: CacheStorage = cache_storage
        self.__cache_manager: CacheManager = cache_manager
        self.__deck_browser: DeckBrowser = deck_browser
        self.__task_manager: TaskManager = task_manager
        self.__wants_cancel: bool = False
        self.__config: Config = config
        self.__update_progress_callback: Callable[[str, Optional[int], Optional[int]], None] = update_progress_callback
        self.__update_progress_step: int = update_progress_step
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self, col: Collection) -> int:
        self.__cache_manager.set_caches_initialized(False)
        result: int = 0
        read_from_file_success: bool = self.__read_cache_from_file()
        if not read_from_file_success:
            result = self.__initialize_caches(col)
        self.__task_manager.run_on_main(self.__deck_browser.refresh)
        return result

    def __initialize_caches(self, col) -> int:
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
            if self.__wants_cancel:
                log.info(f"User cancelled notes cache initialization at {processed_notes}")
                return processed_notes
            self.__update_progress("Caching note sizes", processed_notes, note_number)
            size_calculator.initialize_note_in_caches(note_id, note_type_id, fields)
            for size_type in SizeType:
                deck_browser_size_precision: SizePrecision = self.__config.get_deck_browser_size_precision()
                browser_size_precision: SizePrecision = self.__config.get_browser_size_precision()
                editor_size_precision: SizePrecision = self.__config.get_size_button_size_precision()
                size_str_cache.get_note_size_str(note_id, size_type, deck_browser_size_precision, use_cache=True)
                size_str_cache.get_note_size_str(note_id, size_type, browser_size_precision, use_cache=True)
                size_str_cache.get_note_size_str(note_id, size_type, editor_size_precision, use_cache=True)
                note_files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
                for note_file in note_files:
                    file_type_helper.get_file_type(note_file, use_cache=True)
            processed_notes += 1
        self.__update_progress("Caching card ids...", None, None)
        item_id_cache.initialize_cache()
        self.__cache_manager.set_caches_initialized(True)
        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Cache initialization finished: notes={note_number}, "
                 f"duration_sec={duration_sec}, cache_size={item_id_cache.get_cache_size()}")
        return note_number

    def cancel(self):
        self.__wants_cancel = True

    def __read_cache_from_file(self) -> bool:
        read_from_file_success: bool = False
        if self.__config.get_store_cache_in_file_enabled():
            read_from_file_success = self.__cache_storage.read_caches_from_file(self.__cache_manager.get_caches())
        else:
            log.info("Reading cache file is disabled")
        if read_from_file_success:
            self.__cache_manager.set_caches_initialized(True)
        self.__cache_storage.delete_cache_file()
        return read_from_file_success

    def __update_progress(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        if value and value % self.__update_progress_step == 0:
            value_str: str = NumberFormatter.with_thousands_separator(value)
            max_value_str: str = NumberFormatter.with_thousands_separator(max_value)
            full_label: str = f"{label}: {value_str} of {max_value_str}" if max_value else label
            self.__update_progress_callback(full_label, value, max_value)
