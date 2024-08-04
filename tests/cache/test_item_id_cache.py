import logging
import timeit
from typing import Sequence, Any

import pytest
from anki.cards import CardId
from anki.collection import Collection
from anki.errors import NotFoundError
from anki.notes import NoteId, Note

from note_size.cache.item_id_cache import ItemIdCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.types import SizeBytes, SizeStr, SizeType, MediaFile
from tests.data import Data, DefaultFields


@pytest.fixture
def empty_cache_dict() -> list[dict[str, Any]]:
    return [{},
            {SizeType.TOTAL: {}, SizeType.TEXTS: {}, SizeType.FILES: {}},
            {SizeType.TOTAL: {}, SizeType.TEXTS: {}, SizeType.FILES: {}},
            {}]


def test_get_note_size_bytes(td: Data, item_id_cache: ItemIdCache):
    exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                      len(DefaultFields.back_field_content.encode()) +
                                      len(DefaultFields.content0) + len(DefaultFields.content1) +
                                      len(DefaultFields.content2))
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeBytes = item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == exp_size_1

    content: str = 'updated'
    Data.update_front_field(note, content)

    act_size_cached: SizeBytes = item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=True)
    assert act_size_cached == exp_size_1

    act_size_uncached: SizeBytes = item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_uncached == SizeBytes(len(content.encode()) +
                                          len(DefaultFields.back_field_content.encode()) +
                                          len(DefaultFields.content0) +
                                          len(DefaultFields.content2))


def test_get_note_size_bytes_performance(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True),
        number=1_000_000)
    assert execution_time <= 1


def test_get_note_size_str(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeStr = item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == "143 B"

    Data.update_front_field(note, 'updated')

    size_cached: SizeStr = item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True)
    assert size_cached == "143 B"

    size_uncached: SizeStr = item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
    assert size_uncached == "86 B"


def test_evict_note(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()

    size1: SizeBytes = item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True)
    assert size1 == 143

    content: str = 'updated'
    Data.update_front_field(note, content)
    size2: SizeBytes = item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True)
    assert size2 == size1

    item_id_cache.evict_note(note.id)
    size3: SizeBytes = item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True)
    assert size3 == 86


def test_refresh_note(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    assert item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True) == "143 B"

    Data.update_front_field(note, 'updated')
    assert item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True) == "143 B"

    item_id_cache.refresh_note(note_id)
    assert item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True) == "86 B"


def test_absent_note(item_id_cache: ItemIdCache):
    with pytest.raises(NotFoundError):
        item_id_cache.get_note_size_str(NoteId(123), SizeType.TOTAL, use_cache=True)


def test_get_note_id_by_card_id(td: Data, col: Collection, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    card_ids: Sequence[int] = col.card_ids_of_note(note.id)
    card_id: CardId = card_ids[0]
    assert item_id_cache.get_note_id_by_card_id(card_id) == note.id
    col.remove_notes([note.id])
    col.save()
    col.flush()
    assert item_id_cache.get_note_id_by_card_id(card_id) == note.id
    item_id_cache.evict_note(note.id)
    with pytest.raises(NotFoundError):
        item_id_cache.get_note_id_by_card_id(card_id)


def test_write_read_cache_from_file(td: Data, col: Collection, item_id_cache: ItemIdCache,
                                    size_calculator: SizeCalculator, config: Config, settings: Settings,
                                    empty_cache_dict: list[dict[str, Any]]):
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()

    card_id1: CardId = col.card_ids_of_note(note1.id)[0]
    card_id2: CardId = col.card_ids_of_note(note2.id)[0]
    item_id_cache.get_note_id_by_card_id(card_id1)
    item_id_cache.get_note_id_by_card_id(card_id2)

    note_size1: SizeStr = item_id_cache.get_note_size_str(note1.id, SizeType.TOTAL, use_cache=True)
    note_size2: SizeStr = item_id_cache.get_note_size_str(note2.id, SizeType.TOTAL, use_cache=True)

    files1: list[MediaFile] = item_id_cache.get_note_files(note1.id, use_cache=True)
    files2: list[MediaFile] = item_id_cache.get_note_files(note2.id, use_cache=True)

    item_id_cache.save_caches_to_file()

    item_id_cache_2: ItemIdCache = ItemIdCache(col, size_calculator, config, settings)
    assert item_id_cache_2.as_dict_list() == empty_cache_dict
    item_id_cache_2.read_caches_from_file()
    assert item_id_cache_2.as_dict_list() == [{card_id1: note1.id,
                                               card_id2: note2.id},
                                              {SizeType.TOTAL: {note1.id: 143, note2.id: 70},
                                               SizeType.TEXTS: {note1.id: 122, note2.id: 70},
                                               SizeType.FILES: {note1.id: 21, note2.id: 0}},
                                              {SizeType.TOTAL: {note1.id: "143 B", note2.id: "70 B"},
                                               SizeType.TEXTS: {},
                                               SizeType.FILES: {}},
                                              {note1.id: ['picture.jpg', 'sound.mp3', 'picture.jpg', 'animation.gif'],
                                               note2.id: []}]

    col.remove_notes([note1.id, note2.id])
    assert item_id_cache.get_note_size_str(note1.id, SizeType.TOTAL, use_cache=True) == note_size1
    assert item_id_cache.get_note_size_str(note2.id, SizeType.TOTAL, use_cache=True) == note_size2


def test_read_invalid_cache_file(item_id_cache: ItemIdCache, settings: Settings,
                                 empty_cache_dict: list[dict[str, Any]], caplog):
    settings.cache_file.write_bytes(b'invalid cache content')
    assert item_id_cache.as_dict_list() == empty_cache_dict
    with caplog.at_level(logging.WARNING):
        item_id_cache.read_caches_from_file()
    assert item_id_cache.as_dict_list() == empty_cache_dict
    assert "Cannot deserialize cache file:" in caplog.text


def test_absent_cache_file(item_id_cache: ItemIdCache, settings: Settings,
                           empty_cache_dict: list[dict[str, Any]], caplog):
    assert not settings.cache_file.exists()
    assert item_id_cache.as_dict_list() == empty_cache_dict
    with caplog.at_level(logging.INFO):
        item_id_cache.read_caches_from_file()
    assert item_id_cache.as_dict_list() == empty_cache_dict
    assert "Skip reading absent cache file:" in caplog.text


def test_get_note_files(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: list[MediaFile] = item_id_cache.get_note_files(note_id, use_cache=True)
    assert files == ['picture.jpg', 'sound.mp3', 'picture.jpg', 'animation.gif']

    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: list[MediaFile] = item_id_cache.get_note_files(note_id, use_cache=True)
    assert files_cached == ['picture.jpg', 'sound.mp3', 'picture.jpg', 'animation.gif']
    files_uncached: list[MediaFile] = item_id_cache.get_note_files(note_id, use_cache=False)
    assert files_uncached == ['sound.mp3', 'picture.jpg', 'animation.gif']


def test_get_used_files_size(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: list[MediaFile] = item_id_cache.get_note_files(note_id, use_cache=True)
    assert files == ['picture.jpg', 'sound.mp3', 'picture.jpg', 'animation.gif']
    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: list[MediaFile] = item_id_cache.get_note_files(note_id, use_cache=True)
    assert files_cached == ['picture.jpg', 'sound.mp3', 'picture.jpg', 'animation.gif']

    files_uncached: list[MediaFile] = item_id_cache.get_note_files(note_id, use_cache=False)
    assert files_uncached == ['sound.mp3', 'picture.jpg', 'animation.gif']
