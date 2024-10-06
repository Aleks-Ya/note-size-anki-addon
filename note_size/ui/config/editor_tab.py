import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QWidget, Qt, QDesktopServices

from .color_layout import ColorLayout
from .widgets import CheckboxWithInfo
from ...config.level_parser import LevelParser
from ...config.settings import Settings
from ...config.url_manager import UrlManager, UrlType
from ...ui.config.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class EditorTab(QWidget):
    name: str = "Editor"

    def __init__(self, model: UiModel, desktop_services: QDesktopServices, level_parser: LevelParser,
                 url_manager: UrlManager, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        url: str = url_manager.get_url(UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_ENABLED)
        self.__size_button_enabled: CheckboxWithInfo = CheckboxWithInfo(
            "Show note size in Editor", url, desktop_services, settings)
        self.__size_button_enabled.add_checkbox_listener(self.__on_size_button_enabled)
        self.__color_layout: ColorLayout = ColorLayout(
            self.__model, desktop_services, level_parser, url_manager, settings)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__size_button_enabled)
        layout.addLayout(self.__color_layout)
        layout.addStretch()
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__size_button_enabled.set_checked(self.__model.size_button_enabled)
        self.__color_layout.refresh_from_model()

    def __on_size_button_enabled(self, _: int):
        self.__model.size_button_enabled = self.__size_button_enabled.is_checked()
        self.__color_layout.refresh_from_model()
