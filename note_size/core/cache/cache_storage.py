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
    cache_metadata_key: str = "cache_metadata"
    version_key: str = "version"

    def __init__(self, current_cache_version: int, settings: Settings) -> None:
        self.__lock: RLock = RLock()
        self.__current_cache_version: int = current_cache_version
        self.__settings: Settings = settings
        log.debug(f"{self.__class__.__name__} was instantiated")

    def save_caches_to_file(self, caches: list[Cache]) -> None:
        with self.__lock:
            cache_file: Path = self.__settings.get_cache_file()
            try:
                log.info(f"Saving cache file: {cache_file}")
                dict_of_caches: dict[str, list[dict]] = {cache.cache_id(): cache.as_dict_list() for cache in caches}
                dict_of_caches[self.cache_metadata_key] = [{self.version_key: self.__current_cache_version}]
                with cache_file.open("wb") as io:
                    # noinspection PyTypeChecker
                    pickle.dump(dict_of_caches, io)
                log.info(f"Caches were saved to file: {cache_file}")
            except Exception:
                log.warning(f"Cannot save cache file: {cache_file}", exc_info=True)

    def read_caches_from_file(self, caches: list[Cache]) -> bool:
        cache_file: Path = self.__settings.get_cache_file()
        if cache_file.exists():
            log.info(f"Reading cache file: {cache_file}")
            with self.__lock:
                try:
                    dict_of_caches: dict[str, list[dict]] = pickle.load(open(cache_file, 'rb'))
                    cache_version: int = dict_of_caches[self.cache_metadata_key][0][self.version_key]
                    if cache_version != self.__current_cache_version:
                        log.warning(f"Saved cache version differs: saved={cache_version}, "
                                    f"current={self.__current_cache_version}. Ignoring saved cache.")
                        self.__invalidate_and_delete_caches(caches)
                        return False
                    for cache in caches:
                        cache.read_from_dict_list(dict_of_caches[cache.cache_id()])
                    log.info(f"Caches were read from file: {cache_file}")
                    return True
                except Exception:
                    log.warning(f"Cannot deserialize cache file: {cache_file}", exc_info=True)
                    self.__invalidate_and_delete_caches(caches)
        else:
            log.info(f"Skip reading absent cache file: {cache_file}")
        return False

    def delete_cache_file(self) -> None:
        cache_file: Path = self.__settings.get_cache_file()
        if cache_file.exists():
            os.remove(cache_file)
            log.info(f"Cache file was deleted: {cache_file}")

    def __invalidate_and_delete_caches(self, caches: list[Cache]) -> None:
        for cache in caches:
            cache.invalidate_cache()
        self.delete_cache_file()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
