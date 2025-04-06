import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks
from aqt.theme import ThemeManager

from .theme_listener import ThemeListener
from ..details_dialog.details_dialog import DetailsDialog

log: Logger = logging.getLogger(__name__)


class ThemeHooks:

    def __init__(self, theme_manager: ThemeManager, details_dialog: DetailsDialog) -> None:
        self.__theme_manager: ThemeManager = theme_manager
        self.__listeners: list[ThemeListener] = [details_dialog]
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
        for listener in self.__listeners:
            listener.on_theme_changed(self.__theme_manager)
