import logging
from logging import Logger
from typing import Sequence, Callable

from anki import hooks
from anki.collection import Collection
from anki.notes import NoteId, Note
from aqt import gui_hooks

from ..cache.item_id_cache import ItemIdCache
from ..cache.media_cache import MediaCache
from ..calculator.size_calculator import SizeCalculator

log: Logger = logging.getLogger(__name__)


class CacheHooks:

    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__hook_add_cards_did_add_note: Callable[[Note], None] = self.__add_cards_did_add_note
        self.__hook_notes_will_be_deleted: Callable[[Collection, Sequence[NoteId]], None] = self.__notes_will_be_deleted
        self.__hook_media_sync_did_start_or_stop: Callable[[bool], None] = self.__media_sync_did_start_or_stop
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.add_cards_did_add_note.append(self.__hook_add_cards_did_add_note)
        hooks.notes_will_be_deleted.append(self.__hook_notes_will_be_deleted)
        gui_hooks.media_sync_did_start_or_stop.append(self.__hook_media_sync_did_start_or_stop)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.add_cards_did_add_note.remove(self.__hook_add_cards_did_add_note)
        hooks.notes_will_be_deleted.remove(self.__hook_notes_will_be_deleted)
        gui_hooks.media_sync_did_start_or_stop.remove(self.__hook_media_sync_did_start_or_stop)
        log.info(f"{self.__class__.__name__} was removed")

    def __add_cards_did_add_note(self, note: Note) -> None:
        log.info(f"Note was added: note={note.id}")
        self.__item_id_cache.refresh_note(note.id)

    def __notes_will_be_deleted(self, col: Collection, note_ids: Sequence[NoteId]) -> None:
        log.info(f"Notes will be deleted: note_ids={note_ids}")
        for note_id in note_ids:
            self.__item_id_cache.evict_note(note_id)
            note: Note = col.get_note(note_id)
            self.__size_calculator.file_sizes(note, use_cache=True)

    def __media_sync_did_start_or_stop(self, running: bool) -> None:
        log.info(f"MediaSyncDidStartOrStop: running={running}")
        if not running:
            self.__media_cache.warm_up_cache()
