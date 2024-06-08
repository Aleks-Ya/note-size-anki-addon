import logging
from logging import Logger

from anki.notes import Note
from aqt import gui_hooks
from aqt.editor import Editor
from aqt.utils import showInfo

from .size_button_formatter import SizeButtonFormatter

log: Logger = logging.getLogger(__name__)


class SizeButtonHooks:
    editor: Editor

    def __init__(self, size_button_formatter: SizeButtonFormatter):
        self.size_button_formatter: SizeButtonFormatter = size_button_formatter

    def setup_hooks(self):
        gui_hooks.editor_did_init.append(self._on_init)
        gui_hooks.editor_did_init_buttons.append(self._add_editor_button)
        gui_hooks.editor_did_load_note.append(self._on_load_note)
        gui_hooks.editor_did_unfocus_field.append(self._on_unfocus_field)
        log.info("Size button hooks are set")

    def _on_init(self, editor: Editor):
        self.editor = editor

    def _on_size_button_click(self, editor: Editor):
        log.info("Size button was clicked")
        note = editor.note
        if note:
            showInfo(self.size_button_formatter.format_note_detailed_text(note))

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
        if self.editor.web:
            size_str: str = self.size_button_formatter.get_note_human_str(self.editor.note.id) \
                if self.editor.note else "-"
            self.editor.web.eval(f"document.getElementById('size_button').textContent = 'Size: {size_str}'")
            log.info("Size button was refreshed")
