import logging
from logging import Logger
from typing import Any

from ..cache.cache import Cache
from ..common.types import SizeStr, SizeBytes, SignificantDigits

log: Logger = logging.getLogger(__name__)


class SizeFormatter(Cache):

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
                size_str: SizeStr = self.__bytes_to_str(size, significant_digits, unit_separator)
                if size not in self.__bytes_to_str_cache:
                    self.__bytes_to_str_cache[size] = {}
                self.__bytes_to_str_cache[size][significant_digits] = size_str
                return size_str

    @staticmethod
    def str_to_bytes(size_str: SizeStr) -> SizeBytes:
        size_str = size_str.strip()
        units = {'B': 0, 'KB': 1, 'MB': 2, 'GB': 3}
        if size_str[-2:].upper() in units:
            size = float(size_str[:-2])
            unit = units[size_str[-2:].upper()]
        elif size_str[-1].upper() in units:
            size = float(size_str[:-1])
            unit = units[size_str[-1].upper()]
        else:
            raise ValueError(f"Invalid size string: '{size_str}'")
        size_in_bytes = int(size * (1024 ** unit))
        return SizeBytes(size_in_bytes)

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

    @staticmethod
    def __bytes_to_str(size: SizeBytes, significant_digits: SignificantDigits, unit_separator: str = " ") -> SizeStr:
        divisor: int = 1024
        byte_unit: str = 'B'
        units: list[str] = [byte_unit, 'KB', 'MB', 'GB']
        num: float = size
        unit_index: int = 0
        while num >= divisor and unit_index < len(units) - 1:
            num /= divisor
            unit_index += 1
        unit: str = units[unit_index]
        precision: int = max(0, significant_digits - len(str(int(num)))) if unit != byte_unit else 0
        return SizeStr(f"{num:.{precision}f}{unit_separator}{unit}")
