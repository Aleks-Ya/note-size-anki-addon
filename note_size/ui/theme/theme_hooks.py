import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks

from ..config.config_ui import ConfigUi
from ..deck_browser.deck_browser_updater import DeckBrowserUpdater
from ..details_dialog.details_dialog import DetailsDialog

log: Logger = logging.getLogger(__name__)


class ThemeHooks:

    def __init__(self, deck_browser_updater: DeckBrowserUpdater, details_dialog: DetailsDialog,
                 config_ui: ConfigUi) -> None:
        self.__deck_browser_updater: DeckBrowserUpdater = deck_browser_updater
        self.__details_dialog: DetailsDialog = details_dialog
        self.__config_ui: ConfigUi = config_ui
        self.__hook_theme_did_changed: Callable[[], None] = self.__theme_did_changed
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.theme_did_change.append(self.__hook_theme_did_changed)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.theme_did_change.remove(self.__hook_theme_did_changed)
        log.info(f"{self.__class__.__name__} are removed")

    def __theme_did_changed(self) -> None:
        log.debug("Theme did changed")
        self.__deck_browser_updater.on_theme_changed()
        self.__details_dialog.on_theme_changed()
        self.__config_ui.on_theme_changed()
