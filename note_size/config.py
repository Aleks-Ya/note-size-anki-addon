import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

log: Logger = logging.getLogger(__name__)


class Config:

    def __init__(self, config: dict[str, Any]):
        self.config = config
        log.info(f"Config loaded: {self.config}")

    @classmethod
    def from_path(cls, path: Path) -> 'Config':
        with Path(path).open() as config_file:
            config_data: dict[str, Any] = json.load(config_file)
        return cls(config_data)

    def details_formatter_max_file_length(self) -> int:
        return self.config['Details Formatter']['Max Filename Length']

    def cache_warm_up_enabled(self) -> bool:
        return self.config['Cache']['Warmup Enabled']
