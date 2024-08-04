import logging
import os
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
        self.__lock: RLock = RLock()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_file_size(self, file: MediaFile, use_cache: bool) -> SizeBytes:
        with self.__lock:
            if not use_cache or file not in self.__file_sizes_cache:
                full_path: str = os.path.join(self.__col.media.dir(), file)
                if os.path.exists(full_path):
                    new_size: SizeBytes = SizeBytes(os.path.getsize(full_path))
                else:
                    log.warning(f"File absents: {full_path}")
                    new_size: SizeBytes = SizeBytes(0)
                self.__file_sizes_cache[file] = new_size
            return self.__file_sizes_cache[file]

    def invalidate_cache(self):
        with self.__lock:
            self.__file_sizes_cache.clear()

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
