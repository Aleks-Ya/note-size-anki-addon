import logging
from logging import Logger
from typing import Any

from aqt import mw
from aqt.mediacheck import check_media_db

from ...config.config import Config
from ...ui.config.config_ui import ConfigUi

log: Logger = logging.getLogger(__name__)


class DeckBrowserJs:
    open_config_action: str = "open-config-action"
    open_check_media_action: str = "open-check-media-action"

    def __init__(self, config: Config, config_ui: ConfigUi):
        self.__config: Config = config
        self.__config_ui: ConfigUi = config_ui
        log.debug(f"{self.__class__.__name__} was instantiated")

    def on_js_message(self, handled: tuple[bool, Any], message: str, _: Any) -> tuple[bool, Any]:
        if message == DeckBrowserJs.open_config_action:
            self.__config_ui.show_configuration_dialog()
            return True, None
        if message == DeckBrowserJs.open_check_media_action:
            check_media_db(mw)
            return True, None
        return handled

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
