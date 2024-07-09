import logging
from logging import Logger
from typing import Optional, Any

from aqt.addons import AddonManager

from ..config.config import Config

log: Logger = logging.getLogger(__name__)


class ConfigLoader:

    def __init__(self, addon_manager: AddonManager, module: str):
        self.__module: str = module
        self.__addon_manager: AddonManager = addon_manager
        log.debug(f"{self.__class__.__name__} was instantiated")

    def load_config(self) -> Config:
        log.debug(f"Loading config for module {self.__module}")
        defaults_opt: Optional[dict[str, Any]] = self.__addon_manager.addonConfigDefaults(self.__module)
        actual_opt: Optional[dict[str, Any]] = self.__addon_manager.getConfig(self.__module)
        joined: dict[str, Any] = Config.join(defaults_opt, actual_opt)
        self.__addon_manager.writeConfig(self.__module, joined)
        config: Config = Config(joined)
        log.info(f"Config was loaded: {config}")
        return config
