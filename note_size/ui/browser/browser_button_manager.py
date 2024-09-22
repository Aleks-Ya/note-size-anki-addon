import logging
from logging import Logger

from anki.collection import Collection

from .browser_button import BrowserButton
from ..details_dialog.details_dialog import DetailsDialog
from ...cache.item_id_cache import ItemIdCache

log: Logger = logging.getLogger(__name__)


class BrowserButtonManager:

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, details_dialog: DetailsDialog) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__details_dialog: DetailsDialog = details_dialog
        self.__button: BrowserButton = BrowserButton(self.__col, self.__item_id_cache, self.__details_dialog)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_browser_button(self) -> BrowserButton:
        self.__button = BrowserButton(self.__col, self.__item_id_cache, self.__details_dialog)
        return self.__button

    def get_current_button(self) -> BrowserButton:
        return self.__button
