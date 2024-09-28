import logging
import os.path
import pickle
import shutil
from pathlib import Path
from typing import Any

import pytest
from anki.cards import CardId
from anki.collection import Collection
from anki.notes import Note

from note_size.cache.cache_storage import CacheStorage
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.types import SizeType
from tests.data import Data


@pytest.fixture
def empty_cache_dict() -> list[dict[str, Any]]:
    return [{}, {}]


def test_write_read_cache_file(cache_storage: CacheStorage, td: Data, col: Collection, item_id_cache: ItemIdCache,
                               size_calculator: SizeCalculator, config: Config, settings: Settings,
                               empty_cache_dict: list[dict[str, Any]], media_cache: MediaCache):
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()

    card_id1: CardId = col.card_ids_of_note(note1.id)[0]
    card_id2: CardId = col.card_ids_of_note(note2.id)[0]
    item_id_cache.get_note_id_by_card_id(card_id1)
    item_id_cache.get_note_id_by_card_id(card_id2)
    size_calculator.get_note_size(note1.id, SizeType.TOTAL, use_cache=True)
    size_calculator.get_note_size(note2.id, SizeType.TOTAL, use_cache=True)

    size_calculator.get_note_files(note1.id, use_cache=True)
    size_calculator.get_note_files(note2.id, use_cache=True)

    cache_storage.save_caches_to_file([item_id_cache, size_calculator, media_cache])

    item_id_cache_2: ItemIdCache = ItemIdCache(col, size_calculator, media_cache)
    media_cache_2: MediaCache = MediaCache(col, config)
    size_calculator_2: SizeCalculator = SizeCalculator(col, media_cache_2)
    assert item_id_cache_2.as_dict_list() == empty_cache_dict
    read_success: bool = cache_storage.read_caches_from_file([item_id_cache_2, size_calculator_2, media_cache_2])
    assert read_success
    assert item_id_cache_2.as_dict_list() == [{card_id1: note1.id,
                                               card_id2: note2.id},
                                              {}]
    assert size_calculator_2.as_dict_list() == [{SizeType.TOTAL: {note1.id: 143, note2.id: 70},
                                                 SizeType.TEXTS: {note1.id: 122, note2.id: 70},
                                                 SizeType.FILES: {note1.id: 21, note2.id: 0}},
                                                {note1.id: {'picture.jpg', 'sound.mp3', 'animation.gif'},
                                                 note2.id: set()},
                                                {note1.id: {'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5},
                                                 note2.id: {}}]
    assert media_cache_2.as_dict_list() == [{'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5}]

    col.remove_notes([note1.id, note2.id])


def test_write_cache_file_error(cache_storage: CacheStorage, item_id_cache: ItemIdCache, settings: Settings, caplog):
    shutil.rmtree(settings.cache_file.parent)
    with caplog.at_level(logging.WARNING):
        cache_storage.save_caches_to_file([item_id_cache])
    assert not settings.cache_file.exists()
    assert "Cannot save cache file:" in caplog.text


def test_read_invalid_cache_file(cache_storage: CacheStorage, item_id_cache: ItemIdCache, settings: Settings,
                                 empty_cache_dict: list[dict[str, Any]], caplog):
    cache_file: Path = settings.cache_file
    cache_file.write_bytes(b'invalid cache content')
    assert os.path.exists(cache_file)
    assert item_id_cache.as_dict_list() == empty_cache_dict
    with caplog.at_level(logging.WARNING):
        read_success: bool = cache_storage.read_caches_from_file([item_id_cache])
    assert not read_success
    assert item_id_cache.as_dict_list() == empty_cache_dict
    assert "Cannot deserialize cache file:" in caplog.text
    assert not os.path.exists(cache_file)


def test_read_absent_cache_file(cache_storage: CacheStorage, item_id_cache: ItemIdCache, settings: Settings,
                                empty_cache_dict: list[dict[str, Any]], caplog):
    assert not settings.cache_file.exists()
    assert item_id_cache.as_dict_list() == empty_cache_dict
    with caplog.at_level(logging.INFO):
        read_success: bool = cache_storage.read_caches_from_file([item_id_cache])
    assert not read_success
    assert item_id_cache.as_dict_list() == empty_cache_dict
    assert "Skip reading absent cache file:" in caplog.text
    assert not settings.cache_file.exists()


def test_read_partially_invalid_cache_file(cache_storage: CacheStorage, td: Data, col: Collection,
                                           item_id_cache: ItemIdCache, size_calculator: SizeCalculator,
                                           config: Config, settings: Settings, empty_cache_dict: list[dict[str, Any]],
                                           media_cache: MediaCache, caplog):
    note1: Note = td.create_note_with_files()
    card_id1: CardId = col.card_ids_of_note(note1.id)[0]
    item_id_cache.get_note_id_by_card_id(card_id1)
    size_calculator.get_note_files(note1.id, use_cache=True)

    partially_invalid_cache: list[dict[str, Any]] = item_id_cache.as_dict_list()
    del partially_invalid_cache[0]

    cache_file: Path = settings.cache_file
    pickle.dump(partially_invalid_cache, cache_file.open("wb"))
    assert os.path.exists(cache_file)

    item_id_cache_2: ItemIdCache = ItemIdCache(col, size_calculator, media_cache)
    assert item_id_cache_2.as_dict_list() == empty_cache_dict
    with caplog.at_level(logging.WARNING):
        read_success: bool = cache_storage.read_caches_from_file([item_id_cache_2])
    assert not read_success
    assert "Cannot deserialize cache file:" in caplog.text
    assert item_id_cache_2.as_dict_list() == empty_cache_dict
    assert not os.path.exists(cache_file)
