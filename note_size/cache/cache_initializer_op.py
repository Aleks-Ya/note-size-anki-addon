import logging
from logging import Logger
from typing import Optional

from aqt.operations import QueryOp
from aqt.progress import ProgressManager
from aqt.qt import QWidget
from aqt.taskman import TaskManager
from aqt.utils import showInfo, show_critical

from .cache import Cache
from .cache_initializer_background import CacheInitializerBackground
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter
from ..config.config import Config
from ..ui.common.number_formatter import NumberFormatter
from ..ui.details_dialog.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheInitializerOp:
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self, task_manager: TaskManager, progress_manager: ProgressManager, media_cache: MediaCache,
                 item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                 file_type_helper: FileTypeHelper, config: Config, parent: QWidget, show_success_info: bool):
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__caches: list[Cache] = [media_cache, item_id_cache, size_formatter, size_calculator, file_type_helper]
        self.__config: Config = config
        self.__parent: QWidget = parent
        self.__show_success_info: bool = show_success_info
        self.__cache_initializer_background: CacheInitializerBackground = CacheInitializerBackground(
            media_cache, item_id_cache, size_calculator, size_formatter, file_type_helper, self.__update_progress)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_cache_in_background(self) -> None:
        if self.__config.get_cache_warmup_enabled():
            log.info("Initialize cache")
            query_op: QueryOp[int] = QueryOp(parent=self.__parent,
                                             op=self.__cache_initializer_background.initialize_caches,
                                             success=self.__on_success).failure(self.__on_failure).with_progress(
                "Note Size cache initializing")
            query_op.run_in_background()
        else:
            log.info("Cache initialization is disabled")
            for cache in self.__caches:
                cache.set_initialized(True)

    def __update_progress(self, label: str, value: int, max_value: int) -> None:
        self.__task_manager.run_on_main(lambda: self.__update_progress_in_main(label, value, max_value))
        if self.__progress_manager.want_cancel():
            self.__cache_initializer_background.cancel()

    def __update_progress_in_main(self, label: str, value: Optional[int], max_value: Optional[int]) -> None:
        self.__progress_manager.set_title(self.__progress_dialog_title)
        self.__progress_manager.update(label=label, value=value, max=max_value)

    def __on_success(self, count: int) -> None:
        log.info(f"Cache initialization finished: {count}")
        if self.__show_success_info:
            count_str: str = NumberFormatter.with_thousands_separator(count)
            showInfo(title=self.__progress_dialog_title, text=f"Cache was initialized ({count_str} notes and cards)")

    def __on_failure(self, e: Exception) -> None:
        log.error("Error during cache initialization", exc_info=e)
        show_critical(title=self.__progress_dialog_title, text="Cache initialization failed (see logs)")
