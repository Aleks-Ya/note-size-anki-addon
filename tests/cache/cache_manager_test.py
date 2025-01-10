from anki.cards import Card
from anki.collection import Collection

from note_size.cache.cache import Cache
from note_size.cache.cache_manager import CacheManager
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.cache.size_str_cache import SizeStrCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.types import SizeType, SizeBytes
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper
from tests import wait_until
from tests.conftest import item_id_cache
from tests.data import Data, MediaFiles, Precisions


def test_get_caches(cache_manager: CacheManager, media_cache: MediaCache, item_id_cache: ItemIdCache,
                    size_calculator: SizeCalculator, size_formatter: SizeFormatter, file_type_helper: FileTypeHelper,
                    size_str_cache: SizeStrCache, updated_files_calculator: UpdatedFilesCalculator):
    assert len(cache_manager.get_caches()) == 7
    assert media_cache in cache_manager.get_caches()
    assert item_id_cache in cache_manager.get_caches()
    assert size_calculator in cache_manager.get_caches()
    assert size_formatter in cache_manager.get_caches()
    assert file_type_helper in cache_manager.get_caches()
    assert size_str_cache in cache_manager.get_caches()
    assert updated_files_calculator in cache_manager.get_caches()


def test_set_caches_initialized(cache_manager: CacheManager):
    caches: list[Cache] = cache_manager.get_caches()
    assert not cache_manager.get_caches_initialized()
    for cache in caches:
        assert not cache.is_initialized()
    cache_manager.set_caches_initialized(True)
    assert cache_manager.get_caches_initialized()
    for cache in caches:
        assert cache.is_initialized()
    cache_manager.set_caches_initialized(False)
    assert not cache_manager.get_caches_initialized()
    for cache in caches:
        assert not cache.is_initialized()


def test_cache_initialized(cache_manager: CacheManager):
    assert not cache_manager.get_caches_initialized()
    cache_manager.set_caches_initialized(True)
    assert cache_manager.get_caches_initialized()
    cache_manager.get_item_id_cache().set_initialized(False)
    assert not cache_manager.get_caches_initialized()


def test_invalidate_caches(col: Collection, cache_manager: CacheManager, media_cache: MediaCache,
                           item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                           file_type_helper: FileTypeHelper, size_str_cache: SizeStrCache, td: Data):
    assert media_cache.get_cache_size() == 0
    assert item_id_cache.get_cache_size() == 0
    assert size_calculator.get_cache_size() == 0
    assert size_formatter.get_cache_size() == 0
    assert file_type_helper.get_cache_size() == 0
    assert file_type_helper.get_cache_size() == 0
    assert size_str_cache.get_cache_size() == 0

    __use_all_caches(cache_manager, td)
    assert media_cache.get_cache_size() > 0
    assert item_id_cache.get_cache_size() > 0
    assert size_calculator.get_cache_size() > 0
    assert size_formatter.get_cache_size() > 0
    assert file_type_helper.get_cache_size() > 0
    assert size_str_cache.get_cache_size() > 0

    cache_manager.invalidate_caches()
    assert media_cache.get_cache_size() == 0
    assert item_id_cache.get_cache_size() == 0
    assert size_calculator.get_cache_size() == 0
    assert size_formatter.get_cache_size() == 0
    assert file_type_helper.get_cache_size() == 0
    assert size_str_cache.get_cache_size() == 0


def test_get_item_id_cache(cache_manager: CacheManager, item_id_cache: ItemIdCache):
    assert cache_manager.get_item_id_cache() == item_id_cache


def test_get_size_calculator(cache_manager: CacheManager, size_calculator: SizeCalculator):
    assert cache_manager.get_size_calculator() == size_calculator


def test_get_file_type_helper(cache_manager: CacheManager, file_type_helper: FileTypeHelper):
    assert cache_manager.get_file_type_helper() == file_type_helper


def test_get_size_str_cache(cache_manager: CacheManager, size_str_cache: SizeStrCache):
    assert cache_manager.get_size_str_cache() == size_str_cache


def test_get_size_formatter(cache_manager: CacheManager, size_formatter: SizeFormatter):
    assert cache_manager.get_size_formatter() == size_formatter


def test_updated_files_calculator(cache_manager: CacheManager, updated_files_calculator: UpdatedFilesCalculator):
    assert cache_manager.get_updated_files_calculator() == updated_files_calculator


def test_get_cache_size(cache_manager: CacheManager, media_cache: MediaCache,
                        item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                        file_type_helper: FileTypeHelper, size_str_cache: SizeStrCache, td: Data):
    assert cache_manager.get_cache_size() == 0
    __use_all_caches(cache_manager, td)
    assert cache_manager.get_cache_size() == 13


def test_evict_note(col: Collection, cache_manager: CacheManager, media_cache: MediaCache,
                    item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                    file_type_helper: FileTypeHelper, size_str_cache: SizeStrCache, td: Data):
    assert cache_manager.get_cache_size() == 0
    card: Card = __use_all_caches(cache_manager, td)
    wait_until(lambda: cache_manager.get_cache_size() == 13)
    cache_manager.evict_note(card.nid)
    wait_until(lambda: cache_manager.get_cache_size() == 6)


def __use_all_caches(cache_manager: CacheManager, td: Data) -> Card:
    card: Card = td.create_card_with_files()
    cache_manager.get_item_id_cache().get_note_id_by_card_id(card.id)
    cache_manager.get_size_str_cache().get_note_size_str(card.nid, SizeType.TOTAL, use_cache=True,
                                                         precision=Precisions.one)
    cache_manager.get_file_type_helper().get_file_type(MediaFiles.picture, use_cache=True)
    cache_manager.get_size_calculator().get_note_file_sizes(card.nid, use_cache=True)
    cache_manager.get_size_formatter().bytes_to_str(SizeBytes(123), use_cache=True, precision=Precisions.one)
    cache_manager.get_updated_files_calculator().get_notes_having_updated_files()
    return card
