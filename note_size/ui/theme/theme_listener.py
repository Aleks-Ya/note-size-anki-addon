import logging
from abc import abstractmethod
from logging import Logger

from aqt.theme import ThemeManager

log: Logger = logging.getLogger(__name__)


class ThemeListener:
    @abstractmethod
    def on_theme_changed(self, theme_manager: ThemeManager):
        pass
