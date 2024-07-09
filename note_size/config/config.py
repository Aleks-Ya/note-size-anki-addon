import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any, Optional

log: Logger = logging.getLogger(__name__)


class Config:

    def __init__(self, config: dict[str, Any]):
        self.__config = config
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

    def cache_warm_up_enabled(self) -> bool:
        return self.__config['Cache']['Warmup Enabled']

    def deck_browser_show_full_collection_size(self) -> bool:
        return self.__config['Deck Browser']['Show Full Collection Size']

    def log_level(self) -> str:
        return self.__config['Logging']['Logger Level']

    def size_button_details_formatter_max_filename_length(self) -> int:
        return self.__config['Size Button']['Details Window']['Max Filename Length']

    def size_button_details_formatter_max_files_to_show(self) -> int:
        return self.__config['Size Button']['Details Window']['Max Files To Show']

    def size_button_enabled(self) -> bool:
        return self.__config['Size Button']['Enabled']

    def as_dict(self) -> dict[str, Any]:
        return self.__config
