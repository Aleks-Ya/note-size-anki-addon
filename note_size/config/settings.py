import logging
from logging import Logger
from pathlib import Path

log: Logger = logging.getLogger(__name__)


class Settings:

    def __init__(self, module_dir: Path, module_name: str, logs_folder: Path) -> None:
        self.module_dir: Path = module_dir
        self.module_name: str = module_name
        self.logs_folder: Path = logs_folder
        self.cache_file: Path = self.module_dir.joinpath("cache.tmp")
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(module_dir={self.module_dir}, module_name={self.module_name})"
