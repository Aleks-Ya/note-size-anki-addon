import timeit

import pytest
from anki.errors import NotFoundError
from anki.notes import NoteId, Note

from note_size.cache.size_str_cache import SizeStrCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, SizeStr, SizeType, MediaFile
from tests.conftest import size_calculator
from tests.data import Data, DefaultFields


def test_get_note_size_bytes(td: Data, size_str_cache: SizeStrCache, size_calculator: SizeCalculator):
    exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                      len(DefaultFields.back_field_content.encode()) +
                                      len(DefaultFields.content0) + len(DefaultFields.content1) +
                                      len(DefaultFields.content2))
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
                                          len(DefaultFields.content0) +
                                          len(DefaultFields.content2))


@pytest.mark.performance
def test_get_note_size_bytes_performance(td: Data, size_str_cache: SizeStrCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True),
        number=500_000)
    assert execution_time <= 1


def test_get_note_size_str(td: Data, size_str_cache: SizeStrCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeStr = size_str_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == "143 B"

    Data.update_front_field(note, 'updated')

    size_cached: SizeStr = size_str_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True)
    assert size_cached == "143 B"

    size_uncached: SizeStr = size_str_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
    assert size_uncached == "86 B"


def test_evict_note(td: Data, size_str_cache: SizeStrCache):
    assert size_str_cache.get_cache_size() == 0
    assert size_str_cache.as_dict_list() == [{SizeType.TOTAL: {},
                                              SizeType.TEXTS: {},
                                              SizeType.FILES: {}}]
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()
    for size_type in SizeType:
        size_str_cache.get_note_size_str(note1.id, size_type, use_cache=True)
        size_str_cache.get_note_size_str(note2.id, size_type, use_cache=True)
    assert size_str_cache.get_cache_size() == 6
    assert size_str_cache.as_dict_list() == [{SizeType.TOTAL: {note1.id: '143 B', note2.id: '70 B'},
                                              SizeType.TEXTS: {note1.id: '122 B', note2.id: '70 B'},
                                              SizeType.FILES: {note1.id: '21 B', note2.id: '0 B'}}]
    size_str_cache.evict_note(note1.id)
    assert size_str_cache.get_cache_size() == 3
    assert size_str_cache.as_dict_list() == [{SizeType.TOTAL: {note2.id: '70 B'},
                                              SizeType.TEXTS: {note2.id: '70 B'},
                                              SizeType.FILES: {note2.id: '0 B'}}]


def test_absent_note(size_str_cache: SizeStrCache):
    with pytest.raises(NotFoundError):
        size_str_cache.get_note_size_str(NoteId(123), SizeType.TOTAL, use_cache=True)


def test_get_note_files(td: Data, size_str_cache: SizeStrCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {'animation.gif', 'sound.mp3', 'picture.jpg'}

    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {'animation.gif', 'sound.mp3', 'picture.jpg'}
    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {'sound.mp3', 'picture.jpg', 'animation.gif'}


def test_get_used_files_size(td: Data, size_str_cache: SizeStrCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {'animation.gif', 'sound.mp3', 'picture.jpg'}
    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {'animation.gif', 'picture.jpg', 'sound.mp3'}

    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {'sound.mp3', 'picture.jpg', 'animation.gif'}


def test_initialized(size_str_cache: SizeStrCache):
    assert not size_str_cache.is_initialized()
    size_str_cache.set_initialized(True)
    assert size_str_cache.is_initialized()
    size_str_cache.set_initialized(False)
    assert not size_str_cache.is_initialized()


def test_get_cache_size(td: Data, size_str_cache: SizeStrCache):
    assert size_str_cache.get_cache_size() == 0
    note1: Note = td.create_note_with_files()
    size_str_cache.get_note_size_str(note1.id, SizeType.TOTAL, use_cache=True)
    assert size_str_cache.get_cache_size() == 1
    note2: Note = td.create_note_without_files()
    size_str_cache.get_note_size_str(note2.id, SizeType.TEXTS, use_cache=True)
    assert size_str_cache.get_cache_size() == 2
    size_str_cache.evict_note(note1.id)
    assert size_str_cache.get_cache_size() == 1
    size_str_cache.invalidate_cache()
    assert size_str_cache.get_cache_size() == 0
