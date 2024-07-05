import logging
from logging import Logger
from typing import Sequence, Callable

from anki import hooks
from anki.collection import Collection
from anki.notes import NoteId, Note

from ..cache.item_id_cache import ItemIdCache
from ..cache.media_cache import MediaCache
from ..calculator.size_calculator import SizeCalculator
from ..types import MediaFile, SizeBytes

log: Logger = logging.getLogger(__name__)


class CacheHooks:

    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__hook_notes_will_be_deleted: Callable[[Collection, Sequence[NoteId]], None] = self.__notes_will_be_deleted
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        hooks.notes_will_be_deleted.append(self.__hook_notes_will_be_deleted)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        hooks.notes_will_be_deleted.remove(self.__hook_notes_will_be_deleted)
        log.info(f"{self.__class__.__name__} was removed")

    def __notes_will_be_deleted(self, col: Collection, note_ids: Sequence[NoteId]) -> None:
        log.info(f"Notes will be deleted: note_ids={note_ids}")
        for note_id in note_ids:
            self.__item_id_cache.evict_note(note_id)
            note: Note = col.get_note(note_id)
            file_sizes: dict[MediaFile, SizeBytes] = self.__size_calculator.file_sizes(note, use_cache=True)
