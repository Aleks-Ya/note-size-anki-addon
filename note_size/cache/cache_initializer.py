import logging
from logging import Logger

from aqt import AnkiQt
from aqt.qt import QWidget

from .cache import Cache
from .cache_initializer_op import CacheInitializerOp
from .cache_storage import CacheStorage
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter
from ..config.config import Config
from ..ui.details_dialog.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheInitializer:
    def __init__(self, mw: AnkiQt, media_cache: MediaCache, item_id_cache: ItemIdCache,
                 size_calculator: SizeCalculator, size_formatter: SizeFormatter, file_type_helper: FileTypeHelper,
                 cache_storage: CacheStorage, config: Config) -> None:
        self.__mw: AnkiQt = mw
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__caches: list[Cache] = [self.__media_cache, self.__item_id_cache, self.__size_formatter,
                                      self.__size_calculator, self.__file_type_helper]
        self.__cache_storage: CacheStorage = cache_storage
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self) -> None:
        self.__initialize_caches(self.__mw, False)

    def refresh_caches(self, parent: QWidget) -> None:
        log.info("Refresh caches")
        for cache in self.__caches:
            cache.invalidate_cache()
        self.__cache_storage.delete_cache_file()
        self.__initialize_caches(parent, True)

    def save_cache_to_file(self) -> None:
        if self.__config.get_store_cache_in_file_enabled():
            self.__cache_storage.save_caches_to_file(self.__caches)
        else:
            log.info("Saving cache file is disabled")
            self.__cache_storage.delete_cache_file()

    def __initialize_caches(self, parent: QWidget, show_success_info: bool) -> None:
        read_from_file_success: bool = False
        if self.__config.get_store_cache_in_file_enabled():
            read_from_file_success = self.__cache_storage.read_caches_from_file(self.__caches)
        else:
            log.info("Reading cache file is disabled")
        self.__cache_storage.delete_cache_file()
        if not read_from_file_success:
            CacheInitializerOp(self.__mw.taskman, self.__mw.progress, self.__media_cache, self.__item_id_cache,
                               self.__size_calculator, self.__size_formatter, self.__file_type_helper, self.__config,
                               parent, self.__cache_storage, show_success_info).initialize_cache_in_background()
        else:
            log.info("Skip cache initialization because the cache was read from file")
