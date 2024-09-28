from anki.collection import Collection
from anki.notes import Note

from note_size.cache.cache import Cache
from note_size.cache.cache_manager import CacheManager
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.cache.size_str_cache import SizeStrCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.types import SizeType
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper
from tests.conftest import item_id_cache
from tests.data import Data, DefaultFields


def test_get_caches(cache_manager: CacheManager, media_cache: MediaCache, item_id_cache: ItemIdCache,
                    size_calculator: SizeCalculator, size_formatter: SizeFormatter, file_type_helper: FileTypeHelper,
                    size_str_cache: SizeStrCache):
    assert len(cache_manager.get_caches()) == 6
    assert media_cache in cache_manager.get_caches()
    assert item_id_cache in cache_manager.get_caches()
    assert size_calculator in cache_manager.get_caches()
    assert size_formatter in cache_manager.get_caches()
    assert file_type_helper in cache_manager.get_caches()
    assert size_str_cache in cache_manager.get_caches()


def test_set_caches_initialized(cache_manager: CacheManager):
    caches: list[Cache] = cache_manager.get_caches()
    for cache in caches:
        assert not cache.is_initialized()
    cache_manager.set_caches_initialized(True)
    for cache in caches:
        assert cache.is_initialized()
    cache_manager.set_caches_initialized(False)
    for cache in caches:
        assert not cache.is_initialized()


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

    note: Note = td.create_note_with_files()
    card_id1: int = col.card_ids_of_note(note.id)[0]
    size_str_cache.get_note_size_str(note.id, SizeType.TOTAL, use_cache=False)
    file_type_helper.get_file_type(DefaultFields.file0, use_cache=True)
    item_id_cache.get_note_id_by_card_id(card_id1)
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


def test_size_str_cache(cache_manager: CacheManager, size_str_cache: SizeStrCache):
    assert cache_manager.get_size_str_cache() == size_str_cache
