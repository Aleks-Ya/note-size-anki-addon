import logging
from logging import Logger

from aqt import AnkiQt
from aqt.qt import QWidget

from .cache_initializer_op import CacheInitializerOp
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..config.config import Config

log: Logger = logging.getLogger(__name__)


class CacheInitializer:
    def __init__(self, mw: AnkiQt, media_cache: MediaCache, item_id_cache: ItemIdCache, config: Config):
        self.__mw: AnkiQt = mw
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self):
        CacheInitializerOp(self.__mw, self.__media_cache, self.__item_id_cache, self.__config, self.__mw,
                           show_success_info=False).initialize_cache_in_background()

    def refresh_caches(self, parent: QWidget):
        log.info("Refresh caches")
        self.__item_id_cache.delete_cache_file()
        self.__media_cache.invalidate_cache()
        self.__item_id_cache.invalidate_caches()
        CacheInitializerOp(self.__mw, self.__media_cache, self.__item_id_cache, self.__config, parent,
                           show_success_info=True).initialize_cache_in_background()

    def save_cache_to_file(self):
        if self.__config.get_store_cache_in_file_enabled():
            self.__item_id_cache.save_caches_to_file()
        else:
            log.info("Saving cache file is disabled")
            self.__item_id_cache.delete_cache_file()
