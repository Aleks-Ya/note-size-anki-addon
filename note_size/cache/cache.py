import logging
from abc import ABC, abstractmethod
from logging import Logger
from threading import RLock
from typing import Any

log: Logger = logging.getLogger(__name__)


class Cache(ABC):
    def __init__(self):
        self._lock: RLock = RLock()
        self.__initialized: bool = False

    @abstractmethod
    def cache_id(self) -> str:
        pass

    def is_initialized(self) -> bool:
        initialized: bool = False
        if self._lock.acquire(blocking=False):
            try:
                initialized = self.__initialized
            finally:
                self._lock.release()
        return initialized

    def set_initialized(self, initialized: bool) -> None:
        log.debug(f"Set cache initialized: cache={self.cache_id()}, initialized={initialized}")
        with self._lock:
            self.__initialized = initialized

    @abstractmethod
    def invalidate_cache(self) -> None:
        pass

    @abstractmethod
    def as_dict_list(self) -> list[dict[Any, Any]]:
        pass

    @abstractmethod
    def read_from_dict_list(self, dict_list: list[dict[Any, Any]]):
        pass
