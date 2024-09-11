import logging
import os
import pickle
from logging import Logger
from pathlib import Path
from threading import RLock

from .cache import Cache
from ..config.settings import Settings

log: Logger = logging.getLogger(__name__)


class CacheStorage:

    def __init__(self, settings: Settings) -> None:
        self.__lock: RLock = RLock()
        self.__cache_file: Path = settings.cache_file
        log.debug(f"{self.__class__.__name__} was instantiated")

    def save_caches_to_file(self, caches: list[Cache]) -> None:
        with self.__lock:
            try:
                log.info(f"Saving cache file: {self.__cache_file}")
                dict_of_caches: dict[str, list[dict]] = {cache.cache_id(): cache.as_dict_list() for cache in caches}
                pickle.dump(dict_of_caches, self.__cache_file.open("wb"))
                log.info(f"Caches were saved to file: {self.__cache_file}")
            except Exception:
                log.warning(f"Cannot save cache file: {self.__cache_file}", exc_info=True)

    def read_caches_from_file(self, caches: list[Cache]) -> bool:
        if self.__cache_file.exists():
            log.info(f"Reading cache file: {self.__cache_file}")
            with self.__lock:
                try:
                    dict_of_caches: dict[str, list[dict]] = pickle.load(open(self.__cache_file, 'rb'))
                    for cache in caches:
                        cache.read_from_dict_list(dict_of_caches[cache.cache_id()])
                    log.info(f"Caches were read from file: {self.__cache_file}")
                    return True
                except Exception:
                    log.warning(f"Cannot deserialize cache file: {self.__cache_file}", exc_info=True)
                    for cache in caches:
                        cache.invalidate_cache()
                    self.delete_cache_file()
        else:
            log.info(f"Skip reading absent cache file: {self.__cache_file}")
        return False

    def delete_cache_file(self) -> None:
        if self.__cache_file.exists():
            os.remove(self.__cache_file)
            log.info(f"Cache file was deleted: {self.__cache_file}")
