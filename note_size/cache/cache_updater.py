import logging
from datetime import datetime
from logging import Logger
from typing import Sequence

from anki.collection import Collection
from anki.notes import NoteId
from aqt import mw
from aqt.operations import QueryOp
from aqt.qt import QWidget
from aqt.utils import showInfo

from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from ..config.config import Config
from ..types import size_types

log: Logger = logging.getLogger(__name__)


class CacheUpdater:
    __op_title: str = '"Note Size" addon'

    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache, config: Config):
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__config: Config = config
        log.debug(f"{self.__class__.__name__} was instantiated")

    def initialize_caches(self):
        self.__read_cache_from_file()
        self.__warmup_caches(mw)

    def __read_cache_from_file(self):
        if self.__config.get_store_cache_in_file_enabled():
            op: QueryOp = QueryOp(parent=mw, op=self.__read_cache_file_background_op,
                                  success=self.__read_cache_file_success)
            op.with_progress().run_in_background()
        else:
            log.info("Reading cache file is disabled")

    def save_cache_to_file(self):
        if self.__config.get_store_cache_in_file_enabled():
            op: QueryOp = QueryOp(parent=mw, op=self.__save_cache_file_background_op,
                                  success=self.__save_cache_file_success)
            op.with_progress().run_in_background()
        else:
            log.info("Saving cache file is disabled")
            self.__item_id_cache.delete_cache_file()

    def __warmup_caches(self, parent: QWidget):
        if self.__config.get_cache_warmup_enabled():
            log.info("Warmup caches")
            op: QueryOp = QueryOp(parent=parent, op=self.__warmup_background_op, success=self.__warmup_success)
            op.with_progress().run_in_background()
        else:
            log.info("Cache warmup is disabled")

    def refresh_caches(self, parent: QWidget):
        log.info("Refresh caches")
        self.__item_id_cache.delete_cache_file()
        self.__media_cache.invalidate_cache()
        self.__item_id_cache.invalidate_caches()
        op: QueryOp = QueryOp(parent=parent, op=self.__warmup_background_op, success=self.__refresh_success)
        op.with_progress().run_in_background()

    def __warmup_background_op(self, col: Collection) -> int:
        log.info(f"Cache warmup started: {self.__item_id_cache.get_size()}")
        start_time: datetime = datetime.now()

        all_note_ids: Sequence[NoteId] = col.find_notes("deck:*")
        note_number: int = len(all_note_ids)
        for i, note_id in enumerate(all_note_ids):
            for size_type in size_types:
                self.__update_progress("Caching note sizes", i, note_number)
                self.__item_id_cache.get_note_size_bytes(note_id, size_type, use_cache=True)
                self.__item_id_cache.get_note_size_str(note_id, size_type, use_cache=True)

        all_card_ids: Sequence[int] = col.find_cards("deck:*")
        card_number: int = len(all_card_ids)
        for i, card_id in enumerate(all_card_ids):
            self.__update_progress("Caching card sizes", i, card_number)
            self.__item_id_cache.get_note_id_by_card_id(card_id)

        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Cache warmup finished: notes={note_number}, cards={card_number}, "
                 f"duration_sec={duration_sec}, {self.__item_id_cache.get_size()}")
        return note_number + card_number

    def __read_cache_file_background_op(self, _: Collection) -> int:
        mw.progress.set_title(CacheUpdater.__op_title)
        mw.progress.update(label="Reading note size cache from file...")
        self.__item_id_cache.read_caches_from_file()
        return 0

    def __save_cache_file_background_op(self, _: Collection) -> int:
        mw.progress.set_title(CacheUpdater.__op_title)
        mw.progress.update(label="Saving note size cache from file...")
        self.__item_id_cache.save_caches_to_file()
        return 0

    @staticmethod
    def __update_progress(label: str, value: int, max_value: int):
        if value % 1000 == 0:
            mw.taskman.run_on_main(lambda: CacheUpdater.__update_mw_progress(label, value, max_value))

    @staticmethod
    def __update_mw_progress(label: str, value: int, max_value: int):
        mw.progress.set_title(CacheUpdater.__op_title)
        mw.progress.update(label=f"{label}: {value} of {max_value}", value=value, max=max_value)

    @staticmethod
    def __warmup_success(count: int) -> None:
        log.info(f"Cache warmup finished: {count}")

    @staticmethod
    def __refresh_success(count: int) -> None:
        log.info(f"Cache refresh finished: {count}")
        showInfo(title=CacheUpdater.__op_title, text=f"Cache was refreshed ({count} notes and cards)")

    @staticmethod
    def __read_cache_file_success(_: int) -> None:
        log.info(f"Reading cache file finished")

    @staticmethod
    def __save_cache_file_success(_: int) -> None:
        log.info(f"Saving cache file finished")
