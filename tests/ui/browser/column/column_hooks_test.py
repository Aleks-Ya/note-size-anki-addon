from typing import Sequence

from anki.collection import BrowserColumns
from anki.notes import Note
from aqt import gui_hooks
from aqt.browser import Column, ItemId, CellRow, SearchContext
from mock.mock import MagicMock

from note_size.common.collection_holder import CollectionHolder
from note_size.ui.browser.column.column_hooks import ColumnHooks
from tests.conftest import assert_no_hooks
from tests.data import Data, DefaultFields


def test_setup_hooks(td: Data, column_hooks: ColumnHooks):
    assert_no_hooks()
    column_hooks.setup_hooks()
    assert gui_hooks.browser_did_fetch_columns.count() == 1
    assert gui_hooks.browser_did_fetch_row.count() == 1
    assert gui_hooks.browser_will_search.count() == 1
    assert gui_hooks.browser_did_search.count() == 1
    column_hooks.remove_hooks()
    assert_no_hooks()


def test_add_columns(column_hooks: ColumnHooks):
    column_hooks.setup_hooks()
    columns: dict[str, Column] = {}
    gui_hooks.browser_did_fetch_columns(columns)
    assert columns == {
        "note-size-total": Column(
            key="note-size-total",
            cards_mode_label="Size",
            notes_mode_label="Size",
            sorting_cards=BrowserColumns.SORTING_DESCENDING,
            sorting_notes=BrowserColumns.SORTING_DESCENDING,
            uses_cell_font=False,
            alignment=BrowserColumns.ALIGNMENT_CENTER,
            cards_mode_tooltip="Note size (texts and files are included)",
            notes_mode_tooltip="Note size (texts and files are included)"
        ),
        "note-size-texts": Column(
            key="note-size-texts",
            cards_mode_label="Size (texts)",
            notes_mode_label="Size (texts)",
            sorting_cards=BrowserColumns.SORTING_DESCENDING,
            sorting_notes=BrowserColumns.SORTING_DESCENDING,
            uses_cell_font=False,
            alignment=BrowserColumns.ALIGNMENT_CENTER,
            cards_mode_tooltip="Note size (texts only, files are not included)",
            notes_mode_tooltip="Note size (texts only, files are not included)"
        ),
        "note-size-files": Column(
            key="note-size-files",
            cards_mode_label="Size (files)",
            notes_mode_label="Size (files)",
            sorting_cards=BrowserColumns.SORTING_DESCENDING,
            sorting_notes=BrowserColumns.SORTING_DESCENDING,
            uses_cell_font=False,
            alignment=BrowserColumns.ALIGNMENT_CENTER,
            cards_mode_tooltip="Note size (files only, texts are not included)",
            notes_mode_tooltip="Note size (files only, texts are not included)"
        )
    }


def test_modify_row(td: Data, column_hooks: ColumnHooks):
    column_hooks.setup_hooks()
    note: Note = td.create_note_with_files()
    item_id: ItemId = note.id
    is_note: bool = True
    init_text: str = "init text"
    row: CellRow = CellRow.generic(4, init_text)
    columns: Sequence[str] = ["English", "note-size-total", "note-size-texts", "note-size-files"]
    gui_hooks.browser_did_fetch_row(item_id, is_note, row, columns)
    cells: list[str] = [f"{cell.text} - {cell.is_rtl}" for cell in row.cells]
    assert cells == [
        "init text - False",
        "143 B - False",
        "122 B - False",
        "21 B - False"
    ]


def test_sort_rows_by_column(td: Data, column_hooks: ColumnHooks, collection_holder: CollectionHolder):
    column_hooks.setup_hooks()
    note_big: Note = td.create_note_with_given_fields("big big big")
    note_medium: Note = td.create_note_with_given_fields("medium")
    note_small: Note = td.create_note_with_given_fields("small")
    browser: MagicMock = MagicMock()
    column: Column = Column(key="note-size-total", notes_mode_label="Size")
    ids: Sequence[ItemId] = [note_medium.id, note_big.id, note_small.id]
    search_context: SearchContext = SearchContext("", browser, column, False, ids=ids)
    gui_hooks.browser_did_search(search_context)
    assert search_context.ids
    act_notes: list[str] = [collection_holder.col().get_note(note_id)[DefaultFields.front_field_name]
                            for note_id in search_context.ids]
    exp_notes: list[str] = [note_big[DefaultFields.front_field_name],
                            note_medium[DefaultFields.front_field_name],
                            note_small[DefaultFields.front_field_name]]
    assert act_notes == exp_notes
