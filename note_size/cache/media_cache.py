import logging
import os
from datetime import datetime
from logging import Logger
from threading import RLock

from anki.collection import Collection

from ..config.config import Config
from ..types import MediaFile, SizeBytes

log: Logger = logging.getLogger(__name__)


class MediaCache:

    def __init__(self, col: Collection, config: Config):
        self.warmup_enabled: bool = config.cache_warm_up_enabled()
        self.col: Collection = col
        self.file_sizes_cache: dict[MediaFile, SizeBytes] = {}
        self.total_file_size: SizeBytes = SizeBytes(0)
        self.lock: RLock = RLock()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def warm_up_cache(self):
        with self.lock:
            if not self.warmup_enabled:
                log.info("Cache warmup is disabled")
                return
            log.info("Warming up cache...")
            start_time: datetime = datetime.now()
            media_dir: str = self.col.media.dir()
            listdir: list[str] = os.listdir(media_dir)
            for file in listdir:
                full_path: str = os.path.join(media_dir, file)
                new_size: SizeBytes = SizeBytes(os.path.getsize(full_path) if os.path.isfile(full_path) else 0)
                self.file_sizes_cache[MediaFile(file)] = new_size
            self.total_file_size = sum(self.file_sizes_cache.values())
            end_time: datetime = datetime.now()
            duration_sec: int = round((end_time - start_time).total_seconds())
            log.info(f"Cache warming up finished: files_number={len(listdir)}, "
                     f"cache_len={len(self.file_sizes_cache.keys())}, "
                     f"total_file_size={self.total_file_size}, "
                     f"duration_sec={duration_sec}")

    def get_file_size(self, file: MediaFile, use_cache: bool) -> SizeBytes:
        with self.lock:
            if not use_cache or file not in self.file_sizes_cache:
                full_path: str = os.path.join(self.col.media.dir(), file)
                if os.path.exists(full_path):
                    new_size: SizeBytes = SizeBytes(os.path.getsize(full_path))
                else:
                    log.warning(f"File absents: {full_path}")
                    new_size: SizeBytes = SizeBytes(0)
                old_size: SizeBytes = self.file_sizes_cache[file] if file in self.file_sizes_cache else SizeBytes(0)
                self.__update_total_size(old_size, new_size)
                self.file_sizes_cache[file] = new_size
            return self.file_sizes_cache[file]

    def get_total_size(self) -> SizeBytes:
        with self.lock:
            return self.total_file_size

    def __update_total_size(self, old_size: SizeBytes, new_size: SizeBytes) -> None:
        self.total_file_size = SizeBytes(self.total_file_size - old_size + new_size)
