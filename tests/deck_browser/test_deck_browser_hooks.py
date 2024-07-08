import tempfile
import unittest

from anki.collection import Collection
from aqt import gui_hooks

from note_size.config.config import Config
from note_size.cache.media_cache import MediaCache
from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from tests.data import Data
from note_size.deck_browser.deck_browser_hooks import DeckBrowserHooks


class TestDeckBrowserHooks(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        collection_size_formatter: CollectionSizeFormatter = CollectionSizeFormatter(self.col, media_cache)
        self.deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(collection_size_formatter)

    def test_setup_hooks(self):
        self.assertEqual(0, gui_hooks.deck_browser_will_render_content.count())

        self.deck_browser_hooks.setup_hooks()
        self.assertEqual(1, gui_hooks.deck_browser_will_render_content.count())

        self.deck_browser_hooks.remove_hooks()
        self.assertEqual(0, gui_hooks.deck_browser_will_render_content.count())

    def tearDown(self):
        self.deck_browser_hooks.remove_hooks()
        self.col.close()


if __name__ == '__main__':
    unittest.main()
