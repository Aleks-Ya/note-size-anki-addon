import logging
from logging import Logger

from aqt.qt import QPushButton, QMargins, QIcon
from aqt.theme import ThemeManager

from ..config.config_ui import ConfigUi
from ..theme.theme_listener import ThemeListener
from ...config.settings import Settings

log: Logger = logging.getLogger(__name__)


class ConfigurationButton(QPushButton, ThemeListener):
    def __init__(self, theme_manager: ThemeManager, config_ui: ConfigUi, settings: Settings):
        super().__init__()
        self.__config_ui: ConfigUi = config_ui
        self.__settings_icon_white: QIcon = QIcon(str(settings.module_dir / "ui" / "web" / "setting_white.png"))
        self.__settings_icon_black: QIcon = QIcon(str(settings.module_dir / "ui" / "web" / "setting_black.png"))
        self.on_theme_changed(theme_manager)
        # noinspection PyUnresolvedReferences
        self.setStyleSheet("border: none;")
        # noinspection PyUnresolvedReferences
        self.clicked.connect(self.__on_configuration_button_clicked)
        margin: int = 1
        # noinspection PyUnresolvedReferences
        icon_size: QSize = self.size().shrunkBy(QMargins(margin, margin, margin, margin))
        self.setIconSize(icon_size)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def on_theme_changed(self, theme_manager: ThemeManager):
        is_night_mode: bool = theme_manager.night_mode
        log.debug(f"Theme did changed: is_night_mode={is_night_mode}")
        if is_night_mode:
            icon: QIcon = self.__settings_icon_white
        else:
            icon: QIcon = self.__settings_icon_black
        self.setIcon(icon)
        self.setIconSize(self.sizeHint())
        self.setFixedSize(icon.actualSize(self.iconSize()))

    def __on_configuration_button_clicked(self) -> None:
        self.__config_ui.show_configuration_dialog()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
