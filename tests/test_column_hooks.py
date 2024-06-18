import tempfile
import unittest

from anki.collection import Collection
from aqt import gui_hooks

from note_size import ColumnHooks, ItemIdCache, SizeCalculator, MediaCache


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
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator)
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
