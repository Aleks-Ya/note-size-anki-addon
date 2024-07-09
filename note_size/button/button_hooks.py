import logging
from logging import Logger
from typing import Any, Callable

from anki.notes import Note
from aqt import gui_hooks
from aqt.editor import Editor
from aqt.utils import showInfo

from ..config.config import Config
from ..types import ButtonLabel
from .button_formatter import ButtonFormatter
from .details_formatter import DetailsFormatter

log: Logger = logging.getLogger(__name__)


class ButtonHooks:
    def __init__(self, details_formatter: DetailsFormatter, button_formatter: ButtonFormatter, config: Config):
        self.__enabled: bool = config.size_button_enabled()
        self.__details_formatter: DetailsFormatter = details_formatter
        self.__button_formatter: ButtonFormatter = button_formatter
        self.__hook_editor_did_init: Callable[[Editor], None] = self.__on_editor_did_init
        self.__hook_editor_did_init_buttons: Callable[[list[str], Editor], None] = self.__on_editor_did_init_buttons
        self.__hook_editor_did_load_note: Callable[[Editor], None] = self.__on_editor_did_load_note
        self.__hook_editor_did_unfocus_field: Callable[[bool, Note, int], None] = self.__on_editor_did_unfocus_field
        self.__hook_editor_did_fire_typing_timer: Callable[[Note], None] = self.__on_editor_did_fire_typing_timer
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        if self.__enabled:
            gui_hooks.editor_did_init.append(self.__hook_editor_did_init)
            gui_hooks.editor_did_init_buttons.append(self.__hook_editor_did_init_buttons)
            gui_hooks.editor_did_load_note.append(self.__hook_editor_did_load_note)
            gui_hooks.editor_did_unfocus_field.append(self.__hook_editor_did_unfocus_field)
            gui_hooks.editor_did_fire_typing_timer.append(self.__hook_editor_did_fire_typing_timer)
            log.info(f"{self.__class__.__name__} are set")
        else:
            log.info(f"Size Button is disabled")

    def remove_hooks(self) -> None:
        gui_hooks.editor_did_init.remove(self.__hook_editor_did_init)
        gui_hooks.editor_did_init_buttons.remove(self.__hook_editor_did_init_buttons)
        gui_hooks.editor_did_load_note.remove(self.__hook_editor_did_load_note)
        gui_hooks.editor_did_unfocus_field.remove(self.__hook_editor_did_unfocus_field)
        gui_hooks.editor_did_fire_typing_timer.remove(self.__hook_editor_did_fire_typing_timer)
        log.info(f"{self.__class__.__name__} was set")

    def __on_editor_did_init(self, editor: Editor) -> None:
        log.debug("On init...")
        self.editor: Editor = editor

    def __on_size_button_click(self, editor: Editor) -> None:
        log.debug("On size button click...")
        note: Note = editor.note
        if note:
            showInfo(self.__details_formatter.format_note_detailed_text(note))

    def __on_editor_did_init_buttons(self, buttons: list[str], editor: Editor) -> None:
        log.debug("Add editor button...")
        button: str = editor.addButton(id="size_button",
                                       label=ButtonFormatter.get_zero_size_label(),
                                       icon=None, cmd="size_button_cmd",
                                       func=self.__on_size_button_click,
                                       tip="Click to see details",
                                       disables=False)
        buttons.append(button)
        log.info("Size button was added to Editor")

    def __on_editor_did_load_note(self, _: Editor) -> None:
        log.debug("On load note...")
        self.__refresh_size_button()

    def __on_editor_did_unfocus_field(self, _: bool, __: Note, ___: int) -> None:
        log.debug("On unfocus field...")
        self.__refresh_size_button()

    def __on_editor_did_fire_typing_timer(self, _: Note) -> None:
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
                    label: ButtonLabel = self.__button_formatter.get_add_mode_label(self.editor.note)
                else:
                    label: ButtonLabel = self.__button_formatter.get_edit_mode_label(self.editor.note.id)
            js: str = f""" try {{
                                document.getElementById('size_button').textContent = '{label}'
                            }} catch (error) {{
                              error.stack
                            }}"""
            self.editor.web.evalWithCallback(js, ButtonHooks.__eval_callback)
            log.info(f"Size button was refreshed: {label}")
        else:
            log.debug("Skip size button refresh as editor.web is empty")
