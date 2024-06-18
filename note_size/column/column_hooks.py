import logging
from logging import Logger
from typing import Sequence, Optional, Callable

from anki.collection import BrowserColumns
from anki.notes import NoteId
from aqt import gui_hooks, mw
from aqt.browser import Column, Cell, SearchContext
from aqt.browser import ItemId, CellRow

from ..cache.item_id_cache import ItemIdCache
from ..types import SizeBytes, SizeType

log: Logger = logging.getLogger(__name__)


class ColumnHooks:
    column_total_key: str = "note-size-total"
    column_total_label: str = "Size"
    column_texts_key: str = "note-size-texts"
    column_texts_label: str = "Size (texts)"
    column_files_key: str = "note-size-files"
    column_files_label: str = "Size (files)"

    def __init__(self, item_id_cache: ItemIdCache):
        self.item_id_cache: ItemIdCache = item_id_cache

    def setup_hooks(self):
        gui_hooks.browser_did_fetch_columns.append(ColumnHooks._add_custom_column)
        gui_hooks.browser_did_fetch_row.append(self._modify_row)
        gui_hooks.browser_will_search.append(ColumnHooks._on_browser_will_search)
        gui_hooks.browser_did_search.append(self._on_browser_did_search)
        log.info("Size column hooks are set")

    @staticmethod
    def _add_custom_column(columns: dict[str, Column]) -> None:
        ColumnHooks._add_column(columns, ColumnHooks.column_total_key, ColumnHooks.column_total_label,
                                "Note size (texts and files are included)")
        ColumnHooks._add_column(columns, ColumnHooks.column_texts_key, ColumnHooks.column_texts_label,
                                "Note size (texts only, files are not included)")
        ColumnHooks._add_column(columns, ColumnHooks.column_files_key, ColumnHooks.column_files_label,
                                "Note size (files only, texts are not included)")
        log.info("Columns were added")

    @staticmethod
    def _add_column(columns: dict[str, Column], column_key: str, column_label: str, tooltip_total: str) -> None:
        columns[column_key] = Column(
            key=column_key,
            cards_mode_label=column_label,
            notes_mode_label=column_label,
            sorting_cards=BrowserColumns.SORTING_DESCENDING,
            sorting_notes=BrowserColumns.SORTING_DESCENDING,
            uses_cell_font=True,
            alignment=BrowserColumns.ALIGNMENT_START,
            cards_mode_tooltip=tooltip_total,
            notes_mode_tooltip=tooltip_total,
        )

    def _modify_row(self, item_id: ItemId, is_note: bool, row: CellRow, columns: Sequence[str]) -> None:
        note_id: NoteId = item_id if is_note else self.item_id_cache.get_note_id_by_card_id(item_id)
        self._update_row(columns, note_id, row, ColumnHooks.column_total_key, ItemIdCache.TOTAL_SIZE)
        self._update_row(columns, note_id, row, ColumnHooks.column_texts_key, ItemIdCache.TEXTS_SIZE)
        self._update_row(columns, note_id, row, ColumnHooks.column_files_key, ItemIdCache.FILES_SIZE)

    def _update_row(self, columns: Sequence[str], note_id: NoteId, row: CellRow, column_key: str,
                    size_type: SizeType):
        if column_key in columns:
            column_index: int = columns.index(column_key)
            cell: Cell = row.cells[column_index]
            cell.text = self.item_id_cache.get_note_size_str(note_id, size_type, use_cache=True)

    @staticmethod
    def _on_browser_will_search(context: SearchContext) -> None:
        log.debug("Browser will search")
        ColumnHooks._configure_sorting(context, ColumnHooks.column_total_key, ColumnHooks.column_total_label)
        ColumnHooks._configure_sorting(context, ColumnHooks.column_texts_key, ColumnHooks.column_texts_label)
        ColumnHooks._configure_sorting(context, ColumnHooks.column_files_key, ColumnHooks.column_files_label)

    @staticmethod
    def _configure_sorting(context: SearchContext, column_key: str, column_label: str):
        if isinstance(context.order, Column) and context.order.key == column_key:
            sort_col: Optional[Column] = mw.col.get_browser_column("noteFld")
            sort_col.notes_mode_label = column_label
            context.order = sort_col

    def _on_browser_did_search(self, context: SearchContext) -> None:
        log.debug("Browser did search")
        is_note: bool = ColumnHooks._is_notes_mode(context)
        ColumnHooks._sort_by_column(context, ColumnHooks.column_total_label,
                                    lambda item_id: self._get_item_size(item_id, ItemIdCache.TOTAL_SIZE, is_note))
        ColumnHooks._sort_by_column(context, ColumnHooks.column_texts_label,
                                    lambda item_id: self._get_item_size(item_id, ItemIdCache.TEXTS_SIZE, is_note))
        ColumnHooks._sort_by_column(context, ColumnHooks.column_files_label,
                                    lambda item_id: self._get_item_size(item_id, ItemIdCache.FILES_SIZE, is_note))

    @staticmethod
    def _sort_by_column(context: SearchContext, column_label: str, item_size_lambda: Callable[[ItemId], SizeBytes]):
        if context.ids and isinstance(context.order, Column) and context.order.notes_mode_label == column_label:
            context.ids = sorted(context.ids, key=item_size_lambda, reverse=True)

    @staticmethod
    def _is_notes_mode(context: SearchContext) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return context.browser._switch.isChecked()

    def _get_item_size(self, item_id: ItemId, size_type: SizeType, is_note: bool) -> SizeBytes:
        note_id: NoteId = item_id if is_note else self.item_id_cache.get_note_id_by_card_id(item_id)
        return self.item_id_cache.get_note_size_bytes(note_id, size_type, use_cache=True)
