from typing import Optional

from anki.cards import Card
from anki.collection import Collection
from aqt.deckbrowser import DeckBrowser
from aqt.taskman import TaskManager

from note_size.cache.cache_initializer_background import CacheInitializerBackground
from note_size.cache.cache_manager import CacheManager
from note_size.cache.cache_storage import CacheStorage
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.config.config import Config
from note_size.common.types import FileType, SizeType, FileSize, SizeBytes
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper
from tests.conftest import cache_manager
from tests.data import Data, MediaFiles, Digits

update_progress_history: list[str] = []


def update_progress_callback(label: str, value: Optional[int], max_value: Optional[int]):
    update_progress_history.append(f"{label} - {value} - {max_value}")


def test_initialize_caches(td: Data, col: Collection, cache_manager: CacheManager, media_cache: MediaCache,
                           item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                           file_type_helper: FileTypeHelper, config: Config, cache_storage: CacheStorage,
                           task_manager: TaskManager, deck_browser: DeckBrowser):
    card1: Card = td.create_card_with_files()
    card2: Card = td.create_card_without_files()

    assert not media_cache.is_initialized()
    assert not item_id_cache.is_initialized()
    assert not size_calculator.is_initialized()
    assert not size_formatter.is_initialized()
    assert not file_type_helper.is_initialized()

    cache_initializer_background: CacheInitializerBackground = CacheInitializerBackground(
        cache_storage, cache_manager, deck_browser, task_manager, config, update_progress_callback)
    count: int = cache_initializer_background.initialize_caches(col)
    assert count == 2
    assert update_progress_history == []

    assert media_cache.is_initialized()
    assert item_id_cache.is_initialized()
    assert size_calculator.is_initialized()
    assert size_formatter.is_initialized()
    assert file_type_helper.is_initialized()

    assert media_cache.as_dict_list() == [{MediaFiles.animation: FileSize(SizeBytes(9)),
                                           MediaFiles.picture: FileSize(SizeBytes(7)),
                                           MediaFiles.sound: FileSize(SizeBytes(5))}]
    assert item_id_cache.as_dict_list() == [{card1.id: card1.nid,
                                             card2.id: card2.nid}]
    assert size_calculator.as_dict_list() == [{SizeType.TOTAL: {card1.nid: 144, card2.nid: 71},
                                               SizeType.TEXTS: {card1.nid: 123, card2.nid: 71},
                                               SizeType.FILES: {card1.nid: 21, card2.nid: 0}},
                                              {card1.nid: {MediaFiles.picture, MediaFiles.sound, MediaFiles.animation},
                                               card2.nid: set()},
                                              {card1.nid: {MediaFiles.animation: FileSize(SizeBytes(9)),
                                                           MediaFiles.picture: FileSize(SizeBytes(7)),
                                                           MediaFiles.sound: FileSize(SizeBytes(5))},
                                               card2.nid: {}}]
    assert size_formatter.as_dict_list() == [{SizeBytes(0): {Digits.two: '0 B'},
                                              SizeBytes(21): {Digits.two: '21 B'},
                                              SizeBytes(71): {Digits.two: '71 B'},
                                              SizeBytes(123): {Digits.two: '123 B'},
                                              SizeBytes(144): {Digits.two: '144 B'}}]
    assert file_type_helper.as_dict_list() == [{MediaFiles.animation: FileType.IMAGE,
                                                MediaFiles.picture: FileType.IMAGE,
                                                MediaFiles.sound: FileType.AUDIO}]


def test_update_progress(td: Data, col: Collection, cache_manager: CacheManager, media_cache: MediaCache,
                         item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                         file_type_helper: FileTypeHelper, config: Config, cache_storage: CacheStorage,
                         task_manager: TaskManager, deck_browser: DeckBrowser):
    update_progress_step: int = 10
    note_count: int = update_progress_step * 2 + 1
    for _ in range(note_count):
        td.create_note_without_files()
    cache_initializer_background: CacheInitializerBackground = CacheInitializerBackground(
        cache_storage, cache_manager, deck_browser, task_manager, config, update_progress_callback,
        update_progress_step)
    count: int = cache_initializer_background.initialize_caches(col)
    assert count == 21
    assert update_progress_history == ['Caching note sizes: 10 of 21 - 10 - 21',
                                       'Caching note sizes: 20 of 21 - 20 - 21']
