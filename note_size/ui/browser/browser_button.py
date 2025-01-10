import logging
from logging import Logger
from typing import Sequence

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import NoteId
from aqt.browser import Browser, ItemId
from aqt.progress import ProgressManager
from aqt.qt import QPushButton

from ..common.browser_helper import BrowserHelper
from ..common.number_formatter import NumberFormatter
from ..details_dialog.details_dialog import DetailsDialog
from ..details_dialog.show_details_dialog_op import ShowDetailsDialogOp
from ...cache.item_id_cache import ItemIdCache
from ...cache.size_str_cache import SizeStrCache
from ...config.config import Config
from ...types import SizeType, SizeStr, SizePrecision

log: Logger = logging.getLogger(__name__)


class BrowserButton(QPushButton):

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, size_str_cache: SizeStrCache,
                 details_dialog: DetailsDialog, browser: Browser, progress_manager: ProgressManager,
                 config: Config) -> None:
        super().__init__()
        self.__col: Collection = col
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_str_cache: SizeStrCache = size_str_cache
        self.__details_dialog: DetailsDialog = details_dialog
        self.__browser: Browser = browser
        self.__progress_manager: ProgressManager = progress_manager
        self.__config: Config = config
        self.__current_item_ids: Sequence[ItemId] = []
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

    def show_items_size(self, item_ids: Sequence[ItemId]) -> None:
        log.debug(f"Update browser size button for {len(item_ids)} items")
        self.__current_item_ids = item_ids
        if BrowserHelper.is_notes_mode(self.__browser):
            note_ids: Sequence[NoteId] = item_ids
            self.__show_notes_size(note_ids)
        else:
            card_ids: Sequence[CardId] = item_ids
            self.__show_cards_size(card_ids)

    def __show_notes_size(self, note_ids: Sequence[NoteId]) -> None:
        size_precision: SizePrecision = self.__config.get_size_button_size_precision()
        size: SizeStr = self.__size_str_cache.get_notes_size_str(note_ids, SizeType.TOTAL, size_precision,
                                                                 use_cache=True)
        self.setText(size)
        note_ids_number: str = NumberFormatter.with_thousands_separator(len(note_ids))
        tooltip: str = (f"Size of {note_ids_number} notes\n"
                        "Size includes texts and files\n"
                        "Click for details")
        # noinspection PyUnresolvedReferences
        self.setToolTip(tooltip)

    def __show_cards_size(self, card_ids: Sequence[CardId]) -> None:
        note_ids: Sequence[NoteId] = self.__item_ids_to_note_ids(card_ids)
        size_precision: SizePrecision = self.__config.get_size_button_size_precision()
        size: SizeStr = self.__size_str_cache.get_notes_size_str(note_ids, SizeType.TOTAL, size_precision,
                                                                 use_cache=True)
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
        self.show_items_size(self.__current_item_ids)
        note_ids: Sequence[NoteId] = self.__item_ids_to_note_ids(self.__current_item_ids)
        op: ShowDetailsDialogOp = ShowDetailsDialogOp(self.__details_dialog, note_ids, self.__progress_manager,
                                                      self.__browser)
        op.run()
        log.debug("Browser size button click finished")

    def __item_ids_to_note_ids(self, item_ids: Sequence[ItemId]) -> Sequence[NoteId]:
        if BrowserHelper.is_notes_mode(self.__browser):
            return item_ids
        else:
            return self.__item_id_cache.get_note_ids_by_card_ids(item_ids)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
