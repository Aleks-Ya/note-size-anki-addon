import logging
from logging import Logger
from typing import Sequence, Optional

from anki.cards import Card
from anki.collection import BrowserColumns
from anki.notes import Note, NoteId
from aqt import gui_hooks, mw
from aqt.browser import Column, Cell, SearchContext
from aqt.browser import ItemId, CellRow

from .size_calculator import SizeCalculator
from .size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class SizeColumnHooks:
    column_key: str = "note-size"
    column_label: str = "Size"

    def __init__(self, size_calculator: SizeCalculator):
        self.size_calculator: SizeCalculator = size_calculator

    def setup_hooks(self):
        gui_hooks.browser_did_fetch_columns.append(self._add_custom_column)
        gui_hooks.browser_did_fetch_row.append(self._modify_row)
        gui_hooks.browser_will_search.append(self._on_browser_will_search)
        gui_hooks.browser_did_search.append(self._on_browser_did_search)
        log.info("Size column hooks are set")

    def _add_custom_column(self, columns: dict[str, Column]) -> None:
        columns[self.column_key] = Column(
            key=self.column_key,
            cards_mode_label=self.column_label,
            notes_mode_label=self.column_label,
            sorting_cards=BrowserColumns.SORTING_DESCENDING,
            sorting_notes=BrowserColumns.SORTING_DESCENDING,
            uses_cell_font=True,
            alignment=BrowserColumns.ALIGNMENT_START,
            cards_mode_tooltip="",
            notes_mode_tooltip="",
        )
        log.info("Column was added")

    def _modify_row(self, card_or_note_id: ItemId, is_note: bool, row: CellRow, columns: Sequence[str]) -> None:
        if self.column_key in columns:
            column_index: int = columns.index(self.column_key)
            cell: Cell = row.cells[column_index]
            if is_note:
                note: Note = mw.col.get_note(card_or_note_id)
            else:
                card: Card = mw.col.get_card(card_or_note_id)
                note: Note = card.note()
            size: int = self.size_calculator.calculate_note_size(note, use_cache=True)
            cell.text = SizeFormatter.bytes_to_human_str(size)

    def _on_browser_will_search(self, context: SearchContext) -> None:
        log.debug("Browser will search")
        if isinstance(context.order, Column) and context.order.key == self.column_key:
            sort_col: Optional[Column] = mw.col.get_browser_column("noteFld")
            sort_col.notes_mode_label = self.column_label
            context.order = sort_col

    def _on_browser_did_search(self, context: SearchContext) -> None:
        log.debug("Browser did search")
        if context.ids and isinstance(context.order, Column) and context.order.notes_mode_label == self.column_label:
            is_notes_mode: bool = self._is_notes_mode(context)
            log.debug(f"Is notes mode: {is_notes_mode}")
            context.ids = sorted(context.ids, key=lambda item_id: self._get_item_size(item_id, is_notes_mode),
                                 reverse=True)

    @staticmethod
    def _is_notes_mode(context: SearchContext) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return context.browser._switch.isChecked()

    def _get_item_size(self, item_id: ItemId, is_note: bool) -> int:
        if is_note:
            note: Note = mw.col.get_note(item_id)
        else:
            note_id: NoteId = mw.col.get_card(item_id).nid
            note: Note = mw.col.get_note(note_id)
        return self.size_calculator.calculate_note_size(note, use_cache=True)
