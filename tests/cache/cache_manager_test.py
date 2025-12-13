from anki.cards import Card
from anki.collection import Collection

from note_size.cache.cache import Cache
from note_size.cache.cache_manager import CacheManager
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.cache.note_size_cache import NoteSizeCache
from note_size.cache.bytes_note_size_cache import BytesNoteSizeCache
from note_size.cache.bytes_size_cache import BytesSizeCache
from note_size.cache.updated_files_cache import UpdatedFilesCache
from note_size.common.types import SizeType, SizeBytes
from note_size.cache.file_type_helper import FileTypeHelper
from tests import wait_until
from tests.conftest import item_id_cache
from tests.data import Data, MediaFiles, Digits


def test_get_caches(cache_manager: CacheManager, media_cache: MediaCache, item_id_cache: ItemIdCache,
                    bytes_note_size_cache: BytesNoteSizeCache, bytes_size_cache: BytesSizeCache, file_type_helper: FileTypeHelper,
                    note_size_cache: NoteSizeCache, updated_files_cache: UpdatedFilesCache):
    assert len(cache_manager.get_caches()) == 7
    assert media_cache in cache_manager.get_caches()
    assert item_id_cache in cache_manager.get_caches()
    assert bytes_note_size_cache in cache_manager.get_caches()
    assert bytes_size_cache in cache_manager.get_caches()
    assert file_type_helper in cache_manager.get_caches()
    assert note_size_cache in cache_manager.get_caches()
    assert updated_files_cache in cache_manager.get_caches()


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
                           item_id_cache: ItemIdCache, bytes_note_size_cache: BytesNoteSizeCache, bytes_size_cache: BytesSizeCache,
                           file_type_helper: FileTypeHelper, note_size_cache: NoteSizeCache, td: Data):
    assert media_cache.get_cache_size() == 0
    assert item_id_cache.get_cache_size() == 0
    assert bytes_note_size_cache.get_cache_size() == 0
    assert bytes_size_cache.get_cache_size() == 0
    assert file_type_helper.get_cache_size() == 0
    assert file_type_helper.get_cache_size() == 0
    assert note_size_cache.get_cache_size() == 0

    __use_all_caches(cache_manager, td)
    assert media_cache.get_cache_size() > 0
    assert item_id_cache.get_cache_size() > 0
    assert bytes_note_size_cache.get_cache_size() > 0
    assert bytes_size_cache.get_cache_size() > 0
    assert file_type_helper.get_cache_size() > 0
    assert note_size_cache.get_cache_size() > 0

    cache_manager.invalidate_caches()
    assert media_cache.get_cache_size() == 0
    assert item_id_cache.get_cache_size() == 0
    assert bytes_note_size_cache.get_cache_size() == 0
    assert bytes_size_cache.get_cache_size() == 0
    assert file_type_helper.get_cache_size() == 0
    assert note_size_cache.get_cache_size() == 0


def test_get_item_id_cache(cache_manager: CacheManager, item_id_cache: ItemIdCache):
    assert cache_manager.get_item_id_cache() == item_id_cache


def test_get_bytes_note_size_cache(cache_manager: CacheManager, bytes_note_size_cache: BytesNoteSizeCache):
    assert cache_manager.get_bytes_note_size_cache() == bytes_note_size_cache


def test_get_file_type_helper(cache_manager: CacheManager, file_type_helper: FileTypeHelper):
    assert cache_manager.get_file_type_helper() == file_type_helper


def test_get_note_size_cache(cache_manager: CacheManager, note_size_cache: NoteSizeCache):
    assert cache_manager.get_note_size_cache() == note_size_cache


def test_get_bytes_size_cache(cache_manager: CacheManager, bytes_size_cache: BytesSizeCache):
    assert cache_manager.get_bytes_size_cache() == bytes_size_cache


def test_updated_files_cache(cache_manager: CacheManager, updated_files_cache: UpdatedFilesCache):
    assert cache_manager.get_updated_files_cache() == updated_files_cache


def test_get_cache_size(cache_manager: CacheManager, media_cache: MediaCache,
                        item_id_cache: ItemIdCache, bytes_note_size_cache: BytesNoteSizeCache, bytes_size_cache: BytesSizeCache,
                        file_type_helper: FileTypeHelper, note_size_cache: NoteSizeCache, td: Data):
    assert cache_manager.get_cache_size() == 0
    __use_all_caches(cache_manager, td)
    assert cache_manager.get_cache_size() == 13


def test_evict_note(col: Collection, cache_manager: CacheManager, media_cache: MediaCache,
                    item_id_cache: ItemIdCache, bytes_note_size_cache: BytesNoteSizeCache, bytes_size_cache: BytesSizeCache,
                    file_type_helper: FileTypeHelper, note_size_cache: NoteSizeCache, td: Data):
    assert cache_manager.get_cache_size() == 0
    card: Card = __use_all_caches(cache_manager, td)
    wait_until(lambda: cache_manager.get_cache_size() == 13)
    cache_manager.evict_note(card.nid)
    wait_until(lambda: cache_manager.get_cache_size() == 6)


def __use_all_caches(cache_manager: CacheManager, td: Data) -> Card:
    card: Card = td.create_card_with_files()
    cache_manager.get_item_id_cache().get_note_id_by_card_id(card.id)
    cache_manager.get_note_size_cache().get_note_size_str(card.nid, SizeType.TOTAL, Digits.one, use_cache=True)
    cache_manager.get_file_type_helper().get_file_type(MediaFiles.picture, use_cache=True)
    cache_manager.get_bytes_note_size_cache().get_note_file_sizes(card.nid, use_cache=True)
    cache_manager.get_bytes_size_cache().bytes_to_str(SizeBytes(123), Digits.one, use_cache=True)
    cache_manager.get_updated_files_cache().get_notes_having_updated_files()
    return card
