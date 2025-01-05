import logging
from logging import Logger

from aqt import AnkiQt
from aqt.qt import QWidget

from .cache_initializer_op import CacheInitializerOp
from .cache_manager import CacheManager
from .cache_storage import CacheStorage
from ..config.config import Config

log: Logger = logging.getLogger(__name__)


class CacheInitializer:
    def __init__(self, mw: AnkiQt, cache_manager: CacheManager, cache_storage: CacheStorage, config: Config) -> None:
        self.__mw: AnkiQt = mw
        self.__cache_manager: CacheManager = cache_manager
        self.__cache_storage: CacheStorage = cache_storage
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def warmup_caches(self) -> None:
        log.info("Warmup caches if enabled")
        if self.__config.get_cache_warmup_enabled():
            self.__initialize_caches(self.__mw, False)
        else:
            log.info("Cache initialization is disabled")

    def refresh_caches(self, parent: QWidget) -> None:
        log.info("Refresh caches")
        self.__cache_manager.invalidate_caches()
        self.__cache_storage.delete_cache_file()
        self.__initialize_caches(parent, True)

    def save_cache_to_file(self) -> None:
        if self.__config.get_store_cache_in_file_enabled():
            self.__cache_storage.save_caches_to_file(self.__cache_manager.get_caches())
        else:
            log.info("Saving cache file is disabled")
            self.__cache_storage.delete_cache_file()

    def __initialize_caches(self, parent: QWidget, show_success_info: bool) -> None:
        read_from_file_success: bool = False
        if self.__config.get_store_cache_in_file_enabled():
            read_from_file_success = self.__cache_storage.read_caches_from_file(self.__cache_manager.get_caches())
            if read_from_file_success:
                self.__cache_manager.set_caches_initialized(True)
        else:
            log.info("Reading cache file is disabled")
        self.__cache_storage.delete_cache_file()
        if not read_from_file_success:
            cache_initializer_op: CacheInitializerOp = CacheInitializerOp(
                self.__mw.taskman, self.__mw.progress, self.__cache_manager, parent, show_success_info)
            cache_initializer_op.initialize_cache_in_background()
        else:
            log.info("Skip cache initialization because the cache was read from file")
