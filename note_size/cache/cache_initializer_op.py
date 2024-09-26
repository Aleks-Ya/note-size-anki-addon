import logging
from datetime import datetime
from logging import Logger
from typing import Sequence, Optional

from anki.collection import Collection
from anki.notes import NoteId
from aqt.operations import QueryOp
from aqt.progress import ProgressManager
from aqt.qt import QWidget
from aqt.taskman import TaskManager
from aqt.utils import showInfo, show_critical

from .cache import Cache
from .cache_storage import CacheStorage
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter
from ..config.config import Config
from ..types import SizeType, MediaFile
from ..ui.common.number_formatter import NumberFormatter
from ..ui.details_dialog.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheInitializerOp:
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self, task_manager: TaskManager, progress_manager: ProgressManager, media_cache: MediaCache,
                 item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                 file_type_helper: FileTypeHelper, config: Config, parent: QWidget, cache_storage: CacheStorage,
                 show_success_info: bool):
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__caches: list[Cache] = [self.__media_cache, self.__item_id_cache, self.__size_formatter,
                                      self.__size_calculator, self.__file_type_helper]
        self.__config: Config = config
        self.__parent: QWidget = parent
        self.__cache_storage: CacheStorage = cache_storage
        self.__show_success_info: bool = show_success_info
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_cache_in_background(self) -> None:
        if self.__config.get_cache_warmup_enabled():
            log.info("Initialize cache")
            QueryOp(parent=self.__parent, op=self.__background_op, success=self.__on_success).failure(
                self.__on_failure).with_progress("Note Size cache initializing").run_in_background()
        else:
            log.info("Cache initialization is disabled")
            for cache in self.__caches:
                cache.set_initialized(True)

    def __background_op(self, col: Collection) -> int:
        read_from_file_success: bool = False
        if self.__config.get_store_cache_in_file_enabled():
            read_from_file_success = self.__cache_storage.read_caches_from_file(self.__caches)
        else:
            log.info("Reading cache file is disabled")
        self.__cache_storage.delete_cache_file()
        if not read_from_file_success:
            log.info(f"Cache initialization started: {self.__item_id_cache.get_size()}")
            start_time: datetime = datetime.now()
            self.__update_progress("Note Size cache initializing", None, None)

            all_note_ids: Sequence[NoteId] = col.find_notes("deck:*")
            note_number: int = len(all_note_ids)
            note_number_str: str = NumberFormatter.with_thousands_separator(note_number)
            for i, note_id in enumerate(all_note_ids):
                if self.__progress_manager.want_cancel():
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
                if self.__progress_manager.want_cancel():
                    log.info(f"User cancelled cards cache initialization at {i}")
                    return note_number + i
                i_str: str = NumberFormatter.with_thousands_separator(i)
                self.__update_progress(f"Caching card sizes: {i_str} of {card_number_str}", i, card_number)
                self.__item_id_cache.get_note_id_by_card_id(card_id)

            end_time: datetime = datetime.now()
            duration_sec: int = round((end_time - start_time).total_seconds())
            log.info(f"Cache initialization finished: notes={note_number}, cards={card_number}, "
                     f"duration_sec={duration_sec}, {self.__item_id_cache.get_size()}")
            return note_number + card_number
        else:
            log.info("Skip cache initialization because the cache was read from file")
            return 0

    def __update_progress(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        if value and value % 1000 == 0:
            self.__task_manager.run_on_main(lambda: self.__update_progress_in_main(label, value, max_value))

    def __update_progress_in_main(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        self.__progress_manager.set_title(self.__progress_dialog_title)
        self.__progress_manager.update(label=label, value=value, max=max_value)

    def __on_success(self, count: int) -> None:
        for cache in self.__caches:
            cache.set_initialized(True)
        log.info(f"Cache initialization finished: {count}")
        if self.__show_success_info:
            showInfo(title=self.__progress_dialog_title, text=f"Cache was initialized ({count} notes and cards)")

    def __on_failure(self, e: Exception) -> None:
        log.error("Error during cache initialization", exc_info=e)
        show_critical(title=self.__progress_dialog_title, text="Cache initialization failed (see logs)")
