import logging
from logging import Logger
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout, QWidget, Qt, QDesktopServices

from .widgets import CheckboxWithInfo
from ...config.settings import Settings
from ...ui.config.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class BrowserTab(QWidget):
    name: str = "Browser"

    def __init__(self, model: UiModel, desktop_services: QDesktopServices, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        url: str = urljoin(settings.docs_base_url, "docs/configuration.md#show-found-notes-size")
        self.__checkbox: CheckboxWithInfo = CheckboxWithInfo("Show size of notes found in Browser", url,
                                                             desktop_services, settings)
        self.__checkbox.add_checkbox_listener(self.__on_checkbox_state_changed)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__checkbox)
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__checkbox.set_checked(self.__model.browser_show_found_notes_size)

    def __on_checkbox_state_changed(self, _: int):
        self.__model.browser_show_found_notes_size = self.__checkbox.is_checked()
