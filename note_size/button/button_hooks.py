import logging
from logging import Logger
from typing import Any

from anki.notes import Note
from aqt import gui_hooks
from aqt.editor import Editor
from aqt.utils import showInfo

from ..types import ButtonLabel
from .button_formatter import ButtonFormatter
from .details_formatter import DetailsFormatter

log: Logger = logging.getLogger(__name__)


class ButtonHooks:
    def __init__(self, details_formatter: DetailsFormatter, button_formatter: ButtonFormatter):
        self.details_formatter: DetailsFormatter = details_formatter
        self.button_formatter: ButtonFormatter = button_formatter
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.editor_did_init.append(self.__on_init)
        gui_hooks.editor_did_init_buttons.append(self.__add_editor_button)
        gui_hooks.editor_did_load_note.append(self.__on_load_note)
        gui_hooks.editor_did_unfocus_field.append(self.__on_unfocus_field)
        gui_hooks.editor_did_fire_typing_timer.append(self.__on_fire_typing_timer)
        log.info("Size button hooks are set")

    def __on_init(self, editor: Editor) -> None:
        log.debug("On init...")
        self.editor: Editor = editor

    def __on_size_button_click(self, editor: Editor) -> None:
        log.debug("On size button click...")
        note: Note = editor.note
        if note:
            showInfo(self.details_formatter.format_note_detailed_text(note))

    def __add_editor_button(self, buttons: list[str], editor: Editor) -> None:
        log.debug("Add editor button...")
        button: str = editor.addButton(id="size_button",
                                       label=ButtonFormatter.get_zero_size_label(),
                                       icon=None, cmd="size_button_cmd",
                                       func=self.__on_size_button_click,
                                       tip="Click to see details",
                                       disables=False)
        buttons.append(button)
        log.info("Size button was added to Editor")

    def __on_load_note(self, _: Editor) -> None:
        log.debug("On load note...")
        self.__refresh_size_button()

    def __on_unfocus_field(self, _: bool, __: Note, ___: int) -> None:
        log.debug("On unfocus field...")
        self.__refresh_size_button()

    def __on_fire_typing_timer(self, _: Note) -> None:
        log.debug("On fire typing timer...")
        self.__refresh_size_button()

    @staticmethod
    def __eval_callback(val: Any):
        log.debug(f"Eval callback: {val}")

    def __refresh_size_button(self) -> None:
        log.debug("Refresh size button...")
        if self.editor.web:
            label: ButtonLabel = ButtonFormatter.get_zero_size_label()
            if self.editor.note:
                if self.editor.addMode:
                    label: ButtonLabel = self.button_formatter.get_add_mode_label(self.editor.note)
                else:
                    label: ButtonLabel = self.button_formatter.get_edit_mode_label(self.editor.note.id)
            js: str = f""" try {{
                                document.getElementById('size_button').textContent = '{label}'
                            }} catch (error) {{
                              error.stack
                            }}"""
            self.editor.web.evalWithCallback(js, ButtonHooks.__eval_callback)
            log.info(f"Size button was refreshed: {label}")
        else:
            log.debug("Skip size button refresh as editor.web is empty")
