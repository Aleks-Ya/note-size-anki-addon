import logging
from logging import Logger

from anki.notes import NoteId

from .cache import Cache
from .item_id_cache import ItemIdCache
from .media_cache import MediaCache
from .size_str_cache import SizeStrCache
from ..calculator.size_calculator import SizeCalculator
from ..calculator.size_formatter import SizeFormatter
from ..ui.details_dialog.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache, size_calculator: SizeCalculator,
                 size_formatter: SizeFormatter, file_type_helper: FileTypeHelper, size_str_cache: SizeStrCache) -> None:
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__size_str_cache: SizeStrCache = size_str_cache
        self.__caches: list[Cache] = [self.__media_cache, self.__item_id_cache, self.__size_formatter,
                                      self.__size_calculator, self.__file_type_helper, self.__size_str_cache]
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_caches(self) -> list[Cache]:
        return self.__caches

    def get_cache_size(self) -> int:
        return sum([cache.get_cache_size() for cache in self.__caches])

    def set_caches_initialized(self, initialized: bool) -> None:
        for cache in self.__caches:
            cache.set_initialized(initialized)

    def invalidate_caches(self) -> None:
        for cache in self.__caches:
            cache.invalidate_cache()

    def evict_note(self, note_id: NoteId) -> None:
        self.__item_id_cache.evict_note(note_id)
        self.__size_calculator.evict_note(note_id)
        self.__size_str_cache.evict_note(note_id)

    def get_item_id_cache(self) -> ItemIdCache:
        return self.__item_id_cache

    def get_size_calculator(self) -> SizeCalculator:
        return self.__size_calculator

    def get_file_type_helper(self) -> FileTypeHelper:
        return self.__file_type_helper

    def get_size_str_cache(self) -> SizeStrCache:
        return self.__size_str_cache
