import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any, Optional

log: Logger = logging.getLogger(__name__)


class Config:
    __key_1_cache: str = 'Cache'
    __key_1_deck_browser: str = 'Deck Browser'
    __key_1_logging: str = 'Logging'
    __key_1_size_button: str = 'Size Button'
    __key_2_warmup_enabled: str = 'Warmup Enabled'
    __key_2_store_cache_in_file_enabled: str = 'Store Cache In File Enabled'
    __key_2_show_collection_size: str = 'Show Collection Size'
    __key_2_logger_level: str = 'Logger Level'
    __key_2_details_window: str = 'Details Window'
    __key_2_size_button_enabled: str = 'Enabled'
    __key_2_color: str = 'Color'
    __key_3_max_filename_length: str = 'Max Filename Length'
    __key_3_max_files_to_show: str = 'Max Files To Show'
    __key_3_color_enabled: str = 'Enabled'
    __key_3_levels: str = 'Levels'

    def __init__(self, config: dict[str, Any]):
        self.__config: dict[str, Any] = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        return str(self.__config)

    @classmethod
    def from_path(cls, path: Path) -> 'Config':
        return cls.from_path_updated(path, {})

    @classmethod
    def from_path_updated(cls, path: Path, overwrites: dict[str, Any]) -> 'Config':
        with Path(path).open() as config_file:
            config_data: dict[str, Any] = json.load(config_file)
        return cls(Config.join(config_data, overwrites))

    @staticmethod
    def join(base: Optional[dict[str, Any]], actual: Optional[dict[str, Any]]) \
            -> dict[str, Any]:
        base: dict[str, Any] = dict(base if base else {})
        actual: dict[str, Any] = actual if actual else {}
        for k, v in actual.items():
            if k in base:
                if isinstance(v, dict):
                    base[k] = Config.join(base.get(k, {}), v)
                else:
                    base[k] = v
        return base

    def get_cache_warmup_enabled(self) -> bool:
        return self.__config[self.__key_1_cache][self.__key_2_warmup_enabled]

    def set_cache_warmup_enabled(self, warmup_enabled: bool) -> None:
        self.__set(warmup_enabled, self.__key_1_cache, self.__key_2_warmup_enabled)

    def get_store_cache_in_file_enabled(self) -> bool:
        return self.__config[self.__key_1_cache][self.__key_2_store_cache_in_file_enabled]

    def set_store_cache_in_file_enabled(self, store_cache_in_file_enabled: bool) -> None:
        self.__set(store_cache_in_file_enabled, self.__key_1_cache, self.__key_2_store_cache_in_file_enabled)

    def get_deck_browser_show_collection_size(self) -> bool:
        return self.__config[self.__key_1_deck_browser][self.__key_2_show_collection_size]

    def set_deck_browser_show_collection_size(self, show_collection_size: bool) -> None:
        self.__set(show_collection_size, self.__key_1_deck_browser, self.__key_2_show_collection_size)

    def get_log_level(self) -> str:
        return self.__config[self.__key_1_logging][self.__key_2_logger_level]

    def set_log_level(self, log_level: str) -> None:
        self.__set(log_level, self.__key_1_logging, self.__key_2_logger_level)

    def get_size_button_details_formatter_max_filename_length(self) -> int:
        return self.__config[self.__key_1_size_button][self.__key_2_details_window][self.__key_3_max_filename_length]

    def set_size_button_details_formatter_max_filename_length(self, max_filename_length: int) -> None:
        self.__set(max_filename_length, self.__key_1_size_button, self.__key_2_details_window,
                   self.__key_3_max_filename_length)

    def get_size_button_details_formatter_max_files_to_show(self) -> int:
        return self.__config[self.__key_1_size_button][self.__key_2_details_window][self.__key_3_max_files_to_show]

    def set_size_button_details_formatter_max_files_to_show(self, max_files_to_show: int) -> None:
        self.__set(max_files_to_show, self.__key_1_size_button, self.__key_2_details_window,
                   self.__key_3_max_files_to_show)

    def get_size_button_enabled(self) -> bool:
        return self.__config[self.__key_1_size_button][self.__key_2_size_button_enabled]

    def set_size_button_enabled(self, size_button_enabled: bool) -> None:
        self.__set(size_button_enabled, self.__key_1_size_button, self.__key_2_size_button_enabled)

    def get_size_button_color_enabled(self) -> bool:
        return self.__config[self.__key_1_size_button][self.__key_2_color][self.__key_3_color_enabled]

    def set_size_button_color_enabled(self, color_enabled: bool) -> None:
        self.__set(color_enabled, self.__key_1_size_button, self.__key_2_color, self.__key_3_color_enabled)

    def get_size_button_color_levels(self) -> list[dict[str, str]]:
        return self.__config[self.__key_1_size_button][self.__key_2_color][self.__key_3_levels]

    def set_size_button_color_levels(self, color_levels: list[dict[str, str]]) -> None:
        self.__set(color_levels, self.__key_1_size_button, self.__key_2_color, self.__key_3_levels)

    def get_as_dict(self) -> dict[str, Any]:
        return self.__config

    def __set(self, value: Any, *keys: str) -> None:
        d: dict[str, Any] = self.__config
        for index, key in enumerate(keys):
            is_last: bool = index == len(keys) - 1
            if is_last:
                d[key] = value
            else:
                if key not in d:
                    d[key] = {}
                d = d[key]
