import logging
from logging import Logger

from anki.notes import NoteId

from .cache import Cache
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from .note_size_cache import NoteSizeCache
from ..calculator.bytes_note_size_cache import BytesNoteSizeCache
from .bytes_size_cache import BytesSizeCache
from .updated_files_cache import UpdatedFilesCache
from .file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache, bytes_note_size_cache: BytesNoteSizeCache,
                 bytes_size_cache: BytesSizeCache, file_type_helper: FileTypeHelper, note_size_cache: NoteSizeCache,
                 updated_files_cache: UpdatedFilesCache) -> None:
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__bytes_note_size_cache: BytesNoteSizeCache = bytes_note_size_cache
        self.__bytes_size_cache: BytesSizeCache = bytes_size_cache
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__note_size_cache: NoteSizeCache = note_size_cache
        self.__updated_files_cache: UpdatedFilesCache = updated_files_cache
        self.__caches: list[Cache] = [self.__media_cache, self.__item_id_cache, self.__bytes_size_cache,
                                      self.__bytes_note_size_cache, self.__file_type_helper, self.__note_size_cache,
                                      self.__updated_files_cache]
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_caches(self) -> list[Cache]:
        return self.__caches

    def get_cache_size(self) -> int:
        return sum([cache.get_cache_size() for cache in self.__caches])

    def set_caches_initialized(self, initialized: bool) -> None:
        for cache in self.__caches:
            cache.set_initialized(initialized)

    def get_caches_initialized(self) -> bool:
        for cache in self.__caches:
            if not cache.is_initialized():
                return False
        return True

    def invalidate_caches(self) -> None:
        log.debug("Invalidate caches")
        for cache in self.__caches:
            cache.invalidate_cache()

    def evict_note(self, note_id: NoteId) -> None:
        self.__item_id_cache.evict_note(note_id)
        self.__bytes_note_size_cache.evict_note(note_id)
        self.__note_size_cache.evict_note(note_id)
        self.__updated_files_cache.evict_note(note_id)

    def get_item_id_cache(self) -> ItemIdCache:
        return self.__item_id_cache

    def get_bytes_note_size_cache(self) -> BytesNoteSizeCache:
        return self.__bytes_note_size_cache

    def get_file_type_helper(self) -> FileTypeHelper:
        return self.__file_type_helper

    def get_note_size_cache(self) -> NoteSizeCache:
        return self.__note_size_cache

    def get_bytes_size_cache(self) -> BytesSizeCache:
        return self.__bytes_size_cache

    def get_updated_files_cache(self) -> UpdatedFilesCache:
        return self.__updated_files_cache

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
