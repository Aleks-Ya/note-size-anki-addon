import logging
from logging import Logger
from typing import Sequence, Optional

from anki.cards import Card
from anki.collection import BrowserColumns
from anki.errors import NotFoundError
from anki.notes import Note, NoteId
from aqt import gui_hooks, mw
from aqt.browser import Column, Cell, SearchContext
from aqt.browser import ItemId, CellRow
from aqt.editor import Editor
from aqt.utils import showInfo

from .note_size import NoteSize

log: Logger = logging.getLogger(__name__)


class NoteSizeHooks:
    column_key: str = "note-size"
    column_label: str = "Size"
    editor: Editor

    def setup_hooks(self):
        gui_hooks.editor_did_init.append(self._on_init)
        gui_hooks.browser_did_fetch_columns.append(self._add_custom_column)
        gui_hooks.browser_did_fetch_row.append(self._modify_row)
        gui_hooks.editor_did_init_buttons.append(self._add_editor_button)
        gui_hooks.editor_did_load_note.append(self._on_load_note)
        gui_hooks.editor_did_unfocus_field.append(self._on_unfocus_field)
        gui_hooks.browser_will_search.append(self._on_browser_will_search)
        gui_hooks.browser_did_search.append(self.on_browser_did_search)
        log.info("Hooks are set")

    def _on_init(self, editor: Editor):
        self.editor = editor

    def _add_custom_column(self, columns: dict[str, Column]) -> None:
        columns[self.column_key] = Column(
            key=self.column_key,
            cards_mode_label=self.column_label,
            notes_mode_label=self.column_label,
            sorting_cards=BrowserColumns.SORTING_ASCENDING,
            sorting_notes=BrowserColumns.SORTING_ASCENDING,
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
            size: int = NoteSize.calculate_note_size(note)
            cell.text = NoteSize.bytes_to_human_str(size)

    @staticmethod
    def _on_size_button_click(editor: Editor):
        log.info("Size button was clicked")
        if editor.note:
            total_size: str = NoteSize.bytes_to_human_str(NoteSize.calculate_note_size(editor.note))
            total_texts_size: str = NoteSize.bytes_to_human_str(NoteSize.total_text_size(editor.note))
            total_files_size: str = NoteSize.bytes_to_human_str(NoteSize.total_file_size(editor.note))
            file_sizes: dict[str, int] = NoteSize.sort_by_size_desc(NoteSize.file_sizes(editor.note))
            files_sizes_str: list[str] = NoteSize.file_sizes_to_human_strings(file_sizes)
            files_str: str = '</li><li style="white-space:nowrap">'.join(files_sizes_str) \
                if len(files_sizes_str) > 0 else "<no-files>"
            detailed: str = f"""
                            <h3>Total note size: {total_size}</h3>
                            <ul>
                                <li>Texts size: {total_texts_size}</li>
                                <li>Files size: {total_files_size}</li>
                                <li>Files (big to small):</li>
                                    <ol>
                                        <li style="white-space:nowrap">{files_str}</li>
                                    </ol>
                            </ul>
                            """
            showInfo(detailed)

    def _add_editor_button(self, buttons: list[str], editor: Editor):
        button: str = editor.addButton(id="size_button", label="Size: -", icon=None, cmd="size_button_cmd",
                                       func=self._on_size_button_click, tip="Click to see details", disables=False)
        buttons.append(button)
        log.info("Size button was added to Editor")

    def _on_load_note(self, _: Editor):
        self._refresh_size_button()

    def _on_unfocus_field(self, _: bool, __: Note, ___: int):
        self._refresh_size_button()

    def _refresh_size_button(self):
        size: str = NoteSize.bytes_to_human_str(NoteSize.calculate_note_size(self.editor.note)) \
            if self.editor.note else "-"
        self.editor.web.eval(f"document.getElementById('size_button').textContent = 'Size: {size}'")
        log.info("Size button was refreshed")

    def _on_browser_will_search(self, context: SearchContext) -> None:
        log.debug("Browser will search")
        if isinstance(context.order, Column) and context.order.key == self.column_key:
            sort_col = mw.col.get_browser_column("noteFld")
            sort_col.notes_mode_label = self.column_label
            context.order = sort_col

    def on_browser_did_search(self, context: SearchContext) -> None:
        log.debug("Browser did search")
        if context.ids and isinstance(context.order, Column) and context.order.notes_mode_label == self.column_label:
            context.ids = sorted(context.ids, key=lambda item_id: self.get_size_key(item_id))

    @staticmethod
    def get_size_key(item_id: ItemId) -> int:
        note: Optional[Note]
        try:
            note = mw.col.get_note(item_id)
        except NotFoundError:
            note = None
        if not note:
            note_id: NoteId = mw.col.get_card(item_id).nid
            note: Note = mw.col.get_note(note_id)
        return NoteSize.calculate_note_size(note)
