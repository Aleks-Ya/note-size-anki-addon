import logging
from logging import Logger

from anki.notes import Note
from aqt.editor import Editor
from aqt.qt import QWidget

from .editor_button_formatter import EditorButtonFormatter
from ...details_dialog.details_dialog_factory import DetailsDialogFactory

log: Logger = logging.getLogger(__name__)


class EditorButtonCreator:
    def __init__(self, editor_button_formatter: EditorButtonFormatter,
                 details_dialog_factory: DetailsDialogFactory) -> None:
        self.__editor_button_formatter: EditorButtonFormatter = editor_button_formatter
        self.__details_dialog_factory: DetailsDialogFactory = details_dialog_factory
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_size_button(self, editor: Editor) -> str:
        button: str = editor.addButton(id="size_button",
                                       label=self.__editor_button_formatter.get_zero_size_label().get_text(),
                                       icon=None,
                                       cmd="size_button_cmd",
                                       func=self.__on_size_button_click,
                                       tip="Note size. Click for details",
                                       disables=False)
        return button

    def __on_size_button_click(self, editor: Editor) -> None:
        log.debug("On size button click...")
        log.debug(f"Editor mode: {editor.editorMode}")
        log.debug(f"Is add mode: {editor.addMode}")
        note: Note = editor.note
        if note:
            log.debug(f"Show details dialog for NoteId: {note.id}")
            parent: QWidget = editor.widget
            if editor.addMode:
                self.__details_dialog_factory.get_add_cards_browser_editor_button_details_dialog(parent).show_note(note)
            else:
                self.__details_dialog_factory.get_browser_editor_button_details_dialog(parent).show_note(note)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
