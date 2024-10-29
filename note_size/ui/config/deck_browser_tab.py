import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QWidget, Qt, QDesktopServices

from .widgets import CheckboxWithInfo
from ...config.settings import Settings
from ...config.url_manager import UrlManager, UrlType
from ...ui.config.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class DeckBrowserTab(QWidget):
    name: str = "Deck Browser"

    def __init__(self, model: UiModel, desktop_services: QDesktopServices, url_manager: UrlManager, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        url: str = url_manager.get_url(UrlType.CONFIGURATION_DECK_BROWSER_SHOW_COLLECTION_SIZE)
        self.__checkbox: CheckboxWithInfo = CheckboxWithInfo(
            "Show collection size in Deck Browser", url, desktop_services, settings)
        self.__checkbox.add_checkbox_listener(self.__on_checkbox_state_changed)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__checkbox)
        self.setLayout(layout)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def refresh_from_model(self):
        self.__checkbox.set_checked(self.__model.deck_browser_show_collection_size)

    def __on_checkbox_state_changed(self, _: int):
        self.__model.deck_browser_show_collection_size = self.__checkbox.is_checked()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
