import logging
from logging import Logger
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout, QWidget, Qt

from .widgets import CheckboxWithInfo
from ..settings import Settings
from ...config.ui.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class DeckBrowserTab(QWidget):
    name: str = "Deck Browser"

    def __init__(self, model: UiModel, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        url: str = urljoin(settings.docs_base_url, "docs/configuration.md#show-collection-size")
        self.__checkbox: CheckboxWithInfo = CheckboxWithInfo("Show collection size in Deck Browser", url, settings)
        self.__checkbox.add_checkbox_listener(self.__on_checkbox_state_changed)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__checkbox)
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__checkbox.set_checked(self.__model.deck_browser_show_collection_size)

    def __on_checkbox_state_changed(self, _: int):
        self.__model.deck_browser_show_collection_size = self.__checkbox.is_checked()
