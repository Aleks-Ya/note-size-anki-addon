import json
import logging
from logging import Logger
from pathlib import Path
from typing import Optional, Any

from .config_listener import ConfigListener
from ..config.level_parser import LevelDict
from ..common.types import SignificantDigits

log: Logger = logging.getLogger(__name__)


class Config:
    __key_1_cache: str = 'Cache'
    __key_1_deck_browser: str = 'Deck Browser'
    __key_1_browser: str = 'Browser'
    __key_1_logging: str = 'Logging'
    __key_1_size_button: str = 'Size Button'
    __key_1_profiler: str = 'Profiler'
    __key_2_warmup_enabled: str = 'Warmup Enabled'
    __key_2_store_cache_in_file_enabled: str = 'Store Cache In File Enabled'
    __key_2_deck_browser_show_collection_size: str = 'Show Collection Size'
    __key_2_significant_digits: str = 'Significant Digits'
    __key_2_logger_level: str = 'Logger Level'
    __key_2_size_button_enabled: str = 'Enabled'
    __key_2_color: str = 'Color'
    __key_2_browser_show_found_notes_size: str = 'Show Found Notes Size'
    __key_2_profiler_enabled: str = 'Enabled'
    __key_3_size_button_color_enabled: str = 'Enabled'
    __key_3_size_button_levels: str = 'Levels v2'

    def __init__(self, config: dict[str, Any]):
        self.__config: dict[str, Any] = config
        self.__listeners: set[ConfigListener] = set()
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
    def join(base: Optional[dict[str, Any]], actual: Optional[dict[str, Any]]) -> dict[str, Any]:
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
        return self.__config[self.__key_1_deck_browser][self.__key_2_deck_browser_show_collection_size]

    def set_deck_browser_show_collection_size(self, show_collection_size: bool) -> None:
        self.__set(show_collection_size, self.__key_1_deck_browser, self.__key_2_deck_browser_show_collection_size)

    def get_deck_browser_significant_digits(self) -> SignificantDigits:
        return self.__config[self.__key_1_deck_browser][self.__key_2_significant_digits]

    def set_deck_browser_significant_digits(self, significant_digits: SignificantDigits) -> None:
        self.__set(significant_digits, self.__key_1_deck_browser, self.__key_2_significant_digits)

    def get_browser_show_found_notes_size(self) -> bool:
        return self.__config[self.__key_1_browser][self.__key_2_browser_show_found_notes_size]

    def set_browser_show_found_notes_size(self, show_found_notes_size_size: bool) -> None:
        self.__set(show_found_notes_size_size, self.__key_1_browser, self.__key_2_browser_show_found_notes_size)

    def get_browser_significant_digits(self) -> SignificantDigits:
        return self.__config[self.__key_1_browser][self.__key_2_significant_digits]

    def set_browser_significant_digits(self, significant_digits: SignificantDigits) -> None:
        self.__set(significant_digits, self.__key_1_browser, self.__key_2_significant_digits)

    def get_log_level(self) -> str:
        return self.__config[self.__key_1_logging][self.__key_2_logger_level]

    def set_log_level(self, log_level: str) -> None:
        self.__set(log_level, self.__key_1_logging, self.__key_2_logger_level)

    def get_size_button_enabled(self) -> bool:
        return self.__config[self.__key_1_size_button][self.__key_2_size_button_enabled]

    def set_size_button_enabled(self, size_button_enabled: bool) -> None:
        self.__set(size_button_enabled, self.__key_1_size_button, self.__key_2_size_button_enabled)

    def get_size_button_significant_digits(self) -> SignificantDigits:
        return self.__config[self.__key_1_size_button][self.__key_2_significant_digits]

    def set_size_button_significant_digits(self, significant_digits: SignificantDigits) -> None:
        self.__set(significant_digits, self.__key_1_size_button, self.__key_2_significant_digits)

    def get_size_button_color_enabled(self) -> bool:
        return self.__config[self.__key_1_size_button][self.__key_2_color][self.__key_3_size_button_color_enabled]

    def set_size_button_color_enabled(self, color_enabled: bool) -> None:
        self.__set(color_enabled, self.__key_1_size_button, self.__key_2_color, self.__key_3_size_button_color_enabled)

    def get_size_button_color_levels(self) -> list[LevelDict]:
        return self.__config[self.__key_1_size_button][self.__key_2_color][self.__key_3_size_button_levels]

    def set_size_button_color_levels(self, color_levels: list[LevelDict]) -> None:
        self.__set(color_levels, self.__key_1_size_button, self.__key_2_color, self.__key_3_size_button_levels)

    def get_profiler_enabled(self) -> bool:
        return self.__config[self.__key_1_profiler][self.__key_2_profiler_enabled]

    def set_profiler_enabled(self, profiler_enabled: bool) -> None:
        self.__set(profiler_enabled, self.__key_1_profiler, self.__key_2_profiler_enabled)

    def get_as_dict(self) -> dict[str, Any]:
        return self.__config

    def add_listener(self, listener: ConfigListener) -> None:
        log.debug(f"Add config listener: {listener}")
        self.__listeners.add(listener)

    def fire_config_changed(self) -> None:
        log.debug("Fire config changed")
        for listener in self.__listeners:
            listener.on_config_changed()

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

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
