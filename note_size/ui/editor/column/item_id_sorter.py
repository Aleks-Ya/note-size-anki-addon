import logging
from functools import partial
from logging import Logger
from typing import Sequence

from anki.notes import NoteId
from aqt.browser import ItemId

from ....cache.item_id_cache import ItemIdCache
from ....calculator.size_calculator import SizeCalculator
from ....types import SizeBytes, SizeType

log: Logger = logging.getLogger(__name__)


class ItemIdSorter:

    def __init__(self, item_id_cache: ItemIdCache, size_calculator: SizeCalculator) -> None:
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        log.debug(f"{self.__class__.__name__} was instantiated")

    def sort_item_ids(self, item_ids: Sequence[ItemId], size_type: SizeType, is_note: bool) -> Sequence[NoteId]:
        key_func: partial = partial(self.__get_item_size, size_type, is_note)
        return sorted(item_ids, key=key_func, reverse=True)

    def __get_item_size(self, size_type: SizeType, is_note: bool, item_id: ItemId) -> SizeBytes:
        note_id: NoteId = item_id if is_note else self.__item_id_cache.get_note_id_by_card_id(item_id)
        return self.__size_calculator.get_note_size(note_id, size_type, use_cache=True)
