import timeit

import pytest
from anki.collection import Collection
from anki.notes import NoteId, Note

from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, SizeType, MediaFile
from tests.conftest import size_calculator
from tests.data import Data, DefaultFields


def test_get_note_size_bytes(td: Data, file_note_id_cache: UpdatedFilesCalculator, size_calculator: SizeCalculator):
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
def test_get_note_size_bytes_performance(td: Data, file_note_id_cache: UpdatedFilesCalculator,
                                         size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True),
        number=500_000)
    assert execution_time <= 1


@pytest.mark.skip("TODO fix it")
def test_evict_note(td: Data, file_note_id_cache: UpdatedFilesCalculator, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()

    size1: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size1 == 143

    content: str = 'updated'
    Data.update_front_field(note, content)
    size2: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size2 == size1

    file_note_id_cache.evict_note(note.id)
    size3: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size3 == 86


def test_get_note_files(td: Data, file_note_id_cache: UpdatedFilesCalculator, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {'animation.gif', 'sound.mp3', 'picture.jpg'}

    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {'animation.gif', 'sound.mp3', 'picture.jpg'}
    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {'sound.mp3', 'picture.jpg', 'animation.gif'}


def test_initialized(file_note_id_cache: UpdatedFilesCalculator):
    assert not file_note_id_cache.is_initialized()
    file_note_id_cache.set_initialized(True)
    assert file_note_id_cache.is_initialized()
    file_note_id_cache.set_initialized(False)
    assert not file_note_id_cache.is_initialized()


@pytest.mark.skip("TODO fix it")
def test_get_cache_size(col: Collection, td: Data, file_note_id_cache: UpdatedFilesCalculator):
    assert file_note_id_cache.get_cache_size() == 0
    note1: Note = td.create_note_with_files()
    file_note_id_cache.get_used_files_size(use_cache=True)
    assert file_note_id_cache.get_cache_size() == 1
    file_note_id_cache.get_used_files_size(use_cache=True)
    assert file_note_id_cache.get_cache_size() == 2
    file_note_id_cache.evict_note(note1.id)
    assert file_note_id_cache.get_cache_size() == 1
    file_note_id_cache.invalidate_cache()
    assert file_note_id_cache.get_cache_size() == 0
