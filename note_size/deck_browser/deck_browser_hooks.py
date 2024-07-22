import logging
from logging import Logger
from typing import Callable, Any

from aqt import gui_hooks

from .collection_size_formatter import CollectionSizeFormatter
from ..config.config import Config

log: Logger = logging.getLogger(__name__)


class DeckBrowserHooks:

    def __init__(self, collection_size_formatter: CollectionSizeFormatter, config: Config):
        self.__enabled: bool = config.deck_browser_show_collection_size()
        self.__collection_size_formatter: CollectionSizeFormatter = collection_size_formatter
        self.__hook_deck_browser_will_render_content: Callable[[Any, Any], None] = self.__on_action
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        if self.__enabled:
            gui_hooks.deck_browser_will_render_content.append(self.__hook_deck_browser_will_render_content)
            log.info(f"{self.__class__.__name__} are set")
        else:
            log.info(f"Showing collection size in DeckBrowser is disabled")

    def remove_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.remove(self.__hook_deck_browser_will_render_content)
        log.info(f"{self.__class__.__name__} are removed")

    # noinspection PyUnresolvedReferences
    def __on_action(self, _: 'aqt.deckbrowser.DeckBrowser',
                    content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        html: str = self.__collection_size_formatter.format_collection_size_html()
        content.stats += html
        log.debug(f"DeckBrowserContent stats (edited): {content.stats}\n\n")
