import logging
import os
from datetime import datetime
from logging import Logger
from threading import RLock

from anki.collection import Collection
from anki.media_pb2 import CheckMediaResponse

from ..config.config import Config
from ..types import MediaFile, SizeBytes, FilesNumber

log: Logger = logging.getLogger(__name__)


class MediaCache:

    def __init__(self, col: Collection, config: Config):
        self.__config: Config = config
        self.__col: Collection = col
        self.__file_sizes_cache: dict[MediaFile, SizeBytes] = {}
        self.__total_files_size: SizeBytes = SizeBytes(0)
        self.__lock: RLock = RLock()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def warm_up_cache(self):
        with self.__lock:
            if not self.__config.get_cache_warmup_enabled():
                log.info("Cache warmup is disabled")
                return
            log.info("Warming up cache...")
            start_time: datetime = datetime.now()
            media_dir: str = self.__col.media.dir()
            listdir: list[str] = os.listdir(media_dir)
            for file in listdir:
                full_path: str = os.path.join(media_dir, file)
                new_size: SizeBytes = SizeBytes(os.path.getsize(full_path) if os.path.isfile(full_path) else 0)
                self.__file_sizes_cache[MediaFile(file)] = new_size
            self.__total_files_size = sum(self.__file_sizes_cache.values())
            end_time: datetime = datetime.now()
            duration_sec: int = round((end_time - start_time).total_seconds())
            log.info(f"Cache warming up finished: files_number={len(listdir)}, "
                     f"cache_len={len(self.__file_sizes_cache.keys())}, "
                     f"total_files_size={self.__total_files_size}, "
                     f"duration_sec={duration_sec}")

    def get_file_size(self, file: MediaFile, use_cache: bool) -> SizeBytes:
        with self.__lock:
            if not use_cache or file not in self.__file_sizes_cache:
                full_path: str = os.path.join(self.__col.media.dir(), file)
                if os.path.exists(full_path):
                    new_size: SizeBytes = SizeBytes(os.path.getsize(full_path))
                else:
                    log.warning(f"File absents: {full_path}")
                    new_size: SizeBytes = SizeBytes(0)
                old_size: SizeBytes = self.__file_sizes_cache[file] if file in self.__file_sizes_cache else SizeBytes(0)
                self.__update_total_files_size(old_size, new_size)
                self.__file_sizes_cache[file] = new_size
            return self.__file_sizes_cache[file]

    def get_total_files_size(self) -> SizeBytes:
        with self.__lock:
            return self.__total_files_size

    def invalidate_cache(self):
        with self.__lock:
            self.__file_sizes_cache.clear()
            self.__total_files_size: SizeBytes = SizeBytes(0)

    def get_unused_files_size(self, use_cache: bool) -> (SizeBytes, FilesNumber):
        log.debug("Calculating unused files size...")
        check_result: CheckMediaResponse = self.__col.media.check()
        unused_files: list[str] = list(check_result.unused)
        total_size: SizeBytes = SizeBytes(0)
        for unused_file in unused_files:
            media_file: MediaFile = MediaFile(unused_file)
            file_size: SizeBytes = self.get_file_size(media_file, use_cache)
            total_size += file_size
        log.debug(f"Calculated unused files size: {total_size}")
        return total_size, FilesNumber(len(unused_files))

    def __update_total_files_size(self, old_size: SizeBytes, new_size: SizeBytes) -> None:
        self.__total_files_size = SizeBytes(self.__total_files_size - old_size + new_size)
