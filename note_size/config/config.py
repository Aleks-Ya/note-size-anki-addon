import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

log: Logger = logging.getLogger(__name__)


class Config:

    def __init__(self, config: dict[str, Any]):
        self.__config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        return str(self.__config)

    @classmethod
    def from_path(cls, path: Path) -> 'Config':
        with Path(path).open() as config_file:
            config_data: dict[str, Any] = json.load(config_file)
        return cls(config_data)

    @classmethod
    def from_path_updated(cls, path: Path, overwrites: dict[str, Any]) -> 'Config':
        with Path(path).open() as config_file:
            config_data: dict[str, Any] = json.load(config_file)
            config_data.update(overwrites)
        return cls(config_data)

    def cache_warm_up_enabled(self) -> bool:
        return self.__config['Cache']['Warmup Enabled']

    def deck_browser_show_full_collection_size(self) -> bool:
        return self.__config['Deck Browser']['Show Full Collection Size']

    def log_level(self) -> str:
        return self.__config['Logging']['Logger Level']

    def details_formatter_max_filename_length(self) -> int:
        return self.__config['Size Button']['Details Window']['Max Filename Length']

    def details_formatter_max_files_to_show(self) -> int:
        return self.__config['Size Button']['Details Window']['Max Files To Show']

    def as_dict(self) -> dict[str, Any]:
        return self.__config
