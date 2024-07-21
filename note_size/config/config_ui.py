import logging
from logging import Logger

from .config_loader import ConfigLoader
from .settings import Settings
from .ui.config_dialog import ConfigDialog
from .ui.ui_model import UiModel
from ..config.config import Config
from ..log.logs import Logs

log: Logger = logging.getLogger(__name__)


class ConfigUi:
    def __init__(self, config: Config, config_loader: ConfigLoader, logs: Logs, settings: Settings) -> None:
        model: UiModel = UiModel()
        self.__dialog: ConfigDialog = ConfigDialog(config, config_loader, model, logs, settings)

    def show_configuration_dialog(self) -> None:
        self.__dialog.refresh_from_model()
        self.__dialog.show()
