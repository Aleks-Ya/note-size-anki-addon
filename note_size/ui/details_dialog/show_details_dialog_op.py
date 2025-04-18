import logging
from logging import Logger
from typing import Sequence

from anki.collection import Collection
from anki.notes import NoteId
from aqt.operations import QueryOp
from aqt.progress import ProgressManager
from aqt.utils import show_critical
from aqt import QWidget

from .details_dialog import DetailsDialog

log: Logger = logging.getLogger(__name__)


class ShowDetailsDialogOp:
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self, details_dialog: DetailsDialog, note_ids: Sequence[NoteId], progress_manager: ProgressManager,
                 parent: QWidget):
        self.__details_dialog: DetailsDialog = details_dialog
        self.__note_ids: Sequence[NoteId] = note_ids
        self.__progress_manager: ProgressManager = progress_manager
        self.__parent: QWidget = parent
        log.debug(f"{self.__class__.__name__} was instantiated")

    def run(self):
        log.debug("Start running ShowDetailsDialogOp")
        QueryOp(parent=self.__parent, op=self.__background_op, success=self.__on_success).failure(
            self.__on_failure).without_collection().with_progress().run_in_background()
        self.__progress_manager.set_title(self.__progress_dialog_title)
        log.debug("Finished running ShowDetailsDialogOp")

    def __background_op(self, _: Collection) -> int:
        log.debug(f"Background operation started: {len(self.__note_ids)}")
        self.__details_dialog.prepare_show_notes(self.__note_ids)
        log.debug("Background operation finished")
        return len(self.__note_ids)

    def __on_success(self, count: int) -> None:
        log.debug(f"Notes shown successfully: {count}")
        self.__details_dialog.show_notes(self.__parent.parent())

    @staticmethod
    def __on_failure(e: Exception) -> None:
        log.error("Error during cache initialization", exc_info=e)
        show_critical(title="Showing note details", text="Failed")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
