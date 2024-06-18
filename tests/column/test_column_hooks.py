import tempfile
import unittest

from anki.collection import Collection
from aqt import gui_hooks

from note_size import Config
from note_size.column.column_hooks import ColumnHooks
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from tests.data import Data


class ColumnHooksTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])

    def test_setup_hooks(self):
        self.assertEqual(0, gui_hooks.browser_did_fetch_columns.count())
        self.assertEqual(0, gui_hooks.browser_did_fetch_row.count())
        self.assertEqual(0, gui_hooks.browser_will_search.count())
        self.assertEqual(0, gui_hooks.browser_did_search.count())

        media_cache: MediaCache = MediaCache(self.col)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        config: Config = Data.read_config()
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        column_hooks: ColumnHooks = ColumnHooks(item_id_cache)
        column_hooks.setup_hooks()

        self.assertEqual(1, gui_hooks.browser_did_fetch_columns.count())
        self.assertEqual(1, gui_hooks.browser_did_fetch_row.count())
        self.assertEqual(1, gui_hooks.browser_will_search.count())
        self.assertEqual(1, gui_hooks.browser_did_search.count())

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
