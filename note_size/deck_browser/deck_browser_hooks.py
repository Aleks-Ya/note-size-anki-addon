import logging
from logging import Logger
from typing import Callable, Any

from aqt import gui_hooks

from .collection_size_formatter import CollectionSizeFormatter

log: Logger = logging.getLogger(__name__)


class DeckBrowserHooks:

    def __init__(self, collection_size_formatter: CollectionSizeFormatter):
        self.__collection_size_formatter: CollectionSizeFormatter = collection_size_formatter
        self.__hook_deck_browser_will_render_content: Callable[[Any, Any], None] = self.__on_action
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.append(self.__hook_deck_browser_will_render_content)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.remove(self.__hook_deck_browser_will_render_content)
        log.info(f"{self.__class__.__name__} are removed")

    # noinspection PyUnresolvedReferences
    def __on_action(self, _: 'aqt.deckbrowser.DeckBrowser',
                    content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        html: str = self.__collection_size_formatter.format_collection_size_html()
        content.stats += html
        log.info(f"DeckBrowserContent stats (edited): {content.stats}\n\n")
