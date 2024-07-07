import tempfile
import unittest

from anki.collection import Collection
from aqt import gui_hooks

from note_size.config.config import Config
from note_size.column.column_hooks import ColumnHooks
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.column.item_id_sorter import ItemIdSorter
from tests.data import Data


class TestColumnHooks(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        item_id_sorter: ItemIdSorter = ItemIdSorter(item_id_cache)
        self.column_hooks: ColumnHooks = ColumnHooks(item_id_cache, item_id_sorter)

    def test_setup_hooks(self):
        self.assertEqual(0, gui_hooks.browser_did_fetch_columns.count())
        self.assertEqual(0, gui_hooks.browser_did_fetch_row.count())
        self.assertEqual(0, gui_hooks.browser_will_search.count())
        self.assertEqual(0, gui_hooks.browser_did_search.count())

        self.column_hooks.setup_hooks()
        self.assertEqual(1, gui_hooks.browser_did_fetch_columns.count())
        self.assertEqual(1, gui_hooks.browser_did_fetch_row.count())
        self.assertEqual(1, gui_hooks.browser_will_search.count())
        self.assertEqual(1, gui_hooks.browser_did_search.count())

        self.column_hooks.remove_hooks()
        self.assertEqual(0, gui_hooks.browser_did_fetch_columns.count())
        self.assertEqual(0, gui_hooks.browser_did_fetch_row.count())
        self.assertEqual(0, gui_hooks.browser_will_search.count())
        self.assertEqual(0, gui_hooks.browser_did_search.count())

    def tearDown(self):
        self.column_hooks.remove_hooks()
        self.col.close()


if __name__ == '__main__':
    unittest.main()
