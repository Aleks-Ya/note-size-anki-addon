import logging
from logging import Logger
from typing import Sequence

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import NoteId
from aqt.qt import QPushButton

from ..details_dialog.details_dialog import DetailsDialog
from ...cache.item_id_cache import ItemIdCache
from ...types import SizeType, SizeStr

log: Logger = logging.getLogger(__name__)


class BrowserButton(QPushButton):

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, details_dialog: DetailsDialog) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__details_dialog: DetailsDialog = details_dialog
        self.__current_note_ids: Sequence[NoteId] = []
        # noinspection PyUnresolvedReferences
        self.setStyleSheet("""
        QPushButton {
            padding-left: 5px;
            padding-right: 5px;
        }
        """)
        # noinspection PyUnresolvedReferences
        self.clicked.connect(self.__on_click)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_notes_size(self, note_ids: Sequence[NoteId]) -> None:
        self.__current_note_ids = note_ids
        size: SizeStr = self.__item_id_cache.get_notes_size_str(note_ids, SizeType.TOTAL, use_cache=True)
        self.setText(size)
        tooltip: str = (f"Size of {len(note_ids)} notes\n"
                        "Size includes texts and files\n"
                        "Click for details")
        # noinspection PyUnresolvedReferences
        self.setToolTip(tooltip)

    def show_cards_size(self, card_ids: Sequence[CardId]) -> None:
        note_ids: Sequence[NoteId] = self.__item_id_cache.get_note_ids_by_card_ids(card_ids)
        self.__current_note_ids = note_ids
        size: SizeStr = self.__item_id_cache.get_notes_size_str(note_ids, SizeType.TOTAL, use_cache=True)
        self.setText(size)
        tooltip: str = (f"Size of {len(card_ids)} cards ({len(note_ids)} notes)\n"
                        "Size includes texts and files\n"
                        "Click for details")
        # noinspection PyUnresolvedReferences
        self.setToolTip(tooltip)

    def __on_click(self) -> None:
        self.__details_dialog.prepare_show_notes(self.__current_note_ids)
        self.__details_dialog.show_notes()
