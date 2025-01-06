import logging
from logging import Logger

from aqt.deckbrowser import DeckBrowser
from aqt.progress import ProgressManager
from aqt.qt import QWidget
from aqt.taskman import TaskManager

from .cache_initializer_op import CacheInitializerOp
from .cache_manager import CacheManager
from .cache_storage import CacheStorage
from ..config.config import Config

log: Logger = logging.getLogger(__name__)


class CacheInitializer:
    def __init__(self, parent: QWidget, cache_manager: CacheManager, cache_storage: CacheStorage,
                 deck_browser: DeckBrowser, task_manager: TaskManager, progress_manager: ProgressManager,
                 config: Config) -> None:
        self.__parent: QWidget = parent
        self.__cache_manager: CacheManager = cache_manager
        self.__cache_storage: CacheStorage = cache_storage
        self.__deck_browser: DeckBrowser = deck_browser
        self.__task_manager: TaskManager = task_manager
        self.__progress_manager: ProgressManager = progress_manager
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def warmup_caches(self) -> None:
        log.info("Warmup caches if enabled")
        if self.__config.get_cache_warmup_enabled():
            self.__initialize_caches(self.__parent, False)
        else:
            log.info("Cache initialization is disabled")

    def refresh_caches(self, parent: QWidget) -> None:
        log.info("Refresh caches")
        self.__cache_manager.invalidate_caches()
        self.__cache_storage.delete_cache_file()
        self.__initialize_caches(parent, True)

    def save_cache_to_file(self) -> None:
        enabled: bool = self.__config.get_store_cache_in_file_enabled()
        initialized: bool = self.__cache_manager.get_caches_initialized()
        if enabled and initialized:
            self.__cache_storage.save_caches_to_file(self.__cache_manager.get_caches())
        else:
            log.info(f"Skip saving cache file: "
                     f"store_cache_in_file_enabled={enabled}, caches_initialized={initialized}")
            self.__cache_storage.delete_cache_file()

    def __initialize_caches(self, parent: QWidget, show_success_info: bool) -> None:
        cache_initializer_op: CacheInitializerOp = CacheInitializerOp(
            self.__task_manager, self.__progress_manager, self.__cache_storage, self.__cache_manager,
            self.__deck_browser, parent, show_success_info, self.__config)
        cache_initializer_op.initialize_cache_in_background()
