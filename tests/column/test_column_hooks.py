import tempfile
import unittest

from anki.collection import Collection, BrowserColumns
from aqt import gui_hooks
from aqt.browser import Column

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

    def test_add_columns(self):
        self.column_hooks.setup_hooks()
        columns: dict[str, Column] = {}
        gui_hooks.browser_did_fetch_columns(columns)
        self.assertDictEqual(columns, {
            "note-size-total": Column(
                key="note-size-total",
                cards_mode_label="Size",
                notes_mode_label="Size",
                sorting_cards=BrowserColumns.SORTING_DESCENDING,
                sorting_notes=BrowserColumns.SORTING_DESCENDING,
                uses_cell_font=True,
                cards_mode_tooltip="Note size (texts and files are included)",
                notes_mode_tooltip="Note size (texts and files are included)"
            ),
            "note-size-texts": Column(
                key="note-size-texts",
                cards_mode_label="Size (texts)",
                notes_mode_label="Size (texts)",
                sorting_cards=BrowserColumns.SORTING_DESCENDING,
                sorting_notes=BrowserColumns.SORTING_DESCENDING,
                uses_cell_font=True,
                cards_mode_tooltip="Note size (texts only, files are not included)",
                notes_mode_tooltip="Note size (texts only, files are not included)"
            ),
            "note-size-files": Column(
                key="note-size-files",
                cards_mode_label="Size (files)",
                notes_mode_label="Size (files)",
                sorting_cards=BrowserColumns.SORTING_DESCENDING,
                sorting_notes=BrowserColumns.SORTING_DESCENDING,
                uses_cell_font=True,
                cards_mode_tooltip="Note size (files only, texts are not included)",
                notes_mode_tooltip="Note size (files only, texts are not included)"
            )
        })

    def tearDown(self):
        self.column_hooks.remove_hooks()
        self.col.close()


if __name__ == '__main__':
    unittest.main()
