import logging
from logging import Logger
from typing import Optional

from anki.notes import Note

from .editor_button_label import EditorButtonLabel
from .editor_button_formatter import EditorButtonFormatter

log: Logger = logging.getLogger(__name__)


class EditorButtonJs:
    def __init__(self, editor_button_formatter: EditorButtonFormatter) -> None:
        self.__editor_button_formatter: EditorButtonFormatter = editor_button_formatter
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_size_button_js(self, note: Optional[Note], add_mode: Optional[bool]) -> str:
        log.debug("Refresh size button...")
        label: EditorButtonLabel = self.__editor_button_formatter.get_zero_size_label()
        if note:
            if add_mode:
                label: EditorButtonLabel = self.__editor_button_formatter.get_add_mode_label(note)
            else:
                label: EditorButtonLabel = self.__editor_button_formatter.get_edit_mode_label(note.id)
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
        return js

    @staticmethod
    def hide_size_button_js() -> str:
        js: str = f"""
            try {{
                const sizeButton = document.getElementById('size_button');
                if (sizeButton) {{
                    sizeButton.style.display = 'none';
                }}
            }} catch (error) {{
              error.stack
            }} """
        return js
