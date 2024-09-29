import pytest
from anki.collection import Collection
from anki.notes import Note

from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, SizeType
from tests.conftest import size_calculator
from tests.data import Data


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
