import pytest
from anki.collection import Collection
from aqt import gui_hooks

from note_size.config.config import Config
from note_size.cache.media_cache import MediaCache
from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from tests.data import Data
from note_size.deck_browser.deck_browser_hooks import DeckBrowserHooks


@pytest.fixture
def deck_browser_hooks(config: Config, collection_size_formatter: CollectionSizeFormatter) -> DeckBrowserHooks:
    deck_browser_hooks = DeckBrowserHooks(collection_size_formatter, config)
    yield deck_browser_hooks
    deck_browser_hooks.remove_hooks()


def test_setup_hooks_enabled(deck_browser_hooks: DeckBrowserHooks):
    assert gui_hooks.deck_browser_will_render_content.count() == 0
    deck_browser_hooks.setup_hooks()
    assert gui_hooks.deck_browser_will_render_content.count() == 1
    deck_browser_hooks.remove_hooks()
    assert gui_hooks.deck_browser_will_render_content.count() == 0


def test_setup_hooks_disabled(col: Collection):
    config: Config = Data.read_config_updated({'Deck Browser': {'Show Full Collection Size': False}})
    media_cache: MediaCache = MediaCache(col, config)
    collection_size_formatter: CollectionSizeFormatter = CollectionSizeFormatter(col, media_cache)
    deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(collection_size_formatter, config)
    assert gui_hooks.deck_browser_will_render_content.count() == 0
    deck_browser_hooks.setup_hooks()
    assert gui_hooks.deck_browser_will_render_content.count() == 0
    deck_browser_hooks.remove_hooks()
    assert gui_hooks.deck_browser_will_render_content.count() == 0
