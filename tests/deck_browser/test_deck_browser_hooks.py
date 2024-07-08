import tempfile
import unittest

from anki.collection import Collection
from aqt import gui_hooks

from note_size.config.config import Config
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from tests.data import Data
from note_size.deck_browser.deck_browser_hooks import DeckBrowserHooks


class TestDeckBrowserHooks(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        self.deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(media_cache, item_id_cache)

    def test_setup_hooks(self):
        self.assertEqual(0, gui_hooks.deck_browser_will_render_content.count())
        self.assertEqual(0, gui_hooks.webview_did_receive_js_message.count())

        self.deck_browser_hooks.setup_hooks()
        self.assertEqual(1, gui_hooks.deck_browser_will_render_content.count())
        self.assertEqual(1, gui_hooks.webview_did_receive_js_message.count())

        self.deck_browser_hooks.remove_hooks()
        self.assertEqual(0, gui_hooks.deck_browser_will_render_content.count())
        self.assertEqual(0, gui_hooks.webview_did_receive_js_message.count())

    def tearDown(self):
        self.deck_browser_hooks.remove_hooks()
        self.col.close()


if __name__ == '__main__':
    unittest.main()
