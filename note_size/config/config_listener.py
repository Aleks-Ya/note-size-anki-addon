import logging
from abc import ABC, abstractmethod
from logging import Logger

log: Logger = logging.getLogger(__name__)


class ConfigListener(ABC):
    @abstractmethod
    def on_config_changed(self):
        pass
