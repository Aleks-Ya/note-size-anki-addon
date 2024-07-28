import logging
from logging import Logger
from pathlib import Path

log: Logger = logging.getLogger(__name__)


class Settings:

    def __init__(self, module_dir: Path, module_name: str, logs_folder: Path):
        self.__module_dir: Path = module_dir
        self.__module_name: str = module_name
        self.__logs_folder: Path = logs_folder
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        return f"{self.__class__.__name__}(module_dir={self.__module_dir}, module_name={self.__module_name})"

    def module_dir(self) -> Path:
        return self.__module_dir

    def module_name(self) -> str:
        return self.__module_name

    def logs_folder(self) -> Path:
        return self.__logs_folder
