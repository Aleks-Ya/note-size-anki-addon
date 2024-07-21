import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QWidget, Qt

from .widgets import CheckboxWithInfo
from ..settings import Settings
from ...config.ui.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class CacheTab(QWidget):
    name: str = "Cache"

    def __init__(self, model: UiModel, settings: Settings) -> None:
        super().__init__()
        self.__model: UiModel = model
        url: str = "https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/description/configuration.md#warmup-enabled"
        self.__checkbox: CheckboxWithInfo = CheckboxWithInfo("Enable cache warm-up", url, settings)
        self.__checkbox.add_checkbox_listener(self.__on_checkbox_state_changed)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__checkbox)
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__checkbox.set_checked(self.__model.cache_warmup_enabled)

    def __on_checkbox_state_changed(self, cache_warm_up_enabled: bool):
        self.__model.cache_warmup_enabled = cache_warm_up_enabled
