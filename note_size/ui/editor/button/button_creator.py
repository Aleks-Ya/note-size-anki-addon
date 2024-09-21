import logging
from logging import Logger

from anki.notes import Note
from aqt.editor import Editor

from .button_formatter import ButtonFormatter
from ...details_dialog.details_dialog import DetailsDialog

log: Logger = logging.getLogger(__name__)


class ButtonCreator:
    def __init__(self, button_formatter: ButtonFormatter, details_dialog: DetailsDialog) -> None:
        self.__button_formatter: ButtonFormatter = button_formatter
        self.__details_dialog: DetailsDialog = details_dialog
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __on_size_button_click(self, editor: Editor) -> None:
        log.debug("On size button click...")
        note: Note = editor.note
        if note:
            log.debug(f"Show details dialog for NoteId: {note.id}")
            self.__details_dialog.show_note(note)

    def create_size_button(self, editor: Editor) -> str:
        button: str = editor.addButton(id="size_button",
                                       label=self.__button_formatter.get_zero_size_label().get_text(),
                                       icon=None,
                                       cmd="size_button_cmd",
                                       func=self.__on_size_button_click,
                                       tip="Note size. Click for details",
                                       disables=False)
        return button
