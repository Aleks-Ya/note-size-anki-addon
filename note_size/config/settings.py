import logging
from logging import Logger
from pathlib import Path

log: Logger = logging.getLogger(__name__)


class Settings:

    def __init__(self, module_dir: Path, module_name: str, logs_folder: Path):
        self.module_dir: Path = module_dir
        self.module_name: str = module_name
        self.logs_folder: Path = logs_folder
        self.docs_base_url: str = "https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/"
        self.cache_file: Path = self.module_dir.joinpath("cache.tmp")
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        return f"{self.__class__.__name__}(module_dir={self.module_dir}, module_name={self.module_name})"
