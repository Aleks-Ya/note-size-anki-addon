import logging
from logging import Logger

from aqt.qt import QDesktopServices

from ...cache.cache_initializer import CacheInitializer
from ...config.config import Config
from ...config.config_loader import ConfigLoader
from ...config.level_parser import LevelParser
from ...config.settings import Settings
from ...config.url_manager import UrlManager
from ...log.logs import Logs
from .config_dialog import ConfigDialog
from .ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class ConfigUi:
    def __init__(self, config: Config, config_loader: ConfigLoader, logs: Logs, cache_initializer: CacheInitializer,
                 desktop_services: QDesktopServices, level_parser: LevelParser, url_manager: UrlManager,
                 settings: Settings) -> None:
        model: UiModel = UiModel()
        self.__dialog: ConfigDialog = ConfigDialog(config, config_loader, model, logs, cache_initializer,
                                                   desktop_services, level_parser, url_manager, settings)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_configuration_dialog(self) -> None:
        self.__dialog.refresh_from_model()
        # noinspection PyUnresolvedReferences
        self.__dialog.show()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
