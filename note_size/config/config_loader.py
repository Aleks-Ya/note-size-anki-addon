import logging
from logging import Logger
from typing import Optional, Any

from aqt.addons import AddonManager

from ..config.config import Config
from ..config.settings import Settings

log: Logger = logging.getLogger(__name__)


class ConfigLoader:

    def __init__(self, addon_manager: AddonManager, settings: Settings) -> None:
        self.__module_name: str = settings.module_name
        self.__addon_manager: AddonManager = addon_manager
        log.debug(f"{self.__class__.__name__} was instantiated")

    def load_config(self) -> Config:
        log.debug(f"Loading config for module {self.__module_name}")
        defaults_opts: Optional[dict[str, Any]] = self.get_defaults()
        actual_opt: Optional[dict[str, Any]] = self.__addon_manager.getConfig(self.__module_name)
        joined: dict[str, Any] = Config.join(defaults_opts, actual_opt)
        self.__addon_manager.writeConfig(self.__module_name, joined)
        config: Config = Config(joined)
        log.info(f"Config was loaded: {config}")
        return config

    def get_defaults(self) -> Optional[dict[str, Any]]:
        return self.__addon_manager.addonConfigDefaults(self.__module_name)

    def write_config(self, config: Config) -> None:
        self.__addon_manager.writeConfig(self.__module_name, config.get_as_dict())
