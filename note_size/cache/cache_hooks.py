import logging
from datetime import datetime
from logging import Logger
from typing import Sequence, Callable

from anki import hooks
from anki.collection import Collection
from anki.notes import NoteId, Note
from aqt import gui_hooks

from .cache_initializer import CacheInitializer
from .cache_manager import CacheManager
from ..calculator.updated_files_calculator import UpdatedFilesCalculator

log: Logger = logging.getLogger(__name__)


class CacheHooks:

    def __init__(self, cache_manager: CacheManager, cache_initializer: CacheInitializer,
                 updated_files_calculator: UpdatedFilesCalculator) -> None:
        self.__cache_manager: CacheManager = cache_manager
        self.__cache_initializer: CacheInitializer = cache_initializer
        self.__updated_files_calculator: UpdatedFilesCalculator = updated_files_calculator
        self.__last_update_media_sync_did_progress: datetime = datetime.now()
        self.__hook_add_cards_did_add_note: Callable[[Note], None] = self.__add_cards_did_add_note
        self.__hook_notes_will_be_deleted: Callable[[Collection, Sequence[NoteId]], None] = self.__notes_will_be_deleted
        self.__hook_media_sync_did_start_or_stop: Callable[[bool], None] = self.__media_sync_did_start_or_stop
        self.__hook_note_will_flush: Callable[[Note], None] = self.__on_note_will_flush
        self.__hook_profile_did_open: Callable[[], None] = self.__initialize_cache_on_profile_opening
        self.__hook_profile_will_close: Callable[[], None] = self.__save_cache_to_file
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.add_cards_did_add_note.append(self.__hook_add_cards_did_add_note)
        hooks.notes_will_be_deleted.append(self.__hook_notes_will_be_deleted)
        gui_hooks.media_sync_did_start_or_stop.append(self.__hook_media_sync_did_start_or_stop)
        hooks.note_will_flush.append(self.__hook_note_will_flush)
        gui_hooks.profile_did_open.append(self.__hook_profile_did_open)
        gui_hooks.profile_will_close.append(self.__hook_profile_will_close)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.add_cards_did_add_note.remove(self.__hook_add_cards_did_add_note)
        hooks.notes_will_be_deleted.remove(self.__hook_notes_will_be_deleted)
        gui_hooks.media_sync_did_start_or_stop.remove(self.__hook_media_sync_did_start_or_stop)
        hooks.note_will_flush.remove(self.__hook_note_will_flush)
        gui_hooks.profile_did_open.remove(self.__hook_profile_did_open)
        gui_hooks.profile_will_close.remove(self.__hook_profile_will_close)
        log.info(f"{self.__class__.__name__} was removed")

    def __initialize_cache_on_profile_opening(self) -> None:
        self.__cache_manager.invalidate_caches()
        self.__cache_manager.set_caches_initialized(False)
        self.__cache_initializer.warmup_caches()

    def __save_cache_to_file(self) -> None:
        self.__cache_initializer.save_cache_to_file()

    def __on_note_will_flush(self, note: Note) -> None:
        if note and note.id:
            self.__cache_manager.evict_note(note.id)

    def __add_cards_did_add_note(self, note: Note) -> None:
        log.info(f"Note was added: note={note.id}")
        self.__cache_manager.evict_note(note.id)

    def __notes_will_be_deleted(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        log.info(f"Notes will be deleted: note_ids={note_ids}")
        for note_id in note_ids:
            self.__cache_manager.evict_note(note_id)

    def __media_sync_did_start_or_stop(self, running: bool) -> None:
        log.info(f"MediaSyncDidStartOrStop: running={running}")
        if not running:
            note_ids: set[NoteId] = self.__updated_files_calculator.get_notes_having_updated_files()
            for note_id in note_ids:
                self.__cache_manager.evict_note(note_id)
            log.debug(f"Refreshing notes having updated files finished: refreshed {len(note_ids)} notes")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
