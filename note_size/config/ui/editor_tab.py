import logging
from logging import Logger
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout, QWidget, Qt

from .color_layout import ColorLayout
from .details_window_layout import DetailsWindowLayout
from .widgets import CheckboxWithInfo
from ..settings import Settings
from ...config.ui.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class EditorTab(QWidget):
    name: str = "Editor"

    def __init__(self, model: UiModel, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        url: str = urljoin(settings.docs_base_url, "description/configuration.md#enabled")
        self.__size_button_enabled: CheckboxWithInfo = CheckboxWithInfo("Show note size in Editor", url, settings)
        self.__size_button_enabled.add_checkbox_listener(self.__on_size_button_enabled)
        self.__color_layout: ColorLayout = ColorLayout(self.__model, settings)
        self.__details_window_layout: DetailsWindowLayout = DetailsWindowLayout(self.__model, settings)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__size_button_enabled)
        layout.addLayout(self.__color_layout)
        layout.addLayout(self.__details_window_layout)
        layout.addStretch()
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__size_button_enabled.set_checked(self.__model.size_button_enabled)
        self.__details_window_layout.refresh_from_model()
        self.__color_layout.refresh_from_model()

    def __on_size_button_enabled(self, _: int):
        self.__model.size_button_enabled = self.__size_button_enabled.is_checked()
        self.__details_window_layout.refresh_from_model()
        self.__color_layout.refresh_from_model()
