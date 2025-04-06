import logging
from logging import Logger

from aqt.deckbrowser import DeckBrowser
from aqt.theme import ThemeManager

from .collection_size_formatter import CollectionSizeFormatter
from ..theme.theme_listener import ThemeListener
from ...config.config import Config

log: Logger = logging.getLogger(__name__)


class DeckBrowserUpdater(ThemeListener):
    def __init__(self, deck_browser: DeckBrowser, collection_size_formatter: CollectionSizeFormatter, config: Config):
        self.__collection_size_formatter: CollectionSizeFormatter = collection_size_formatter
        self.__deck_browser: DeckBrowser = deck_browser
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    # noinspection PyUnresolvedReferences
    def on_browser_will_render_content(self, _: 'aqt.deckbrowser.DeckBrowser',
                                       content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        if self.__config.get_deck_browser_show_collection_size():
            html: str = self.__collection_size_formatter.format_collection_size_html()
            content.stats += html
            log.debug(f"DeckBrowserContent stats (edited): {content.stats}")
        else:
            log.debug("Showing collection size in DeckBrowser is disabled")

    def on_theme_changed(self, theme_manager: ThemeManager):
        log.debug(f"Theme did changed")
        self.__deck_browser.refresh()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
