import logging
from logging import Logger
from typing import Optional, Any

from aqt.addons import AddonManager

from ..config.config import Config

log: Logger = logging.getLogger(__name__)


class ConfigLoader:

    def __init__(self, addon_manager: AddonManager, module: str):
        self.module: str = module
        self.addon_manager: AddonManager = addon_manager
        log.debug(f"{self.__class__.__name__} was instantiated")

    def load_config(self) -> Config:
        log.debug(f"Loading config for module {self.module}")
        defaults_opt: Optional[dict[str, Any]] = self.addon_manager.addonConfigDefaults(self.module)
        actual_opt: Optional[dict[str, Any]] = self.addon_manager.getConfig(self.module)
        joined: dict[str, Any] = self.__update_dict_recursive_if_present(defaults_opt, actual_opt)
        self.addon_manager.writeConfig(self.module, joined)
        config: Config = Config(joined)
        log.info(f"Config was loaded: {config}")
        return config

    def __update_dict_recursive_if_present(self, base: Optional[dict[str, Any]], actual: Optional[dict[str, Any]]) \
            -> dict[str, Any]:
        base: dict[str, Any] = dict(base if base else {})
        actual: dict[str, Any] = actual if actual else {}
        for k, v in actual.items():
            if k in base:
                if isinstance(v, dict):
                    base[k] = self.__update_dict_recursive_if_present(base.get(k, {}), v)
                else:
                    base[k] = v
        return base
