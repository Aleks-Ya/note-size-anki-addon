import logging
from logging import Logger
from typing import Callable, Any

from aqt import gui_hooks

from .deck_browser_js import DeckBrowserJs
from .deck_browser_updater import DeckBrowserUpdater

log: Logger = logging.getLogger(__name__)


class DeckBrowserHooks:

    def __init__(self, deck_browser_updater: DeckBrowserUpdater, deck_browser_js: DeckBrowserJs):
        self.__hook_deck_browser_will_render_content: Callable[
            [Any, Any], None] = deck_browser_updater.on_browser_will_render_content
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

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
