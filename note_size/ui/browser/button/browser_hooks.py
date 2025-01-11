import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks
from aqt.browser import Browser, SearchContext

from .browser_button import BrowserButton
from .browser_button_manager import BrowserButtonManager
from ....config.config import Config

log: Logger = logging.getLogger(__name__)


class BrowserHooks:

    def __init__(self, browser_button_manager: BrowserButtonManager, config: Config) -> None:
        self.__browser_button_manager: BrowserButtonManager = browser_button_manager
        self.__config: Config = config
        self.__hook_browser_will_show: Callable[[Browser], None] = self.__add_size_button
        self.__hook_browser_did_search: Callable[[SearchContext], None] = self.__update_button
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.browser_will_show.append(self.__hook_browser_will_show)
        gui_hooks.browser_did_search.append(self.__hook_browser_did_search)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.browser_will_show.remove(self.__hook_browser_will_show)
        gui_hooks.browser_did_search.remove(self.__hook_browser_did_search)
        log.info(f"{self.__class__.__name__} are removed")

    def __add_size_button(self, browser: Browser) -> None:
        if self.__config.get_browser_show_found_notes_size():
            log.debug("Add browser size button")
            button: BrowserButton = self.__browser_button_manager.create_browser_button(browser)
            browser.form.gridLayout.addWidget(button, 0, 2)
        else:
            log.debug("Browser size button is disabled")

    def __update_button(self, context: SearchContext) -> None:
        if self.__config.get_browser_show_found_notes_size():
            self.__browser_button_manager.get_current_button().show_items_size(context.ids)
        else:
            log.debug("Browser size button is disabled")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
