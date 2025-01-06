import logging
from logging import Logger
from typing import Optional

from aqt.deckbrowser import DeckBrowser
from aqt.operations import QueryOp
from aqt.progress import ProgressManager
from aqt.qt import QWidget
from aqt.taskman import TaskManager
from aqt.utils import showInfo, show_critical

from .cache_initializer_background import CacheInitializerBackground
from .cache_manager import CacheManager
from .cache_storage import CacheStorage
from ..config.config import Config
from ..ui.common.number_formatter import NumberFormatter

log: Logger = logging.getLogger(__name__)


class CacheInitializerOp:
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self, task_manager: TaskManager, progress_manager: ProgressManager, cache_storage: CacheStorage,
                 cache_manager: CacheManager, deck_browser: DeckBrowser, parent: QWidget, show_success_info: bool,
                 config: Config):
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__cache_manager: CacheManager = cache_manager
        self.__parent: QWidget = parent
        self.__show_success_info: bool = show_success_info
        self.__cache_initializer_background: CacheInitializerBackground = CacheInitializerBackground(
            cache_storage, cache_manager, deck_browser, task_manager, config, self.__update_progress)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_cache_in_background(self) -> None:
        log.info("Initialize cache")
        query_op: QueryOp[int] = QueryOp(parent=self.__parent, op=self.__cache_initializer_background.initialize_caches,
                                         success=self.__on_success).failure(self.__on_failure).with_progress(
            "Note Size cache initializing")
        query_op.run_in_background()

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
            showInfo(title=self.__progress_dialog_title, text=f"Cache was initialized ({count_str} notes)")

    def __on_failure(self, e: Exception) -> None:
        log.error("Error during cache initialization", exc_info=e)
        show_critical(title=self.__progress_dialog_title, text="Cache initialization failed (see logs)")
