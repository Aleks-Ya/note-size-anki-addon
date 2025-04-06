import logging
from logging import Logger
from typing import Callable, Any

from aqt import gui_hooks

from .collection_size_formatter import CollectionSizeFormatter
from .deck_browser_js import DeckBrowserJs
from ...config.config import Config

log: Logger = logging.getLogger(__name__)


class DeckBrowserHooks:

    def __init__(self, collection_size_formatter: CollectionSizeFormatter, deck_browser_js: DeckBrowserJs,
                 config: Config):
        self.__config: Config = config
        self.__collection_size_formatter: CollectionSizeFormatter = collection_size_formatter
        self.__hook_deck_browser_will_render_content: Callable[[Any, Any], None] = self.__on_browser_will_render_content
        self.__hook_webview_did_receive_js_message: Callable[
            [tuple[bool, Any], str, Any], tuple[bool, Any]] = deck_browser_js.on_js_message
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.append(self.__hook_deck_browser_will_render_content)
        gui_hooks.webview_did_receive_js_message.append(self.__hook_webview_did_receive_js_message)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.remove(self.__hook_deck_browser_will_render_content)
        gui_hooks.webview_did_receive_js_message.remove(self.__hook_webview_did_receive_js_message)
        log.info(f"{self.__class__.__name__} are removed")

    # noinspection PyUnresolvedReferences
    def __on_browser_will_render_content(self, _: 'aqt.deckbrowser.DeckBrowser',
                                         content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        if self.__config.get_deck_browser_show_collection_size():
            html: str = self.__collection_size_formatter.format_collection_size_html()
            content.stats += html
            log.debug(f"DeckBrowserContent stats (edited): {content.stats}")
        else:
            log.debug("Showing collection size in DeckBrowser is disabled")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
