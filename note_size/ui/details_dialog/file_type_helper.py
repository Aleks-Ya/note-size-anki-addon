import logging
import mimetypes
import os
from logging import Logger
from typing import Any

from ...cache.cache import Cache
from ...types import FileType

log: Logger = logging.getLogger(__name__)


class FileTypeHelper(Cache):
    __exclusions: dict[str, FileType] = {
        ".webp": FileType.IMAGE,
        ".ashx": FileType.IMAGE,
        ".axd": FileType.IMAGE,
        ".cms": FileType.IMAGE,
        ".jpglarge": FileType.IMAGE,
    }

    def __init__(self) -> None:
        super().__init__()
        self.__cache: dict[str, FileType] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_file_type(self, filename: str, use_cache: bool = True) -> FileType:
        with self._lock:
            if use_cache and filename in self.__cache:
                return self.__cache[filename]
            else:
                file_type: FileType = FileTypeHelper.__determine_file_type(filename)
                self.__cache[filename] = file_type
                return file_type

    def invalidate_cache(self) -> None:
        with self._lock:
            self.__cache.clear()

    def as_dict_list(self) -> list[dict[Any, Any]]:
        with self._lock:
            return [self.__cache]

    def read_from_dict_list(self, dict_list: list[dict[Any, Any]]):
        with self._lock:
            self.__cache = dict_list[0]

    def get_cache_size(self) -> int:
        return len(self.__cache)

    @staticmethod
    def __determine_file_type(filename: str) -> FileType:
        full_mime_type: str = mimetypes.guess_type(filename)[0]
        if not full_mime_type:
            extension: str = os.path.splitext(filename)[1]
            if extension in FileTypeHelper.__exclusions:
                return FileTypeHelper.__exclusions[extension]
            return FileType.OTHER
        general_mime_type: str = full_mime_type.split("/")[0]
        if general_mime_type == "image":
            return FileType.IMAGE
        if general_mime_type == "audio":
            return FileType.AUDIO
        if general_mime_type == "video":
            return FileType.VIDEO
        return FileType.OTHER
