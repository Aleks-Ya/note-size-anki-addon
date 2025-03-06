import logging
from logging import Logger
from pathlib import Path

from aqt import ProfileManager

log: Logger = logging.getLogger(__name__)


class Settings:

    def __init__(self, module_dir: Path, module_name: str, logs_folder: Path, profile_manager: ProfileManager) -> None:
        self.module_dir: Path = module_dir
        self.module_name: str = module_name
        self.logs_folder: Path = logs_folder
        caches_dir: Path = self.module_dir / "caches"
        caches_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file: Path = caches_dir / f"{profile_manager.name}.tmp"
        log.debug(f"Cache file: {self.cache_file}")
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(module_dir={self.module_dir}, module_name={self.module_name})"
