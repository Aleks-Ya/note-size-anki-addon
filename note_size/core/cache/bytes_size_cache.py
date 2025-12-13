import logging
from logging import Logger
from typing import Any

from .cache import Cache
from ..common.size_formatter import SizeFormatter
from ..common.types import SizeStr, SizeBytes, SignificantDigits

log: Logger = logging.getLogger(__name__)


class BytesSizeCache(Cache):

    def __init__(self) -> None:
        super().__init__()
        self.__bytes_to_str_cache: dict[SizeBytes, dict[SignificantDigits, SizeStr]] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def bytes_to_str(self, size: SizeBytes, significant_digits: SignificantDigits, use_cache: bool = True,
                     unit_separator: str = " ") -> SizeStr:
        with self._lock:
            if use_cache and size in self.__bytes_to_str_cache and significant_digits in self.__bytes_to_str_cache[
                size]:
                return self.__bytes_to_str_cache[size][significant_digits]
            else:
                size_str: SizeStr = SizeFormatter.bytes_to_str(size, significant_digits, unit_separator)
                if size not in self.__bytes_to_str_cache:
                    self.__bytes_to_str_cache[size] = {}
                self.__bytes_to_str_cache[size][significant_digits] = size_str
                return size_str

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__bytes_to_str_cache.clear()

    def as_dict_list(self) -> list[dict[Any, Any]]:
        with self._lock:
            return [self.__bytes_to_str_cache]

    def read_from_dict_list(self, dict_list: list[dict[Any, Any]]):
        with self._lock:
            self.__bytes_to_str_cache = dict_list[0]

    def get_cache_size(self) -> int:
        with self._lock:
            return len(self.__bytes_to_str_cache)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
