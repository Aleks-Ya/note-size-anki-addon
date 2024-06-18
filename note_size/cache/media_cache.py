import logging
import os
from logging import Logger
from threading import RLock

from anki.collection import Collection

from ..types import MediaFile, SizeBytes

log: Logger = logging.getLogger(__name__)


class MediaCache:

    def __init__(self, col: Collection):
        self.col: Collection = col
        self.file_sizes_cache: dict[MediaFile, SizeBytes] = {}
        self.total_file_size: SizeBytes = SizeBytes(0)
        self.lock: RLock = RLock()
        log.debug(f"{self.__class__.__name__} was instantiated")

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
                self._update_total_size(old_size, new_size)
                self.file_sizes_cache[file] = new_size
            return self.file_sizes_cache[file]

    def get_total_size(self) -> SizeBytes:
        with self.lock:
            return self.total_file_size

    def _update_total_size(self, old_size: SizeBytes, new_size: SizeBytes) -> None:
        self.total_file_size = SizeBytes(self.total_file_size - old_size + new_size)
