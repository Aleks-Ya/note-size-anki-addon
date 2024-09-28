import logging
from logging import Logger
from typing import Optional

from anki.collection import Collection
from aqt.browser import Browser

from .browser_button import BrowserButton
from ..details_dialog.details_dialog import DetailsDialog
from ...cache.item_id_cache import ItemIdCache
from ...cache.size_str_cache import SizeStrCache

log: Logger = logging.getLogger(__name__)


class BrowserButtonManager:

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, size_str_cache: SizeStrCache,
                 details_dialog: DetailsDialog) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_str_cache: SizeStrCache = size_str_cache
        self.__details_dialog: DetailsDialog = details_dialog
        self.__button: Optional[BrowserButton] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_browser_button(self, browser: Browser) -> BrowserButton:
        self.__button = BrowserButton(self.__col, self.__item_id_cache, self.__size_str_cache, self.__details_dialog,
                                      browser)
        return self.__button

    def get_current_button(self) -> BrowserButton:
        return self.__button
