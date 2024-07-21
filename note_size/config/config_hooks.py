import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.qt import qconnect, QAction, QMenu

from ..config.config_ui import ConfigUi

log: Logger = logging.getLogger(__name__)


class ConfigHooks:

    def __init__(self, config_ui: ConfigUi):
        self.__config_ui: ConfigUi = config_ui
        self.__hook_main_window_did_init: Callable[[], None] = self.__add_deck_browser_menu_item
        self.__hook_browser_will_show: Callable[[Browser], None] = self.__add_browser_menu_item
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __add_browser_menu_item(self, browser: Browser) -> None:
        menu_item: QMenu = self.__menu_item()
        browser.form.menuEdit.addMenu(menu_item)

    def setup_hooks(self) -> None:
        gui_hooks.main_window_did_init.append(self.__hook_main_window_did_init)
        gui_hooks.browser_will_show.append(self.__hook_browser_will_show)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.main_window_did_init.remove(self.__hook_main_window_did_init)
        gui_hooks.browser_will_show.remove(self.__hook_browser_will_show)
        log.info(f"{self.__class__.__name__} are removed")

    def __show_config(self):
        self.__config_ui.show_configuration_dialog()

    def __add_deck_browser_menu_item(self) -> None:
        log.debug("Main Window did init")
        menu_item: QMenu = self.__menu_item()
        mw.form.menuTools.addMenu(menu_item)

    def __menu_item(self) -> QMenu:
        parent_menu: QMenu = QMenu("Note Size", mw)
        child_action: QAction = QAction("Configuration...", mw)
        qconnect(child_action.triggered, self.__show_config)
        parent_menu.addAction(child_action)
        return parent_menu
