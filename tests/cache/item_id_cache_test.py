import timeit

import pytest
from anki.cards import Card
from anki.collection import Collection
from anki.errors import NotFoundError
from anki.notes import NoteId, Note

from note_size.cache.item_id_cache import ItemIdCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.common.types import SizeBytes, SizeType, MediaFile
from tests import wait_until, wait_until_exception
from tests.conftest import size_calculator
from tests.data import Data, DefaultFields, MediaFiles, FileContents


def test_get_note_size_bytes(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                      len(DefaultFields.back_field_content.encode()) +
                                      len(FileContents.picture) + len(FileContents.sound) +
                                      len(FileContents.animation))
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeBytes = size_calculator.get_note_size(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == exp_size_1

    content: str = 'updated'
    Data.update_front_field(note, content)

    act_size_cached: SizeBytes = size_calculator.get_note_size(note_id, SizeType.TOTAL, use_cache=True)
    assert act_size_cached == exp_size_1

    act_size_uncached: SizeBytes = size_calculator.get_note_size(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_uncached == SizeBytes(len(content.encode()) +
                                          len(DefaultFields.back_field_content.encode()) +
                                          len(FileContents.picture) +
                                          len(FileContents.animation))


@pytest.mark.performance
def test_get_note_size_bytes_performance(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True),
        number=250_000)
    assert execution_time <= 1


def test_evict_note(col: Collection, td: Data, item_id_cache: ItemIdCache):
    assert item_id_cache.get_cache_size() == 0
    assert item_id_cache.as_dict_list() == [{}]

    card1: Card = td.create_card_with_files()
    item_id_cache.get_note_id_by_card_id(card1.id)

    card2: Card = td.create_card_with_files()
    item_id_cache.get_note_id_by_card_id(card2.id)
    assert item_id_cache.get_cache_size() == 2
    assert item_id_cache.as_dict_list() == [{card1.id: card1.nid, card2.id: card2.nid}]

    item_id_cache.evict_note(card1.nid)
    wait_until(lambda: item_id_cache.get_cache_size() == 1)
    wait_until(lambda: item_id_cache.as_dict_list() == [{card2.id: card2.nid}])


def test_get_note_id_by_card_id(td: Data, col: Collection, item_id_cache: ItemIdCache):
    card: Card = td.create_card_with_files()
    assert item_id_cache.get_note_id_by_card_id(card.id) == card.nid
    col.remove_notes([card.nid])
    col.flush()
    assert item_id_cache.get_note_id_by_card_id(card.id) == card.nid
    item_id_cache.evict_note(card.nid)
    col.flush()
    wait_until_exception(lambda: item_id_cache.get_note_id_by_card_id(card.id), NotFoundError)


def test_get_note_files(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {MediaFiles.animation, MediaFiles.sound, MediaFiles.picture}

    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {MediaFiles.animation, MediaFiles.sound, MediaFiles.picture}
    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {MediaFiles.sound, MediaFiles.picture, MediaFiles.animation}


def test_get_used_files_size(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {MediaFiles.animation, MediaFiles.sound, MediaFiles.picture}
    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {MediaFiles.animation, MediaFiles.picture, MediaFiles.sound}

    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {MediaFiles.sound, MediaFiles.picture, MediaFiles.animation}


def test_initialized(item_id_cache: ItemIdCache):
    assert not item_id_cache.is_initialized()
    item_id_cache.set_initialized(True)
    assert item_id_cache.is_initialized()
    item_id_cache.set_initialized(False)
    assert not item_id_cache.is_initialized()


def test_get_cache_size(col: Collection, td: Data, item_id_cache: ItemIdCache):
    assert item_id_cache.get_cache_size() == 0
    card1: Card = td.create_card_with_files()
    item_id_cache.get_note_id_by_card_id(card1.id)
    assert item_id_cache.get_cache_size() == 1
    card2: Card = td.create_card_with_files()
    item_id_cache.get_note_id_by_card_id(card2.id)
    assert item_id_cache.get_cache_size() == 2
    item_id_cache.evict_note(card1.nid)
    wait_until(lambda: item_id_cache.get_cache_size() == 1)
    item_id_cache.invalidate_cache()
    assert item_id_cache.get_cache_size() == 0
