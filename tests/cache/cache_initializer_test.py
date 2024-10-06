from pathlib import Path

from anki.cards import Card

from note_size.cache.cache_initializer import CacheInitializer
from note_size.cache.cache_manager import CacheManager
from note_size.cache.cache_storage import CacheStorage
from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.types import SizeType
from tests.conftest import cache_manager
from tests.data import Data, FileNames

update_progress_history: list[str] = []


def test_initialize_caches_no_file(cache_initializer: CacheInitializer, cache_manager: CacheManager):
    assert cache_manager.get_cache_size() == 0
    for cache in cache_manager.get_caches():
        assert not cache.is_initialized()
    cache_initializer.initialize_caches()
    for cache in cache_manager.get_caches():
        assert cache.is_initialized()
    assert cache_manager.get_cache_size() == 0


def test_initialize_caches_from_file(cache_initializer: CacheInitializer, td: Data, cache_manager: CacheManager,
                                     cache_storage: CacheStorage, settings: Settings):
    __fill_cache(cache_manager, td)
    assert cache_manager.get_cache_size() == 12

    cache_file: Path = settings.cache_file
    assert not cache_file.exists()
    cache_storage.save_caches_to_file(cache_manager.get_caches())
    assert cache_file.exists()

    cache_manager.invalidate_caches()
    cache_manager.set_caches_initialized(False)
    assert cache_manager.get_cache_size() == 0

    assert cache_file.exists()
    for cache in cache_manager.get_caches():
        assert not cache.is_initialized()
    cache_initializer.initialize_caches()
    for cache in cache_manager.get_caches():
        assert cache.is_initialized()
    assert cache_manager.get_cache_size() == 12
    assert not cache_file.exists()


def test_save_cache_to_file_enabled(cache_initializer: CacheInitializer, td: Data, cache_manager: CacheManager,
                                    settings: Settings, config: Config):
    assert config.get_store_cache_in_file_enabled()
    __fill_cache(cache_manager, td)
    assert cache_manager.get_cache_size() == 12

    cache_file: Path = settings.cache_file
    assert not cache_file.exists()
    cache_initializer.save_cache_to_file()
    assert cache_file.exists()


def test_save_cache_to_file_disabled(cache_initializer: CacheInitializer, td: Data, cache_manager: CacheManager,
                                     settings: Settings, config: Config):
    config.set_store_cache_in_file_enabled(False)
    __fill_cache(cache_manager, td)
    assert cache_manager.get_cache_size() == 12

    cache_file: Path = settings.cache_file
    assert not cache_file.exists()
    cache_initializer.save_cache_to_file()
    assert not cache_file.exists()


def test_save_cache_to_file_delete_existing(cache_initializer: CacheInitializer, td: Data, cache_manager: CacheManager,
                                            settings: Settings, config: Config):
    cache_file: Path = settings.cache_file
    __fill_cache(cache_manager, td)

    assert config.get_store_cache_in_file_enabled()
    assert cache_manager.get_cache_size() == 12
    assert not cache_file.exists()
    cache_initializer.save_cache_to_file()
    assert cache_file.exists()

    config.set_store_cache_in_file_enabled(False)
    assert cache_file.exists()
    cache_initializer.save_cache_to_file()
    assert not cache_file.exists()


def __fill_cache(cache_manager, td) -> None:
    card: Card = td.create_card_with_files()
    cache_manager.get_item_id_cache().get_note_id_by_card_id(card.id)
    cache_manager.get_size_calculator().get_note_size(card.nid, SizeType.TOTAL, use_cache=True)
    cache_manager.get_file_type_helper().get_file_type(FileNames.image, use_cache=True)
    cache_manager.get_size_str_cache().get_note_size_str(card.nid, SizeType.TOTAL, use_cache=True)
