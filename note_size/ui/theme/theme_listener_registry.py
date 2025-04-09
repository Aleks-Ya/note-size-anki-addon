import logging
from abc import abstractmethod
from logging import Logger

from aqt.theme import ThemeManager

log: Logger = logging.getLogger(__name__)


class ThemeListener:
    @abstractmethod
    def on_theme_changed(self, theme_manager: ThemeManager):
        pass


class ThemeListenerRegistry:
    def __init__(self, theme_manager: ThemeManager) -> None:
        self.__theme_manager: ThemeManager = theme_manager
        self.__listeners: list[ThemeListener] = []
        log.debug(f"{self.__class__.__name__} was instantiated")

    def register(self, listener: ThemeListener) -> None:
        self.__listeners.append(listener)
        log.debug(f"Listener {listener.__class__.__name__} was registered")

    def unregister(self, listener: ThemeListener) -> None:
        self.__listeners.remove(listener)
        log.debug(f"Listener {listener.__class__.__name__} was unregistered")

    def on_theme_changed(self) -> None:
        for listener in self.__listeners:
            listener.on_theme_changed(self.__theme_manager)

    def call_now(self, listener: ThemeListener) -> None:
        listener.on_theme_changed(self.__theme_manager)
