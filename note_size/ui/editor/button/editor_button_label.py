import logging
from logging import Logger

from ....common.types import ColorName

log: Logger = logging.getLogger(__name__)


class EditorButtonLabel:

    def __init__(self, text: str, background_color: ColorName) -> None:
        self.__text: str = text
        self.__background_color: ColorName = background_color
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_text(self) -> str:
        return self.__text

    def get_background_color(self) -> ColorName:
        return self.__background_color

    def __eq__(self, other) -> bool:
        if isinstance(other, EditorButtonLabel):
            return self.get_text() == other.get_text() and self.get_background_color() == other.get_background_color()
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text='{self.__text}', background_color='{self.__background_color}')"

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
