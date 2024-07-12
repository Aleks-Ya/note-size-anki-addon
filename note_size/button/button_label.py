import logging
from logging import Logger

log: Logger = logging.getLogger(__name__)


class ButtonLabel:

    def __init__(self, text: str, background_color: str):
        self.__text: str = text
        self.__background_color: str = background_color
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_text(self) -> str:
        return self.__text

    def get_background_color(self) -> str:
        return self.__background_color

    def __eq__(self, other):
        if isinstance(other, ButtonLabel):
            return self.get_text() == other.get_text() and self.get_background_color() == other.get_background_color()
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}(text='{self.__text}', background_color='{self.__background_color}')"
