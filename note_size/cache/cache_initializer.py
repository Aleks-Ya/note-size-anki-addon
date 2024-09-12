import logging
from logging import Logger

from aqt import AnkiQt
from aqt.qt import QWidget

from .cache_initializer_op import CacheInitializerOp
from .cache_storage import CacheStorage
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter
from ..config.config import Config

log: Logger = logging.getLogger(__name__)


class CacheInitializer:
    def __init__(self, mw: AnkiQt, media_cache: MediaCache, item_id_cache: ItemIdCache,
                 size_calculator: SizeCalculator, size_formatter: SizeFormatter, cache_storage: CacheStorage,
                 config: Config) -> None:
        self.__mw: AnkiQt = mw
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__cache_storage: CacheStorage = cache_storage
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self) -> None:
        CacheInitializerOp(self.__mw, self.__media_cache, self.__item_id_cache, self.__size_calculator,
                           self.__size_formatter, self.__config, self.__mw, self.__cache_storage,
                           show_success_info=False).initialize_cache_in_background()

    def refresh_caches(self, parent: QWidget) -> None:
        log.info("Refresh caches")
        self.__cache_storage.delete_cache_file()
        self.__media_cache.invalidate_cache()
        self.__item_id_cache.invalidate_cache()
        CacheInitializerOp(self.__mw, self.__media_cache, self.__item_id_cache, self.__size_calculator,
                           self.__size_formatter, self.__config, parent, self.__cache_storage,
                           show_success_info=True).initialize_cache_in_background()

    def save_cache_to_file(self) -> None:
        if self.__config.get_store_cache_in_file_enabled():
            self.__cache_storage.save_caches_to_file([self.__item_id_cache, self.__size_calculator, self.__media_cache])
        else:
            log.info("Saving cache file is disabled")
            self.__cache_storage.delete_cache_file()
