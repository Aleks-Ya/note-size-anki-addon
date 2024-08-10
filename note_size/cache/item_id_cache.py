import logging
import os
import pickle
from logging import Logger
from pathlib import Path
from threading import RLock
from typing import Sequence, Any

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import NoteId, Note

from .media_cache import MediaCache
from ..config.config import Config
from ..config.settings import Settings
from ..types import SizeStr, SizeBytes, SizeType, size_types, MediaFile, FilesNumber
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class ItemIdCache:

    def __init__(self, col: Collection, size_calculator: SizeCalculator, media_cache: MediaCache, config: Config,
                 settings: Settings):
        self.__config: Config = config
        self.__lock: RLock = RLock()
        self.__col: Collection = col
        self.__size_calculator: SizeCalculator = size_calculator
        self.__media_cache: MediaCache = media_cache
        self.__cache_file: Path = settings.cache_file
        self.__id_cache: dict[CardId, NoteId]
        self.__size_bytes_caches: dict[SizeType, dict[NoteId, SizeBytes]]
        self.__size_str_caches: dict[SizeType, dict[NoteId, SizeStr]]
        self.__note_files_cache: dict[NoteId, list[MediaFile]]
        self.invalidate_caches()
        self.__initialized: bool = False
        log.debug(f"{self.__class__.__name__} was instantiated")

    def is_initialized(self) -> bool:
        initialized: bool = False
        if self.__lock.acquire(blocking=False):
            try:
                initialized = self.__initialized
            finally:
                self.__lock.release()
        log.debug(f"Is initialized: {initialized}")
        return initialized

    def set_initialized(self, initialized: bool) -> None:
        with self.__lock:
            self.__initialized = initialized
            log.debug(f"Set initialized: {initialized}")

    def get_note_id_by_card_id(self, card_id: CardId) -> NoteId:
        with self.__lock:
            if card_id not in self.__id_cache:
                self.__id_cache[card_id] = self.__col.get_card(card_id).nid
            return self.__id_cache[card_id]

    def get_note_size_bytes(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeBytes:
        with self.__lock:
            cache: dict[NoteId, SizeBytes] = self.__size_bytes_caches[size_type]
            if use_cache and note_id in cache:
                return cache[note_id]
            else:
                if size_type == SizeType.TOTAL:
                    size: SizeBytes = SizeBytes(self.get_note_size_bytes(note_id, SizeType.TEXTS, use_cache) +
                                                self.get_note_size_bytes(note_id, SizeType.FILES, use_cache))
                if size_type == SizeType.TEXTS:
                    size: SizeBytes = self.__size_calculator.calculate_texts_size(self.__col.get_note(note_id))
                if size_type == SizeType.FILES:
                    size: SizeBytes = self.__size_calculator.calculate_files_size(self.__col.get_note(note_id),
                                                                                  use_cache)
                cache[note_id] = size
                return cache[note_id]

    def get_note_size_str(self, note_id: NoteId, size_type: SizeType, use_cache: bool) -> SizeStr:
        with self.__lock:
            cache: dict[NoteId, SizeStr] = self.__size_str_caches[size_type]
            if use_cache and note_id in cache:
                return cache[note_id]
            else:
                size: SizeBytes = self.get_note_size_bytes(note_id, size_type, use_cache)
                cache[note_id] = SizeFormatter.bytes_to_str(size)
                return cache[note_id]

    def refresh_note(self, note_id: NoteId) -> None:
        for size_type in size_types:
            self.get_note_size_str(note_id, size_type, use_cache=False)
            self.get_note_files(note_id, use_cache=False)

    def evict_note(self, note_id: NoteId) -> None:
        with self.__lock:
            for cache in self.__size_bytes_caches.values():
                if note_id in cache:
                    del cache[note_id]
            for cache in self.__size_str_caches.values():
                if note_id in cache:
                    del cache[note_id]
            for cid, nid in list(self.__id_cache.items()):
                if nid == note_id and note_id in self.__id_cache:
                    del self.__id_cache[cid]

    def as_dict_list(self) -> list[dict[str, Any]]:
        return [self.__id_cache, self.__size_bytes_caches, self.__size_str_caches, self.__note_files_cache]

    def save_caches_to_file(self) -> None:
        with self.__lock:
            try:
                log.info(f"Saving cache file: {self.__cache_file}")
                pickle.dump(self.as_dict_list(), self.__cache_file.open("wb"))
                log.info(f"Caches were saved to file: {self.__cache_file}")
            except Exception:
                log.warning(f"Cannot save cache file: {self.__cache_file}", exc_info=True)

    def read_caches_from_file(self) -> bool:
        if self.__cache_file.exists():
            log.info(f"Reading cache file: {self.__cache_file}")
            with self.__lock:
                try:
                    caches: list[dict] = pickle.load(open(self.__cache_file, 'rb'))
                    self.__id_cache: dict[CardId, NoteId] = caches[0]
                    self.__size_bytes_caches: dict[SizeType, dict[NoteId, SizeBytes]] = caches[1]
                    self.__size_str_caches: dict[SizeType, dict[NoteId, SizeStr]] = caches[2]
                    self.__note_files_cache: dict[NoteId, list[MediaFile]] = caches[3]
                    log.info(f"Caches were read from file: {self.__cache_file}")
                    return True
                except Exception:
                    log.warning(f"Cannot deserialize cache file: {self.__cache_file}", exc_info=True)
                    self.invalidate_caches()
                    self.delete_cache_file()
        else:
            log.info(f"Skip reading absent cache file: {self.__cache_file}")
        return False

    def get_note_files(self, note_id: NoteId, use_cache: bool) -> list[MediaFile]:
        with self.__lock:
            if use_cache and note_id in self.__note_files_cache:
                return self.__note_files_cache[note_id]
            else:
                note: Note = self.__col.get_note(note_id)
                files: list[MediaFile] = self.__size_calculator.note_files(note)
                self.__note_files_cache[note_id] = files
                return files

    def get_used_files_size(self, use_cache: bool) -> (SizeBytes, FilesNumber):
        all_note_ids: Sequence[NoteId] = self.__col.find_notes("deck:*")
        files_list: list[list[MediaFile]] = [self.get_note_files(note_id, use_cache) for note_id in all_note_ids]
        files: set[MediaFile] = {file for sublist in files_list for file in sublist}
        files_size: SizeBytes = self.__size_calculator.calculate_size_of_files(files, use_cache)
        return files_size, FilesNumber(len(files))

    def __size_bytes_cache_lengths(self) -> str:
        return str([f"{cache[0]}={len(cache[1].keys())}" for cache in self.__size_bytes_caches.items()])

    def __size_str_cache_lengths(self) -> str:
        return str([f"{cache[0]}={len(cache[1].keys())}" for cache in self.__size_str_caches.items()])

    def get_size(self) -> str:
        return (f"size_bytes_cache_lengths={self.__size_bytes_cache_lengths()}, "
                f"size_str_cache_lengths={self.__size_str_cache_lengths()}, "
                f"id_cache_length={len(self.__id_cache.keys())}, "
                f"note_files_cache={len(self.__note_files_cache.keys())}")

    def invalidate_caches(self) -> None:
        with self.__lock:
            self.__id_cache: dict[CardId, NoteId] = {}
            self.__size_bytes_caches: dict[SizeType, dict[NoteId, SizeBytes]] = {SizeType.TOTAL: {},
                                                                                 SizeType.TEXTS: {},
                                                                                 SizeType.FILES: {}}
            self.__size_str_caches: dict[SizeType, dict[NoteId, SizeStr]] = {SizeType.TOTAL: {},
                                                                             SizeType.TEXTS: {},
                                                                             SizeType.FILES: {}}
            self.__note_files_cache: dict[NoteId, list[MediaFile]] = {}

    def delete_cache_file(self):
        if self.__cache_file.exists():
            os.remove(self.__cache_file)
            log.info(f"Cache file was deleted: {self.__cache_file}")

    def refresh_notes_having_updated_files(self):
        if self.is_initialized():
            log.debug("Refreshing notes having updated files started")
            updated_files: list[MediaFile] = self.__media_cache.get_updated_files()
            counter: int = 0
            for updated_file in updated_files:
                updated_note_ids: list[NoteId] = self.__note_ids_by_file(updated_file)
                for note_id in updated_note_ids:
                    self.refresh_note(note_id)
                    counter += 1
            log.debug(f"Refreshing notes having updated files finished: "
                      f"refreshed {counter} notes with {len(updated_files)} files")
        else:
            log.debug("Skip refreshing notes having updated files because ItemIdCache is not initialized")

    def __note_ids_by_file(self, file: MediaFile) -> list[NoteId]:
        note_ids: list[NoteId] = []
        for note_id, media_files in self.__note_files_cache.items():
            if file in media_files:
                note_ids.append(note_id)
        return note_ids
