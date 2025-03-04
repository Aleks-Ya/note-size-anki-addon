import logging
from logging import Logger
from typing import Optional

import aqt
from aqt.browser import Browser
from aqt.progress import ProgressManager

from .browser_button import BrowserButton
from ....ui.details_dialog.details_dialog import DetailsDialog
from ....cache.item_id_cache import ItemIdCache
from ....cache.size_str_cache import SizeStrCache
from ....config.config import Config
from ....config.config_listener import ConfigListener

log: Logger = logging.getLogger(__name__)


class BrowserButtonManager(ConfigListener):

    def __init__(self, item_id_cache: ItemIdCache, size_str_cache: SizeStrCache, details_dialog: DetailsDialog,
                 progress_manager: ProgressManager, config: Config) -> None:
        super().__init__()
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_str_cache: SizeStrCache = size_str_cache
        self.__details_dialog: DetailsDialog = details_dialog
        self.__progress_manager: ProgressManager = progress_manager
        self.__config: Config = config
        self.__button: Optional[BrowserButton] = None
        self.__config.add_listener(self)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_browser_button(self, browser: Browser) -> BrowserButton:
        self.__button = BrowserButton(self.__item_id_cache, self.__size_str_cache, self.__details_dialog,
                                      browser, self.__progress_manager, self.__config)
        return self.__button

    def get_current_button(self) -> BrowserButton:
        return self.__button

    def on_config_changed(self):
        log.debug(f"On config changed: {self.__config.get_browser_show_found_notes_size()}")
        is_browser_open: bool = aqt.dialogs._dialogs["Browser"][1] is not None
        log.debug(f"Browser is open: {is_browser_open}")
        if is_browser_open and self.__button:
            if self.__config.get_browser_show_found_notes_size():
                # noinspection PyUnresolvedReferences
                self.__button.show()
            else:
                self.__button.hide()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
