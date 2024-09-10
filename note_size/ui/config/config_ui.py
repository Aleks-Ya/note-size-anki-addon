import logging
from logging import Logger

from aqt.qt import QDesktopServices

from ...cache.cache_initializer import CacheInitializer
from ...config.config import Config
from ...config.config_loader import ConfigLoader
from ...config.settings import Settings
from ...log.logs import Logs
from .config_dialog import ConfigDialog
from .ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class ConfigUi:
    def __init__(self, config: Config, config_loader: ConfigLoader, logs: Logs, cache_updater: CacheInitializer,
                 desktop_services: QDesktopServices, settings: Settings) -> None:
        model: UiModel = UiModel()
        self.__dialog: ConfigDialog = ConfigDialog(config, config_loader, model, logs, cache_updater, desktop_services,
                                                   settings)

    def show_configuration_dialog(self) -> None:
        self.__dialog.refresh_from_model()
        # noinspection PyUnresolvedReferences
        self.__dialog.show()
