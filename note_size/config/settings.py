import logging
from logging import Logger
from pathlib import Path

log: Logger = logging.getLogger(__name__)


class Settings:

    def __init__(self, addon_dir: Path, module: str, logs_folder: Path, addon_package: str):
        self.__addon_dir: Path = addon_dir
        self.__module: str = module
        self.__logs_folder: Path = logs_folder
        self.__addon_package: str = addon_package
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        return f"{self.__class__.__name__}(addon_dir={self.__addon_dir}, module={self.__module})"

    def addon_dir(self) -> Path:
        return self.__addon_dir

    def module(self) -> str:
        return self.__module

    def logs_folder(self) -> Path:
        return self.__logs_folder

    def addon_package(self) -> str:
        return self.__addon_package
