import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.qt import qconnect, QAction, QMenu, QDesktopServices, QUrl

from .url_manager import UrlManager, UrlType, URL
from ..ui.config.config_ui import ConfigUi

log: Logger = logging.getLogger(__name__)


class ConfigHooks:

    def __init__(self, config_ui: ConfigUi, desktop_services: QDesktopServices, url_manager: UrlManager) -> None:
        self.__config_ui: ConfigUi = config_ui
        self.__desktop_services: QDesktopServices = desktop_services
        self.__url_manager: UrlManager = url_manager
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

    def __open_web_page(self, url_type: UrlType) -> None:
        url: URL = self.__url_manager.get_url(url_type)
        self.__desktop_services.openUrl(QUrl(url))

    def __add_deck_browser_menu_item(self) -> None:
        log.debug("Main Window did init")
        menu_item: QMenu = self.__menu_item()
        mw.form.menuTools.addMenu(menu_item)

    def __menu_item(self) -> QMenu:
        configuration_action: QAction = QAction("Configuration...", mw)
        qconnect(configuration_action.triggered, self.__show_config)

        user_manual_action: QAction = QAction("User manual...", mw)
        qconnect(user_manual_action.triggered, lambda: self.__open_web_page(UrlType.INFO_USER_MANUAL))

        addon_page_action: QAction = QAction("Addon page...", mw)
        qconnect(addon_page_action.triggered, lambda: self.__open_web_page(UrlType.INFO_ADDON_PAGE))

        support_page_action: QAction = QAction("Forum support topic...", mw)
        qconnect(support_page_action.triggered, lambda: self.__open_web_page(UrlType.INFO_FORUM))

        change_log_page_action: QAction = QAction("Change log...", mw)
        qconnect(change_log_page_action.triggered, lambda: self.__open_web_page(UrlType.INFO_CHANGE_LOG))

        bug_tracker_page_action: QAction = QAction("Bug tracker...", mw)
        qconnect(bug_tracker_page_action.triggered, lambda: self.__open_web_page(UrlType.INFO_BUG_TRACKER))

        github_page_action: QAction = QAction("GitHub project...", mw)
        qconnect(github_page_action.triggered, lambda: self.__open_web_page(UrlType.INFO_GITHUB))

        info_menu: QMenu = QMenu("Info", mw)
        info_menu.addAction(user_manual_action)
        info_menu.addAction(addon_page_action)
        info_menu.addAction(support_page_action)
        info_menu.addAction(change_log_page_action)
        info_menu.addAction(bug_tracker_page_action)
        info_menu.addAction(github_page_action)

        root_menu: QMenu = QMenu("Note Size", mw)
        root_menu.addAction(configuration_action)
        root_menu.addMenu(info_menu)
        return root_menu
