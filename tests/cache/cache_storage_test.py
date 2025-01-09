import logging
import os.path
import pickle
import shutil
from pathlib import Path
from typing import Any

from anki.cards import Card
from anki.collection import Collection

from note_size.cache.cache_storage import CacheStorage
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.cache.size_str_cache import SizeStrCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.types import SizeType, FileType
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper
from tests.data import Data, FileNames, MediaFiles


def test_write_read_cache_file(cache_storage: CacheStorage, td: Data, col: Collection, item_id_cache: ItemIdCache,
                               size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                               file_type_helper: FileTypeHelper, size_str_cache: SizeStrCache,
                               updated_files_calculator: UpdatedFilesCalculator, config: Config, settings: Settings,
                               media_cache: MediaCache):
    card1: Card = td.create_card_with_files()
    card2: Card = td.create_card_without_files()
    item_id_cache.get_note_id_by_card_id(card1.id)
    item_id_cache.get_note_id_by_card_id(card2.id)
    size_calculator.get_note_size(card1.nid, SizeType.TOTAL, use_cache=True)
    size_calculator.get_note_size(card2.nid, SizeType.TOTAL, use_cache=True)

    size_calculator.get_note_files(card1.nid, use_cache=True)
    size_calculator.get_note_files(card2.nid, use_cache=True)

    file_type_helper.get_file_type(MediaFiles.image, use_cache=True)

    size_str_cache.get_note_size_str(card1.nid, SizeType.TOTAL, use_cache=True)
    size_str_cache.get_note_size_str(card2.nid, SizeType.TEXTS, use_cache=True)
    size_str_cache.get_note_size_str(card2.nid, SizeType.FILES, use_cache=True)

    cache_storage.save_caches_to_file(
        [media_cache, item_id_cache, size_calculator, size_formatter, file_type_helper, size_str_cache,
         updated_files_calculator])

    media_cache_2: MediaCache = MediaCache(col, config)
    item_id_cache_2: ItemIdCache = ItemIdCache(col)
    size_calculator_2: SizeCalculator = SizeCalculator(col, media_cache_2)
    size_formatter_2: SizeFormatter = SizeFormatter()
    file_type_helper_2: FileTypeHelper = FileTypeHelper()
    size_str_cache_2: SizeStrCache = SizeStrCache(col, size_calculator_2, size_formatter_2)
    updated_files_calculator_2: UpdatedFilesCalculator = UpdatedFilesCalculator(col, size_calculator_2, media_cache_2)
    assert item_id_cache_2.as_dict_list() == [{}]
    read_success: bool = cache_storage.read_caches_from_file(
        [media_cache_2, item_id_cache_2, size_calculator_2, size_formatter_2, file_type_helper_2, size_str_cache_2,
         updated_files_calculator_2])
    assert read_success
    assert media_cache_2.as_dict_list() == [{FileNames.animation: 9, FileNames.picture: 7, FileNames.sound: 5}]
    assert item_id_cache_2.as_dict_list() == [{card1.id: card1.nid,
                                               card2.id: card2.nid}]
    assert size_calculator_2.as_dict_list() == [{SizeType.TOTAL: {card1.nid: 143, card2.nid: 70},
                                                 SizeType.TEXTS: {card1.nid: 122, card2.nid: 70},
                                                 SizeType.FILES: {card1.nid: 21, card2.nid: 0}},
                                                {card1.nid: {FileNames.picture, FileNames.sound, FileNames.animation},
                                                 card2.nid: set()},
                                                {card1.nid: {FileNames.animation: 9, FileNames.picture: 7,
                                                             FileNames.sound: 5},
                                                 card2.nid: {}}]
    assert size_formatter_2.as_dict_list() == [{0: '0 B', 70: '70 B', 143: '143 B'}]
    assert file_type_helper_2.as_dict_list() == [{FileNames.image: FileType.IMAGE}]
    assert size_str_cache_2.as_dict_list() == [{SizeType.TOTAL: {card1.nid: '143 B'},
                                                SizeType.TEXTS: {card2.nid: '70 B'},
                                                SizeType.FILES: {card2.nid: '0 B'}}]

    col.remove_notes([card1.nid, card2.nid])


def test_write_cache_file_error(cache_storage: CacheStorage, item_id_cache: ItemIdCache, settings: Settings, caplog):
    shutil.rmtree(settings.cache_file.parent)
    with caplog.at_level(logging.WARNING):
        cache_storage.save_caches_to_file([item_id_cache])
    assert not settings.cache_file.exists()
    assert "Cannot save cache file:" in caplog.text


def test_read_invalid_cache_file(cache_storage: CacheStorage, item_id_cache: ItemIdCache, settings: Settings, caplog):
    cache_file: Path = settings.cache_file
    cache_file.write_bytes(b'invalid cache content')
    assert os.path.exists(cache_file)
    assert item_id_cache.as_dict_list() == [{}]
    with caplog.at_level(logging.WARNING):
        read_success: bool = cache_storage.read_caches_from_file([item_id_cache])
    assert not read_success
    assert item_id_cache.as_dict_list() == [{}]
    assert "Cannot deserialize cache file:" in caplog.text
    assert not os.path.exists(cache_file)


def test_read_absent_cache_file(cache_storage: CacheStorage, item_id_cache: ItemIdCache, settings: Settings, caplog):
    assert not settings.cache_file.exists()
    assert item_id_cache.as_dict_list() == [{}]
    with caplog.at_level(logging.INFO):
        read_success: bool = cache_storage.read_caches_from_file([item_id_cache])
    assert not read_success
    assert item_id_cache.as_dict_list() == [{}]
    assert "Skip reading absent cache file:" in caplog.text
    assert not settings.cache_file.exists()


def test_read_partially_invalid_cache_file(cache_storage: CacheStorage, td: Data, col: Collection,
                                           item_id_cache: ItemIdCache, size_calculator: SizeCalculator,
                                           config: Config, settings: Settings, media_cache: MediaCache, caplog):
    card1: Card = td.create_card_with_files()
    item_id_cache.get_note_id_by_card_id(card1.id)
    size_calculator.get_note_files(card1.nid, use_cache=True)

    partially_invalid_cache: list[dict[str, Any]] = item_id_cache.as_dict_list()
    del partially_invalid_cache[0]

    cache_file: Path = settings.cache_file
    # noinspection PyTypeChecker
    pickle.dump(partially_invalid_cache, cache_file.open("wb"))
    assert os.path.exists(cache_file)

    item_id_cache_2: ItemIdCache = ItemIdCache(col)
    assert item_id_cache_2.as_dict_list() == [{}]
    with caplog.at_level(logging.WARNING):
        read_success: bool = cache_storage.read_caches_from_file([item_id_cache_2])
    assert not read_success
    assert "Cannot deserialize cache file:" in caplog.text
    assert item_id_cache_2.as_dict_list() == [{}]
    assert not os.path.exists(cache_file)
