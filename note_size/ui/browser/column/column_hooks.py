import logging
from logging import Logger
from typing import Sequence, Optional, Callable, Union

from anki.collection import BrowserColumns
from anki.notes import NoteId
from aqt import gui_hooks, mw
from aqt.browser import Column, Cell, SearchContext
from aqt.browser import ItemId, CellRow

from .item_id_sorter import ItemIdSorter
from ....ui.common.browser_helper import BrowserHelper
from ....cache.item_id_cache import ItemIdCache
from ....cache.size_str_cache import SizeStrCache
from ....config.config import Config
from ....types import SizeType, SizePrecision

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

    def __init__(self, item_id_cache: ItemIdCache, size_str_cache: SizeStrCache, item_id_sorter: ItemIdSorter,
                 config: Config) -> None:
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_str_cache: SizeStrCache = size_str_cache
        self.__item_id_sorter: ItemIdSorter = item_id_sorter
        self.__config: Config = config
        self.__hook_browser_did_fetch_columns: Callable[[dict[str, Column]], None] = ColumnHooks.__add_custom_column
        self.__hook_browser_did_fetch_row: Callable[[Union[int, NoteId], bool, CellRow, Sequence[str]], None] = \
            self.__modify_row
        self.__hook_browser_will_search: Callable[[SearchContext], None] = ColumnHooks.__on_browser_will_search
        self.__hook_browser_did_search: Callable[[SearchContext], None] = self.__on_browser_did_search
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.browser_did_fetch_columns.append(self.__hook_browser_did_fetch_columns)
        gui_hooks.browser_did_fetch_row.append(self.__hook_browser_did_fetch_row)
        gui_hooks.browser_will_search.append(self.__hook_browser_will_search)
        gui_hooks.browser_did_search.append(self.__hook_browser_did_search)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.browser_did_fetch_columns.remove(self.__hook_browser_did_fetch_columns)
        gui_hooks.browser_did_fetch_row.remove(self.__hook_browser_did_fetch_row)
        gui_hooks.browser_will_search.remove(self.__hook_browser_will_search)
        gui_hooks.browser_did_search.remove(self.__hook_browser_did_search)
        log.info(f"{self.__class__.__name__} are removed")

    @staticmethod
    def __add_custom_column(columns: dict[str, Column]) -> None:
        ColumnHooks.__add_column(columns, ColumnHooks.__column_total_key, ColumnHooks.__column_total_label,
                                 ColumnHooks.__column_total_tooltip)
        ColumnHooks.__add_column(columns, ColumnHooks.__column_texts_key, ColumnHooks.__column_texts_label,
                                 ColumnHooks.__column_texts_tooltip)
        ColumnHooks.__add_column(columns, ColumnHooks.__column_files_key, ColumnHooks.__column_files_label,
                                 ColumnHooks.__column_files_tooltip)
        log.info("Columns were added")

    @staticmethod
    def __add_column(columns: dict[str, Column], column_key: str, column_label: str, tooltip_total: str) -> None:
        columns[column_key] = Column(
            key=column_key,
            cards_mode_label=column_label,
            notes_mode_label=column_label,
            sorting_cards=BrowserColumns.SORTING_DESCENDING,
            sorting_notes=BrowserColumns.SORTING_DESCENDING,
            uses_cell_font=False,
            alignment=BrowserColumns.ALIGNMENT_CENTER,
            cards_mode_tooltip=tooltip_total,
            notes_mode_tooltip=tooltip_total
        )

    def __modify_row(self, item_id: ItemId, is_note: bool, row: CellRow, columns: Sequence[str]) -> None:
        note_id: NoteId = item_id if is_note else self.__item_id_cache.get_note_id_by_card_id(item_id)
        self.__update_column(ColumnHooks.__column_total_key, SizeType.TOTAL, row, columns, note_id)
        self.__update_column(ColumnHooks.__column_texts_key, SizeType.TEXTS, row, columns, note_id)
        self.__update_column(ColumnHooks.__column_files_key, SizeType.FILES, row, columns, note_id)

    def __update_column(self, column_key: str, size_type: SizeType, row: CellRow, columns: Sequence[str],
                        note_id: NoteId) -> None:
        if column_key in columns:
            column_index: int = columns.index(column_key)
            cell: Cell = row.cells[column_index]
            size_precision: SizePrecision = self.__config.get_browser_size_precision()
            cell.text = self.__size_str_cache.get_note_size_str(note_id, size_type, size_precision, use_cache=True)

    @staticmethod
    def __on_browser_will_search(context: SearchContext) -> None:
        log.debug("Browser will search")
        ColumnHooks.__configure_sorting(context, ColumnHooks.__column_total_key, ColumnHooks.__column_total_label)
        ColumnHooks.__configure_sorting(context, ColumnHooks.__column_texts_key, ColumnHooks.__column_texts_label)
        ColumnHooks.__configure_sorting(context, ColumnHooks.__column_files_key, ColumnHooks.__column_files_label)

    @staticmethod
    def __configure_sorting(context: SearchContext, column_key: str, column_label: str) -> None:
        if isinstance(context.order, Column) and context.order.key == column_key:
            sort_col: Optional[Column] = mw.col.get_browser_column("noteFld")
            sort_col.notes_mode_label = column_label
            context.order = sort_col

    def __on_browser_did_search(self, context: SearchContext) -> None:
        log.debug("Browser did search")
        is_note: bool = BrowserHelper.is_notes_mode(context.browser)
        self.__sort_rows_by_column(ColumnHooks.__column_total_label, SizeType.TOTAL, context, is_note)
        self.__sort_rows_by_column(ColumnHooks.__column_texts_label, SizeType.TEXTS, context, is_note)
        self.__sort_rows_by_column(ColumnHooks.__column_files_label, SizeType.FILES, context, is_note)

    def __sort_rows_by_column(self, column_label: str, size_type: SizeType, context: SearchContext,
                              is_note: bool) -> None:
        if context.ids and isinstance(context.order, Column) and context.order.notes_mode_label == column_label:
            context.ids = self.__item_id_sorter.sort_item_ids(context.ids, size_type, is_note)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
