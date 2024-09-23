import timeit
from typing import Sequence

import pytest
from anki.cards import CardId
from anki.collection import Collection
from anki.errors import NotFoundError
from anki.notes import NoteId, Note

from note_size.cache.item_id_cache import ItemIdCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, SizeStr, SizeType, MediaFile
from tests.conftest import size_calculator
from tests.data import Data, DefaultFields


def test_get_note_size_bytes(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
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


def test_get_note_size_bytes_performance(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True),
        number=500_000)
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


def test_evict_note(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()

    size1: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size1 == 143

    content: str = 'updated'
    Data.update_front_field(note, content)
    size2: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size2 == size1

    item_id_cache.evict_note(note.id)
    size3: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
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


def test_get_note_files(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {'animation.gif', 'sound.mp3', 'picture.jpg'}

    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {'animation.gif', 'sound.mp3', 'picture.jpg'}
    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {'sound.mp3', 'picture.jpg', 'animation.gif'}


def test_get_used_files_size(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {'animation.gif', 'sound.mp3', 'picture.jpg'}
    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {'animation.gif', 'picture.jpg', 'sound.mp3'}

    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {'sound.mp3', 'picture.jpg', 'animation.gif'}


def test_refresh_notes_having_updated_files(td: Data, item_id_cache: ItemIdCache, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    item_id_cache.refresh_note(note.id)
    size1: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    td.write_file(DefaultFields.file0, "new file content")
    size2: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size2 == size1

    assert not item_id_cache.is_initialized()
    item_id_cache.refresh_notes_having_updated_files()
    size3: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size3 == size1

    item_id_cache.set_initialized(True)
    item_id_cache.refresh_notes_having_updated_files()
    size4: SizeBytes = size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)
    assert size4 != size1


def test_initialized(item_id_cache: ItemIdCache):
    assert not item_id_cache.is_initialized()
    item_id_cache.set_initialized(True)
    assert item_id_cache.is_initialized()
    item_id_cache.set_initialized(False)
    assert not item_id_cache.is_initialized()
