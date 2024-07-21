import logging
from logging import Logger
from typing import Any, Callable, Optional

from anki.notes import Note
from aqt import gui_hooks
from aqt.editor import Editor
from aqt.utils import showInfo
from aqt.webview import WebContent
from aqt.qt import QWidget

from .button_label import ButtonLabel
from ..config.config import Config
from ..config.settings import Settings
from .button_formatter import ButtonFormatter
from .details_formatter import DetailsFormatter

log: Logger = logging.getLogger(__name__)


class ButtonHooks:
    def __init__(self, details_formatter: DetailsFormatter, button_formatter: ButtonFormatter,
                 settings: Settings, config: Config):
        self.editor: Optional[Editor] = None
        self.__config: Config = config
        self.__details_formatter: DetailsFormatter = details_formatter
        self.__button_formatter: ButtonFormatter = button_formatter
        self.__addon_package: str = settings.addon_package()
        self.__hook_editor_did_init: Callable[[Editor], None] = self.__on_editor_did_init
        self.__hook_editor_did_init_buttons: Callable[[list[str], Editor], None] = self.__on_editor_did_init_buttons
        self.__hook_editor_did_load_note: Callable[[Editor], None] = self.__on_editor_did_load_note
        self.__hook_editor_did_unfocus_field: Callable[[bool, Note, int], None] = self.__on_editor_did_unfocus_field
        self.__hook_editor_did_fire_typing_timer: Callable[[Note], None] = self.__on_editor_did_fire_typing_timer
        self.__hook_webview_will_set_content: Callable[[WebContent, Optional[object]], None] \
            = self.__add_size_button_css
        self.__hook_focus_did_change: Callable[[Optional[QWidget], Optional[QWidget]], None] = self.__on_focus_changed
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.editor_did_init.append(self.__hook_editor_did_init)
        gui_hooks.editor_did_init_buttons.append(self.__hook_editor_did_init_buttons)
        gui_hooks.editor_did_load_note.append(self.__hook_editor_did_load_note)
        gui_hooks.editor_did_unfocus_field.append(self.__hook_editor_did_unfocus_field)
        gui_hooks.editor_did_fire_typing_timer.append(self.__hook_editor_did_fire_typing_timer)
        gui_hooks.webview_will_set_content.append(self.__hook_webview_will_set_content)
        gui_hooks.focus_did_change.append(self.__hook_focus_did_change)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.editor_did_init.remove(self.__hook_editor_did_init)
        gui_hooks.editor_did_init_buttons.remove(self.__hook_editor_did_init_buttons)
        gui_hooks.editor_did_load_note.remove(self.__hook_editor_did_load_note)
        gui_hooks.editor_did_unfocus_field.remove(self.__hook_editor_did_unfocus_field)
        gui_hooks.editor_did_fire_typing_timer.remove(self.__hook_editor_did_fire_typing_timer)
        gui_hooks.webview_will_set_content.remove(self.__hook_webview_will_set_content)
        gui_hooks.focus_did_change.remove(self.__hook_focus_did_change)
        log.info(f"{self.__class__.__name__} was set")

    def __on_focus_changed(self, _: Optional[QWidget], __: Optional[QWidget]) -> None:
        log.debug("On focus changed...")
        self.__refresh_size_button(self.editor)

    def __on_editor_did_init(self, editor: Editor) -> None:
        log.debug("On Editor did init...")
        self.editor: Optional[Editor] = editor
        self.__refresh_size_button(editor)

    def __on_size_button_click(self, editor: Editor) -> None:
        log.debug("On size button click...")
        note: Note = editor.note
        if note:
            showInfo(self.__details_formatter.format_note_detailed_text(note))

    def __on_editor_did_init_buttons(self, buttons: list[str], editor: Editor) -> None:
        log.debug("On Editor did init buttons...")
        button: str = editor.addButton(id="size_button",
                                       label=self.__button_formatter.get_zero_size_label().get_text(),
                                       icon=None, cmd="size_button_cmd",
                                       func=self.__on_size_button_click,
                                       tip="Note size. Click for details",
                                       disables=False)
        buttons.append(button)
        log.info("Size button was added to Editor")

    def __on_editor_did_load_note(self, editor: Editor) -> None:
        log.debug("On load note...")
        self.__refresh_size_button(editor)

    def __on_editor_did_unfocus_field(self, _: bool, __: Note, ___: int) -> None:
        log.debug("On unfocus field...")
        self.__refresh_size_button(self.editor)

    def __on_editor_did_fire_typing_timer(self, _: Note) -> None:
        log.debug("On fire typing timer...")
        self.__refresh_size_button(self.editor)

    def __add_size_button_css(self, web_content: WebContent, _: Optional[object]) -> None:
        web_content.css.append(f"/_addons/{self.__addon_package}/web/size_button.css")

    @staticmethod
    def __eval_callback(val: Any):
        log.debug(f"Eval callback: {val}")

    def __refresh_size_button(self, editor: Optional[Editor]) -> None:
        log.debug("Refresh size button...")
        if editor and editor.web:
            if self.__config.get_size_button_enabled():
                label: ButtonLabel = self.__button_formatter.get_zero_size_label()
                if editor.note:
                    if editor.addMode:
                        label: ButtonLabel = self.__button_formatter.get_add_mode_label(editor.note)
                    else:
                        label: ButtonLabel = self.__button_formatter.get_edit_mode_label(editor.note.id)
                js: str = f"""
                    try {{
                        const sizeButton = document.getElementById('size_button');
                        if (sizeButton) {{
                            sizeButton.style.display = 'block';
                            sizeButton.textContent = '{label.get_text()}';
                            sizeButton.style.backgroundColor = '{label.get_background_color()}';
                        }}
                    }} catch (error) {{
                      error.stack
                    }} """
                editor.web.evalWithCallback(js, ButtonHooks.__eval_callback)
                log.debug(f"Size button was refreshed: {label}")
            else:
                js: str = f"""
                    try {{
                        const sizeButton = document.getElementById('size_button');
                        if (sizeButton) {{
                            sizeButton.style.display = 'none';
                        }}
                    }} catch (error) {{
                      error.stack
                    }} """
                editor.web.evalWithCallback(js, ButtonHooks.__eval_callback)
                log.debug(f"Size button was hidden")
        else:
            log.debug("Skip size button refresh as editor.web is empty")
