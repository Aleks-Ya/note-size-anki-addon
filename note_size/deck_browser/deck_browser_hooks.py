import logging
from logging import Logger
from typing import Callable, Any

from aqt import gui_hooks, mw
from aqt.mediacheck import check_media_db

from .collection_size_formatter import CollectionSizeFormatter
from .js_actions import JsActions
from ..config.config import Config
from ..config.config_ui import ConfigUi

log: Logger = logging.getLogger(__name__)


class DeckBrowserHooks:

    def __init__(self, collection_size_formatter: CollectionSizeFormatter, config: Config, config_ui: ConfigUi):
        self.__config: Config = config
        self.__collection_size_formatter: CollectionSizeFormatter = collection_size_formatter
        self.__config_ui: ConfigUi = config_ui
        self.__hook_deck_browser_will_render_content: Callable[[Any, Any], None] = self.__on_action
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.append(self.__hook_deck_browser_will_render_content)
        gui_hooks.webview_did_receive_js_message.append(self.__on_js_message)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.remove(self.__hook_deck_browser_will_render_content)
        log.info(f"{self.__class__.__name__} are removed")

    # noinspection PyUnresolvedReferences
    def __on_action(self, _: 'aqt.deckbrowser.DeckBrowser',
                    content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        if self.__config.get_deck_browser_show_collection_size():
            html: str = self.__collection_size_formatter.format_collection_size_html()
            content.stats += html
            log.debug(f"DeckBrowserContent stats (edited): {content.stats}\n\n")
        else:
            log.debug(f"Showing collection size in DeckBrowser is disabled")

    def __on_js_message(self, handled: tuple[bool, Any], message: str, _: Any) -> tuple[bool, Any]:
        if message == JsActions.open_config_action:
            self.__config_ui.show_configuration_dialog()
            return True, None
        if message == JsActions.open_check_media_action:
            check_media_db(mw)
            return True, None
        return handled
