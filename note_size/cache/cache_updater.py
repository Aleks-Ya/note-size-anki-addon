import logging
from datetime import datetime
from logging import Logger
from typing import Sequence, Optional

from anki.collection import Collection
from anki.notes import NoteId
from aqt import AnkiQt
from aqt.operations import QueryOp
from aqt.qt import QWidget
from aqt.utils import showInfo, show_critical

from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..config.config import Config
from ..types import size_types

log: Logger = logging.getLogger(__name__)


class _WarmupCacheOp:
    __progress_dialog_title: str = '"Note Size" addon'

    def __init__(self, mw: AnkiQt, media_cache: MediaCache, item_id_cache: ItemIdCache, config: Config, parent: QWidget,
                 show_success_info: bool):
        self.__mw: AnkiQt = mw
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__config: Config = config
        self.__parent: QWidget = parent
        self.__show_success_info: bool = show_success_info
        log.debug(f"{self.__class__.__name__} was instantiated")

    def warmup_caches_in_background(self):
        if self.__config.get_cache_warmup_enabled():
            log.info("Warmup caches")
            QueryOp(parent=self.__parent, op=self.__background_op, success=self.__on_success).failure(
                self.__on_failure).with_progress("Note Size cache initializing").run_in_background()
        else:
            log.info("Cache warmup is disabled")
            self.__item_id_cache.set_initialized(True)

    def __background_op(self, col: Collection) -> int:
        read_from_file_success: bool = False
        if self.__config.get_store_cache_in_file_enabled():
            read_from_file_success = self.__item_id_cache.read_caches_from_file()
        else:
            log.info("Reading cache file is disabled")
        self.__item_id_cache.delete_cache_file()
        if not read_from_file_success:
            log.info(f"Cache warmup started: {self.__item_id_cache.get_size()}")
            start_time: datetime = datetime.now()
            self.__update_progress("Note Size cache initializing", None, None)

            all_note_ids: Sequence[NoteId] = col.find_notes("deck:*")
            note_number: int = len(all_note_ids)
            for i, note_id in enumerate(all_note_ids):
                if self.__mw.progress.want_cancel():
                    return 0
                for size_type in size_types:
                    self.__update_progress(f"Caching note sizes: {i} of {note_number}", i, note_number)
                    self.__item_id_cache.get_note_size_bytes(note_id, size_type, use_cache=True)
                    self.__item_id_cache.get_note_size_str(note_id, size_type, use_cache=True)
                    self.__item_id_cache.get_note_files(note_id, use_cache=True)

            all_card_ids: Sequence[int] = col.find_cards("deck:*")
            card_number: int = len(all_card_ids)
            for i, card_id in enumerate(all_card_ids):
                if self.__mw.progress.want_cancel():
                    return 0
                self.__update_progress(f"Caching card sizes: {i} of {card_number}", i, card_number)
                self.__item_id_cache.get_note_id_by_card_id(card_id)

            end_time: datetime = datetime.now()
            duration_sec: int = round((end_time - start_time).total_seconds())
            log.info(f"Cache warmup finished: notes={note_number}, cards={card_number}, "
                     f"duration_sec={duration_sec}, {self.__item_id_cache.get_size()}")
            return note_number + card_number
        else:
            log.info("Skip cache warmup because the cache was read from file")
            return 0

    def __update_progress(self, label: str, value: Optional[int], max_value: Optional[int]):
        if value and value % 1000 == 0:
            self.__mw.taskman.run_on_main(lambda: self.__update_progress_in_main(label, value, max_value))

    def __update_progress_in_main(self, label: str, value: Optional[int], max_value: Optional[int]):
        self.__mw.progress.set_title(self.__progress_dialog_title)
        self.__mw.progress.update(label=label, value=value, max=max_value)

    def __on_success(self, count: int) -> None:
        self.__item_id_cache.set_initialized(True)
        log.info(f"Cache initialization finished: {count}")
        if self.__show_success_info:
            showInfo(title=self.__progress_dialog_title, text=f"Cache was initialized ({count} notes and cards)")

    def __on_failure(self, e: Exception) -> None:
        log.error("Error during cache warmup", exc_info=e)
        show_critical(title=self.__progress_dialog_title, text="Cache initialization failed (see logs)")


class CacheUpdater:
    def __init__(self, mw: AnkiQt, media_cache: MediaCache, item_id_cache: ItemIdCache, config: Config):
        self.__mw: AnkiQt = mw
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self):
        _WarmupCacheOp(self.__mw, self.__media_cache, self.__item_id_cache, self.__config, self.__mw,
                       show_success_info=False).warmup_caches_in_background()

    def refresh_caches(self, parent: QWidget):
        log.info("Refresh caches")
        self.__item_id_cache.delete_cache_file()
        self.__media_cache.invalidate_cache()
        self.__item_id_cache.invalidate_caches()
        _WarmupCacheOp(self.__mw, self.__media_cache, self.__item_id_cache, self.__config, parent,
                       show_success_info=True).warmup_caches_in_background()

    def save_cache_to_file(self):
        if self.__config.get_store_cache_in_file_enabled():
            self.__item_id_cache.save_caches_to_file()
        else:
            log.info("Saving cache file is disabled")
            self.__item_id_cache.delete_cache_file()
