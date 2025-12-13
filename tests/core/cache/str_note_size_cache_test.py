import timeit

import pytest
from anki.errors import NotFoundError
from anki.notes import NoteId, Note

from note_size.core.cache.str_note_size_cache import StrNoteSizeCache
from note_size.core.cache.bytes_note_size_cache import BytesNoteSizeCache
from note_size.core.common.types import SizeBytes, SizeStr, SizeType, MediaFile
from tests.conftest import bytes_note_size_cache
from tests.data import Data, DefaultFields, MediaFiles, FileContents, Digits


def test_get_note_size_bytes(td: Data, str_note_size_cache: StrNoteSizeCache, bytes_note_size_cache: BytesNoteSizeCache):
    exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                      len(DefaultFields.back_field_content.encode()) +
                                      len(FileContents.picture) + len(FileContents.sound) +
                                      len(FileContents.animation))
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeBytes = bytes_note_size_cache.get_note_size(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == exp_size_1

    content: str = 'updated'
    Data.update_front_field(note, content)

    act_size_cached: SizeBytes = bytes_note_size_cache.get_note_size(note_id, SizeType.TOTAL, use_cache=True)
    assert act_size_cached == exp_size_1

    act_size_uncached: SizeBytes = bytes_note_size_cache.get_note_size(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_uncached == SizeBytes(len(content.encode()) +
                                          len(DefaultFields.back_field_content.encode()) +
                                          len(FileContents.picture) +
                                          len(FileContents.animation))


@pytest.mark.performance
def test_get_note_size_bytes_performance(td: Data, str_note_size_cache: StrNoteSizeCache, bytes_note_size_cache: BytesNoteSizeCache):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: bytes_note_size_cache.get_note_size(note.id, SizeType.TOTAL, use_cache=True),
        number=200_000)
    assert execution_time <= 1


def test_get_note_size_str(td: Data, str_note_size_cache: StrNoteSizeCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeStr = str_note_size_cache.get_note_size_str(note_id, SizeType.TOTAL, Digits.one, use_cache=False)
    assert act_size_1 == "143 B"

    Data.update_front_field(note, 'updated')

    size_cached: SizeStr = str_note_size_cache.get_note_size_str(note_id, SizeType.TOTAL, Digits.one, use_cache=True)
    assert size_cached == "143 B"

    size_uncached: SizeStr = str_note_size_cache.get_note_size_str(note_id, SizeType.TOTAL, Digits.one, use_cache=False)
    assert size_uncached == "86 B"


def test_evict_note(td: Data, str_note_size_cache: StrNoteSizeCache):
    assert str_note_size_cache.get_cache_size() == 0
    assert str_note_size_cache.as_dict_list() == [{SizeType.TOTAL: {},
                                              SizeType.TEXTS: {},
                                              SizeType.FILES: {}}]
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()
    for size_type in SizeType:
        str_note_size_cache.get_note_size_str(note1.id, size_type, Digits.one, use_cache=True)
        str_note_size_cache.get_note_size_str(note2.id, size_type, Digits.one, use_cache=True)
    assert str_note_size_cache.get_cache_size() == 6
    assert str_note_size_cache.as_dict_list() == [{SizeType.TOTAL: {note1.id: {Digits.one: '143 B'},
                                                               note2.id: {Digits.one: '70 B'}},
                                              SizeType.TEXTS: {note1.id: {Digits.one: '122 B'},
                                                               note2.id: {Digits.one: '70 B'}},
                                              SizeType.FILES: {note1.id: {Digits.one: '21 B'},
                                                               note2.id: {Digits.one: '0 B'}}}]
    str_note_size_cache.evict_note(note1.id)
    assert str_note_size_cache.get_cache_size() == 3
    assert str_note_size_cache.as_dict_list() == [{SizeType.TOTAL: {note2.id: {Digits.one: '70 B'}},
                                              SizeType.TEXTS: {note2.id: {Digits.one: '70 B'}},
                                              SizeType.FILES: {note2.id: {Digits.one: '0 B'}}}]


def test_absent_note(str_note_size_cache: StrNoteSizeCache):
    with pytest.raises(NotFoundError):
        str_note_size_cache.get_note_size_str(NoteId(123), SizeType.TOTAL, Digits.one, use_cache=True)


def test_get_note_files(td: Data, str_note_size_cache: StrNoteSizeCache, bytes_note_size_cache: BytesNoteSizeCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = bytes_note_size_cache.get_note_files(note_id, use_cache=True)
    assert files == {MediaFiles.animation, MediaFiles.sound, MediaFiles.picture}

    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = bytes_note_size_cache.get_note_files(note_id, use_cache=True)
    assert files_cached == {MediaFiles.animation, MediaFiles.sound, MediaFiles.picture}
    files_uncached: set[MediaFile] = bytes_note_size_cache.get_note_files(note_id, use_cache=False)
    assert files_uncached == {MediaFiles.sound, MediaFiles.picture, MediaFiles.animation}


def test_get_used_files_size(td: Data, str_note_size_cache: StrNoteSizeCache, bytes_note_size_cache: BytesNoteSizeCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = bytes_note_size_cache.get_note_files(note_id, use_cache=True)
    assert files == {MediaFiles.animation, MediaFiles.sound, MediaFiles.picture}
    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = bytes_note_size_cache.get_note_files(note_id, use_cache=True)
    assert files_cached == {MediaFiles.animation, MediaFiles.picture, MediaFiles.sound}

    files_uncached: set[MediaFile] = bytes_note_size_cache.get_note_files(note_id, use_cache=False)
    assert files_uncached == {MediaFiles.sound, MediaFiles.picture, MediaFiles.animation}


def test_initialized(str_note_size_cache: StrNoteSizeCache):
    assert not str_note_size_cache.is_initialized()
    str_note_size_cache.set_initialized(True)
    assert str_note_size_cache.is_initialized()
    str_note_size_cache.set_initialized(False)
    assert not str_note_size_cache.is_initialized()


def test_get_cache_size(td: Data, str_note_size_cache: StrNoteSizeCache):
    assert str_note_size_cache.get_cache_size() == 0
    note1: Note = td.create_note_with_files()
    str_note_size_cache.get_note_size_str(note1.id, SizeType.TOTAL, Digits.one, use_cache=True)
    assert str_note_size_cache.get_cache_size() == 1
    note2: Note = td.create_note_without_files()
    str_note_size_cache.get_note_size_str(note2.id, SizeType.TEXTS, Digits.one, use_cache=True)
    assert str_note_size_cache.get_cache_size() == 2
    str_note_size_cache.evict_note(note1.id)
    assert str_note_size_cache.get_cache_size() == 1
    str_note_size_cache.invalidate_cache()
    assert str_note_size_cache.get_cache_size() == 0
