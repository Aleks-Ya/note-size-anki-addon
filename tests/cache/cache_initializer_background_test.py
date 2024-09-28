from typing import Optional

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import Note

from note_size.cache.cache_initializer_background import CacheInitializerBackground
from note_size.cache.cache_manager import CacheManager
from note_size.cache.cache_storage import CacheStorage
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.config.config import Config
from note_size.types import FileType, SizeType
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper
from tests.conftest import cache_manager
from tests.data import Data

update_progress_history: list[str] = []


def update_progress_callback(label: str, value: Optional[int], max_value: Optional[int]):
    update_progress_history.append(f"{label} - {value} - {max_value}")


def test_initialize_caches(td: Data, col: Collection, cache_manager: CacheManager, media_cache: MediaCache,
                           item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                           file_type_helper: FileTypeHelper, config: Config, cache_storage: CacheStorage):
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()
    card_id1: CardId = col.card_ids_of_note(note1.id)[0]
    card_id2: CardId = col.card_ids_of_note(note2.id)[0]

    assert not media_cache.is_initialized()
    assert not item_id_cache.is_initialized()
    assert not size_calculator.is_initialized()
    assert not size_formatter.is_initialized()
    assert not file_type_helper.is_initialized()

    cache_initializer_background: CacheInitializerBackground = CacheInitializerBackground(
        cache_manager, update_progress_callback)
    count: int = cache_initializer_background.initialize_caches(col)
    assert count == 4
    assert update_progress_history == []

    assert media_cache.is_initialized()
    assert item_id_cache.is_initialized()
    assert size_calculator.is_initialized()
    assert size_formatter.is_initialized()
    assert file_type_helper.is_initialized()

    assert media_cache.as_dict_list() == [{'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5}]
    assert item_id_cache.as_dict_list() == [{card_id1: note1.id,
                                             card_id2: note2.id}]
    assert size_calculator.as_dict_list() == [{SizeType.TOTAL: {note1.id: 143, note2.id: 70},
                                               SizeType.TEXTS: {note1.id: 122, note2.id: 70},
                                               SizeType.FILES: {note1.id: 21, note2.id: 0}},
                                              {note1.id: {'picture.jpg', 'sound.mp3', 'animation.gif'},
                                               note2.id: set()},
                                              {note1.id: {'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5},
                                               note2.id: {}}]
    assert size_formatter.as_dict_list() == [{0: '0 B', 21: '21 B', 70: '70 B', 122: '122 B', 143: '143 B'}]
    assert file_type_helper.as_dict_list() == [{'animation.gif': FileType.IMAGE,
                                                'picture.jpg': FileType.IMAGE,
                                                'sound.mp3': FileType.AUDIO}]


def test_update_progress(td: Data, col: Collection, cache_manager: CacheManager, media_cache: MediaCache,
                         item_id_cache: ItemIdCache, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                         file_type_helper: FileTypeHelper, config: Config, cache_storage: CacheStorage):
    update_progress_step: int = 10
    note_count: int = update_progress_step * 2 + 1
    for i in range(note_count):
        td.create_note_without_files()
    cache_initializer_background: CacheInitializerBackground = CacheInitializerBackground(
        cache_manager, update_progress_callback, update_progress_step)
    count: int = cache_initializer_background.initialize_caches(col)
    assert count == 42
    assert update_progress_history == ['Caching note sizes: 10 of 21 - 10 - 21',
                                       'Caching note sizes: 20 of 21 - 20 - 21',
                                       'Caching card sizes: 10 of 21 - 10 - 21',
                                       'Caching card sizes: 20 of 21 - 20 - 21']
