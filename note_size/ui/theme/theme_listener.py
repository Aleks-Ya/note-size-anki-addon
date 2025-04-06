import logging
from abc import abstractmethod
from logging import Logger

log: Logger = logging.getLogger(__name__)


class ThemeListener:
    @abstractmethod
    def on_theme_changed(self):
        pass
