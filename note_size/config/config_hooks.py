import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.qt import qconnect, QAction, QMenu, QDesktopServices, QUrl

from ..ui.config.config_ui import ConfigUi

log: Logger = logging.getLogger(__name__)


class ConfigHooks:

    def __init__(self, config_ui: ConfigUi, desktop_services: QDesktopServices) -> None:
        self.__config_ui: ConfigUi = config_ui
        self.__desktop_services: QDesktopServices = desktop_services
        self.__hook_main_window_did_init: Callable[[], None] = self.__add_deck_browser_menu_item
        self.__hook_browser_will_show: Callable[[Browser], None] = self.__add_browser_menu_item
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.main_window_did_init.append(self.__hook_main_window_did_init)
        gui_hooks.browser_will_show.append(self.__hook_browser_will_show)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.main_window_did_init.remove(self.__hook_main_window_did_init)
        gui_hooks.browser_will_show.remove(self.__hook_browser_will_show)
        log.info(f"{self.__class__.__name__} are removed")

    def __add_browser_menu_item(self, browser: Browser) -> None:
        menu_item: QMenu = self.__menu_item()
        browser.form.menuEdit.addMenu(menu_item)

    def __show_config(self) -> None:
        self.__config_ui.show_configuration_dialog()

    def __open_web_page(self, url: str) -> None:
        self.__desktop_services.openUrl(QUrl(url))

    def __add_deck_browser_menu_item(self) -> None:
        log.debug("Main Window did init")
        menu_item: QMenu = self.__menu_item()
        mw.form.menuTools.addMenu(menu_item)

    def __menu_item(self) -> QMenu:
        open_configuration_action: QAction = QAction("Configuration...", mw)
        qconnect(open_configuration_action.triggered, self.__show_config)

        open_user_manual_action: QAction = QAction("User manual...", mw)
        qconnect(open_user_manual_action.triggered, lambda: self.__open_web_page(
            "https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/user-manual.md"))

        open_addon_page_action: QAction = QAction("Addon page...", mw)
        qconnect(open_addon_page_action.triggered,
                 lambda: self.__open_web_page("https://ankiweb.net/shared/info/1188705668"))

        open_support_page_action: QAction = QAction("Forum support topic...", mw)
        qconnect(open_support_page_action.triggered,
                 lambda: self.__open_web_page("https://forums.ankiweb.net/t/note-size-addon-support/46001"))

        open_change_log_page_action: QAction = QAction("Change log...", mw)
        qconnect(open_change_log_page_action.triggered, lambda: self.__open_web_page(
            "https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/CHANGELOG.md"))

        open_bug_tracker_page_action: QAction = QAction("Bug tracker...", mw)
        qconnect(open_bug_tracker_page_action.triggered,
                 lambda: self.__open_web_page("https://github.com/Aleks-Ya/note-size-anki-addon/issues"))

        open_github_page_action: QAction = QAction("GitHub project...", mw)
        qconnect(open_github_page_action.triggered,
                 lambda: self.__open_web_page("https://github.com/Aleks-Ya/note-size-anki-addon"))

        info_menu: QMenu = QMenu("Info", mw)
        info_menu.addAction(open_user_manual_action)
        info_menu.addAction(open_addon_page_action)
        info_menu.addAction(open_support_page_action)
        info_menu.addAction(open_change_log_page_action)
        info_menu.addAction(open_bug_tracker_page_action)
        info_menu.addAction(open_github_page_action)

        root_menu: QMenu = QMenu("Note Size", mw)
        root_menu.addAction(open_configuration_action)
        root_menu.addMenu(info_menu)
        return root_menu
