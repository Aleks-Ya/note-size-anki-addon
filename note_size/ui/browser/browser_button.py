import logging
from logging import Logger
from typing import Sequence

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import NoteId
from aqt.browser import Browser
from aqt.qt import QPushButton

from ..common.number_formatter import NumberFormatter
from ..details_dialog.details_dialog import DetailsDialog
from ..details_dialog.progress import WithProgressQueryOp
from ...cache.item_id_cache import ItemIdCache
from ...types import SizeType, SizeStr

log: Logger = logging.getLogger(__name__)


class BrowserButton(QPushButton):

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, details_dialog: DetailsDialog,
                 browser: Browser) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__details_dialog: DetailsDialog = details_dialog
        self.__browser: Browser = browser
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
        note_ids_number: str = NumberFormatter.with_thousands_separator(len(note_ids))
        tooltip: str = (f"Size of {note_ids_number} notes\n"
                        "Size includes texts and files\n"
                        "Click for details")
        # noinspection PyUnresolvedReferences
        self.setToolTip(tooltip)

    def show_cards_size(self, card_ids: Sequence[CardId]) -> None:
        note_ids: Sequence[NoteId] = self.__item_id_cache.get_note_ids_by_card_ids(card_ids)
        self.__current_note_ids = note_ids
        size: SizeStr = self.__item_id_cache.get_notes_size_str(note_ids, SizeType.TOTAL, use_cache=True)
        self.setText(size)
        note_ids_number: str = NumberFormatter.with_thousands_separator(len(note_ids))
        card_ids_number: str = NumberFormatter.with_thousands_separator(len(card_ids))
        tooltip: str = (f"Size of {card_ids_number} cards ({note_ids_number} notes)\n"
                        "Size includes texts and files\n"
                        "Click for details")
        # noinspection PyUnresolvedReferences
        self.setToolTip(tooltip)

    def __on_click(self) -> None:
        log.debug("Browser size button clicked")
        op: WithProgressQueryOp = WithProgressQueryOp(self.__details_dialog, self.__current_note_ids, self.__browser)
        op.run()
        log.debug("Browser size button click finished")
