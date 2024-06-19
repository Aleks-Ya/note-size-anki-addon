import logging
from logging import Logger
from typing import Sequence, Optional

from anki.collection import BrowserColumns
from anki.notes import NoteId
from aqt import gui_hooks, mw
from aqt.browser import Column, Cell, SearchContext
from aqt.browser import ItemId, CellRow

from .item_id_sorter import ItemIdSorter
from ..cache.item_id_cache import ItemIdCache
from ..types import SizeType

log: Logger = logging.getLogger(__name__)


class ColumnHooks:
    __column_total_key: str = "note-size-total"
    __column_total_label: str = "Size"
    __column_total_tooltip: str = "Note size (texts and files are included)"
    __column_texts_key: str = "note-size-texts"
    __column_texts_label: str = "Size (texts)"
    __column_texts_tooltip: str = "Note size (texts only, files are not included)"
    __column_files_key: str = "note-size-files"
    __column_files_label: str = "Size (files)"
    __column_files_tooltip: str = "Note size (files only, texts are not included)"

    def __init__(self, item_id_cache: ItemIdCache, item_id_sorter: ItemIdSorter):
        self.item_id_cache: ItemIdCache = item_id_cache
        self.item_id_sorter: ItemIdSorter = item_id_sorter
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.browser_did_fetch_columns.append(ColumnHooks._add_custom_column)
        gui_hooks.browser_did_fetch_row.append(self._modify_row)
        gui_hooks.browser_will_search.append(ColumnHooks._on_browser_will_search)
        gui_hooks.browser_did_search.append(self._on_browser_did_search)
        log.info("Size column hooks are set")

    @staticmethod
    def _add_custom_column(columns: dict[str, Column]) -> None:
        ColumnHooks._add_column(columns, ColumnHooks.__column_total_key, ColumnHooks.__column_total_label,
                                ColumnHooks.__column_total_tooltip)
        ColumnHooks._add_column(columns, ColumnHooks.__column_texts_key, ColumnHooks.__column_texts_label,
                                ColumnHooks.__column_texts_tooltip)
        ColumnHooks._add_column(columns, ColumnHooks.__column_files_key, ColumnHooks.__column_files_label,
                                ColumnHooks.__column_files_tooltip)
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
            notes_mode_tooltip=tooltip_total
        )

    def _modify_row(self, item_id: ItemId, is_note: bool, row: CellRow, columns: Sequence[str]) -> None:
        note_id: NoteId = item_id if is_note else self.item_id_cache.get_note_id_by_card_id(item_id)
        self._update_row(columns, note_id, row, ColumnHooks.__column_total_key, SizeType.TOTAL)
        self._update_row(columns, note_id, row, ColumnHooks.__column_texts_key, SizeType.TEXTS)
        self._update_row(columns, note_id, row, ColumnHooks.__column_files_key, SizeType.FILES)

    def _update_row(self, columns: Sequence[str], note_id: NoteId, row: CellRow, column_key: str,
                    size_type: SizeType):
        if column_key in columns:
            column_index: int = columns.index(column_key)
            cell: Cell = row.cells[column_index]
            cell.text = self.item_id_cache.get_note_size_str(note_id, size_type, use_cache=True)

    @staticmethod
    def _on_browser_will_search(context: SearchContext) -> None:
        log.debug("Browser will search")
        ColumnHooks._configure_sorting(context, ColumnHooks.__column_total_key, ColumnHooks.__column_total_label)
        ColumnHooks._configure_sorting(context, ColumnHooks.__column_texts_key, ColumnHooks.__column_texts_label)
        ColumnHooks._configure_sorting(context, ColumnHooks.__column_files_key, ColumnHooks.__column_files_label)

    @staticmethod
    def _configure_sorting(context: SearchContext, column_key: str, column_label: str) -> None:
        if isinstance(context.order, Column) and context.order.key == column_key:
            sort_col: Optional[Column] = mw.col.get_browser_column("noteFld")
            sort_col.notes_mode_label = column_label
            context.order = sort_col

    def _on_browser_did_search(self, context: SearchContext) -> None:
        log.debug("Browser did search")
        is_note: bool = ColumnHooks._is_notes_mode(context)
        self._sort_by_column(context, ColumnHooks.__column_total_label, SizeType.TOTAL, is_note)
        self._sort_by_column(context, ColumnHooks.__column_texts_label, SizeType.TEXTS, is_note)
        self._sort_by_column(context, ColumnHooks.__column_files_label, SizeType.FILES, is_note)

    def _sort_by_column(self, context: SearchContext, column_label: str, size_type: SizeType, is_note: bool) -> None:
        if context.ids and isinstance(context.order, Column) and context.order.notes_mode_label == column_label:
            context.ids = self.item_id_sorter.sort_item_ids(context.ids, size_type, is_note)

    @staticmethod
    def _is_notes_mode(context: SearchContext) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return context.browser._switch.isChecked()
