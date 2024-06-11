import logging
from logging import Logger

from anki.notes import Note
from aqt import gui_hooks
from aqt.editor import Editor
from aqt.utils import showInfo

from .button_formatter import ButtonFormatter, ButtonLabel
from .details_formatter import DetailsFormatter

log: Logger = logging.getLogger(__name__)


class ButtonHooks:
    editor: Editor

    def __init__(self, details_formatter: DetailsFormatter, button_formatter: ButtonFormatter):
        self.details_formatter: DetailsFormatter = details_formatter
        self.button_formatter: ButtonFormatter = button_formatter

    def setup_hooks(self):
        gui_hooks.editor_did_init.append(self._on_init)
        gui_hooks.editor_did_init_buttons.append(ButtonHooks._add_editor_button)
        gui_hooks.editor_did_load_note.append(self._on_load_note)
        gui_hooks.editor_did_unfocus_field.append(self._on_unfocus_field)
        log.info("Size button hooks are set")

    def _on_init(self, editor: Editor):
        self.editor = editor

    @staticmethod
    def _on_size_button_click(editor: Editor):
        log.info("Size button was clicked")
        note = editor.note
        if note:
            showInfo(DetailsFormatter.format_note_detailed_text(note))

    @staticmethod
    def _add_editor_button(buttons: list[str], editor: Editor):
        button: str = editor.addButton(id="size_button",
                                       label=ButtonFormatter.get_zero_size_label(),
                                       icon=None, cmd="size_button_cmd",
                                       func=ButtonHooks._on_size_button_click,
                                       tip="Click to see details",
                                       disables=False)
        buttons.append(button)
        log.info("Size button was added to Editor")

    def _on_load_note(self, _: Editor):
        self._refresh_size_button()

    def _on_unfocus_field(self, _: bool, __: Note, ___: int):
        self._refresh_size_button()

    def _refresh_size_button(self):
        if self.editor.web:
            label: ButtonLabel = ButtonFormatter.get_zero_size_label()
            if self.editor.note:
                if self.editor.addMode:
                    label: ButtonLabel = ButtonFormatter.get_add_mode_label(self.editor.note)
                else:
                    label: ButtonLabel = self.button_formatter.get_edit_mode_label(self.editor.note.id)
            self.editor.web.eval(f"document.getElementById('size_button').textContent = '{label}'")
            log.info("Size button was refreshed")
