from typing import Any
import logging
from logging import Logger

from ..cache.cache import Cache
from ..types import SizeStr, SizeBytes

log: Logger = logging.getLogger(__name__)


class SizeFormatter(Cache):

    def __init__(self) -> None:
        super().__init__()
        self.__bytes_to_str_cache: dict[SizeBytes, SizeStr] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def cache_id(self) -> str:
        return "size_formatter"

    def bytes_to_str(self, size: SizeBytes, use_cache: bool = True, precision: int = 1,
                     unit_separator: str = " ") -> SizeStr:
        with self._lock:
            if use_cache and size in self.__bytes_to_str_cache:
                return self.__bytes_to_str_cache[size]
            else:
                size_str: SizeStr = self.__bytes_to_str(size, precision, unit_separator)
                self.__bytes_to_str_cache[size] = size_str
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

    @staticmethod
    def __bytes_to_str(size: SizeBytes, precision: int = 1, unit_separator: str = " ") -> SizeStr:
        divisor: int = 1024
        units: tuple[str, str, str] = 'B', 'KB', 'MB'
        final_unit: str = 'GB'
        num: float = float(size)
        for unit in units:
            if abs(num) < divisor:
                if unit == 'B':
                    return SizeStr(f'{num:0.0f}{unit_separator}{unit}')
                else:
                    return SizeStr(f'{num:0.{precision}f}{unit_separator}{unit}')
            num /= divisor
        return SizeStr(f'{num:0.{precision}f}{unit_separator}{final_unit}')

    def get_cache_size(self) -> int:
        return len(self.__bytes_to_str_cache)
