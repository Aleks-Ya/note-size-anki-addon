import tempfile
import unittest
from typing import Sequence

from anki.collection import Collection, BrowserColumns
from anki.notes import Note
from aqt import gui_hooks
from aqt.browser import Column, ItemId, CellRow, Cell, SearchContext
from mock.mock import MagicMock

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
        self.td: Data = Data(self.col)
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        self.size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, self.size_calculator, config)
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

    def test_modify_row(self):
        self.column_hooks.setup_hooks()
        note: Note = self.td.create_note_with_files()
        item_id: ItemId = note.id
        is_note: bool = True
        init_text: str = "init text"
        row: CellRow = CellRow.generic(4, init_text)
        columns: Sequence[str] = ["English", "note-size-total", "note-size-texts", "note-size-files"]
        gui_hooks.browser_did_fetch_row(item_id, is_note, row, columns)
        self.assertTupleEqual((
            Cell(init_text, False),
            Cell("143B", False),
            Cell("122B", False),
            Cell("21B", False)
        ), row.cells)

    def test_sort_rows_by_column(self):
        self.column_hooks.setup_hooks()
        note_big: Note = self.td.create_note_with_given_fields("big big big")
        note_medium: Note = self.td.create_note_with_given_fields("medium")
        note_small: Note = self.td.create_note_with_given_fields("small")
        browser: MagicMock = MagicMock()
        column: Column = Column(key="note-size-total", notes_mode_label="Size")
        ids: Sequence[ItemId] = [note_medium.id, note_big.id, note_small.id]
        search_context: SearchContext = SearchContext("", browser, column, False, ids)
        gui_hooks.browser_did_search(search_context)
        self.assertSequenceEqual([note_big.id, note_medium.id, note_small.id], search_context.ids)

    def tearDown(self):
        self.column_hooks.remove_hooks()
        self.col.close()


if __name__ == '__main__':
    unittest.main()
