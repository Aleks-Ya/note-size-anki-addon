import logging
from logging import Logger

from aqt.qt import QPushButton, QMargins, QIcon

from ..config.config_ui import ConfigUi
from ...config.settings import Settings

log: Logger = logging.getLogger(__name__)


class ConfigurationButton(QPushButton):
    def __init__(self, config_ui: ConfigUi, settings: Settings):
        super().__init__()
        self.__config_ui: ConfigUi = config_ui
        self.__settings_icon: QIcon = QIcon(str(settings.module_dir / "ui" / "web" / "setting.png"))
        self.setIcon(self.__settings_icon)
        self.setIconSize(self.sizeHint())
        self.setFixedSize(self.__settings_icon.actualSize(self.iconSize()))
        # noinspection PyUnresolvedReferences
        self.setStyleSheet("border: none;")
        # noinspection PyUnresolvedReferences
        self.clicked.connect(self.__on_configuration_button_clicked)
        margin: int = 1
        # noinspection PyUnresolvedReferences
        icon_size: QSize = self.size().shrunkBy(QMargins(margin, margin, margin, margin))
        self.setIconSize(icon_size)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_configuration_button_clicked(self) -> None:
        self.__config_ui.show_configuration_dialog()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
