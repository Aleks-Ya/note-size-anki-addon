import logging
import os
from logging import Logger
from pathlib import Path
from typing import Any

from anki.collection import Collection
from anki.media_pb2 import CheckMediaResponse

from .cache import Cache
from ..config.config import Config
from ..types import MediaFile, SizeBytes, FilesNumber

log: Logger = logging.getLogger(__name__)


class MediaCache(Cache):

    def __init__(self, col: Collection, config: Config) -> None:
        super().__init__()
        self.__config: Config = config
        self.__col: Collection = col
        self.__media_dir: Path = Path(col.media.dir())
        self.__file_sizes_cache: dict[MediaFile, SizeBytes] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_file_size(self, file: MediaFile, use_cache: bool) -> SizeBytes:
        with self._lock:
            if not use_cache or file not in self.__file_sizes_cache:
                full_path: Path = self.__media_dir.joinpath(file)
                if os.path.exists(full_path):
                    new_size: SizeBytes = SizeBytes(os.path.getsize(full_path))
                else:
                    log.warning(f"File absents: {full_path}")
                    new_size: SizeBytes = SizeBytes(0)
                self.__file_sizes_cache[file] = new_size
            return self.__file_sizes_cache[file]

    def invalidate_cache(self) -> None:
        with self._lock:
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
        files_number: FilesNumber = FilesNumber(len(unused_files))
        log.debug(f"Calculated unused: total_size={total_size}, files_number={files_number}")
        return total_size, files_number

    def get_updated_files(self) -> set[MediaFile]:
        updated_files: set[MediaFile] = set()
        for file in self.__media_dir.iterdir():
            if file.is_file():
                media_file: MediaFile = MediaFile(file.name)
                cached_file_size: SizeBytes = self.get_file_size(media_file, use_cache=True)
                actual_file_size: SizeBytes = self.get_file_size(media_file, use_cache=False)
                if cached_file_size != actual_file_size:
                    updated_files.add(media_file)
        log.debug(f"Found updated files: {len(updated_files)}")
        return updated_files

    def as_dict_list(self) -> list[dict[Any, Any]]:
        return [self.__file_sizes_cache]

    def read_from_dict_list(self, caches: list[dict[Any, Any]]):
        with self._lock:
            self.__file_sizes_cache = caches[0]
            log.info(f"Cache was read from dict list")

    def get_cache_size(self) -> int:
        return len(self.__file_sizes_cache)
