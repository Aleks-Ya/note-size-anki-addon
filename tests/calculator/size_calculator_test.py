import timeit
from typing import Sequence

import pytest
from anki.collection import Collection
from anki.errors import NotFoundError
from anki.notes import Note, NoteId
from pytest import raises

from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, MediaFile, SizeType
from tests.data import Data, DefaultFields, FileNames, MediaFiles, FileContents


@pytest.fixture
def note(td: Data) -> Note:
    return td.create_note_with_files()


def test_calculate_note_size_text(size_calculator: SizeCalculator, note: Note):
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TEXTS, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                    len(DefaultFields.back_field_content.encode()))
    assert act_size == exp_size


def test_calculate_note_size_text_unicode(size_calculator: SizeCalculator, td: Data):
    note: Note = td.create_note_without_files()
    note[DefaultFields.front_field_name] = '∑￡'
    note[DefaultFields.back_field_name] = '∆∏∦'
    size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TEXTS, use_cache=False)
    assert size == SizeBytes(15)


@pytest.mark.performance
def test_calculate_note_size_text_performance(size_calculator: SizeCalculator, note: Note):
    execution_time: float = timeit.timeit(
        lambda: size_calculator.calculate_note_size(note, SizeType.TEXTS, use_cache=True), number=250_000)
    assert execution_time <= 1


def test_calculate_note_size_files(size_calculator: SizeCalculator, note: Note):
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.FILES, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(FileContents.picture) +
                                    len(FileContents.sound) +
                                    len(FileContents.animation))
    assert act_size == exp_size


def test_calculate_note_size_total(size_calculator: SizeCalculator, note: Note):
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                    len(DefaultFields.back_field_content.encode()) +
                                    len(FileContents.picture) +
                                    len(FileContents.sound) +
                                    len(FileContents.animation))
    assert act_size == exp_size


def test_calculate_note_size_total_missing_file(size_calculator: SizeCalculator, note: Note):
    content: str = 'Missing file: <img src="absents.png"> ￡'
    note[DefaultFields.front_field_name] = content
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(content.encode()) +
                                    len(DefaultFields.back_field_content.encode()) +
                                    len(FileContents.picture) +
                                    len(FileContents.animation))
    assert act_size == exp_size


@pytest.mark.performance
def test_calculate_note_size_total_performance(size_calculator: SizeCalculator, note: Note):
    execution_time: float = timeit.timeit(
        lambda: size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=True), number=250_000)
    assert execution_time <= 1


def test_calculate_note_file_sizes(size_calculator: SizeCalculator, note: Note):
    act_file_sizes: dict[MediaFile, SizeBytes] = size_calculator.calculate_note_file_sizes(note, use_cache=False)
    exp_file_sizes: dict[MediaFile, SizeBytes] = {
        MediaFiles.picture: SizeBytes(len(FileContents.picture)),
        MediaFiles.sound: SizeBytes(len(FileContents.sound)),
        MediaFiles.animation: SizeBytes(len(FileContents.animation))}
    assert act_file_sizes == exp_file_sizes


@pytest.mark.performance
def test_calculate_note_file_sizes_performance(size_calculator: SizeCalculator, note: Note):
    execution_time: float = timeit.timeit(lambda: size_calculator.calculate_note_file_sizes(note, use_cache=True),
                                          number=250_000)
    assert execution_time <= 1


def test_calculate_size_of_files(size_calculator: SizeCalculator, col: Collection):
    content1: bytes = b"first"
    content2: bytes = b"second"
    file1: MediaFile = MediaFile(col.media.write_data("file1.txt", content1))
    file2: MediaFile = MediaFile(col.media.write_data("file2.txt", content2))
    file2_duplicate: MediaFile = file2
    files: set[MediaFile] = {file1, file2, file2_duplicate}

    size: SizeBytes = size_calculator.calculate_size_of_files(files, use_cache=True)
    exp_size: SizeBytes = SizeBytes(len(content1) + len(content2))
    assert size == exp_size

    col.media.trash_files([file2])
    size_cached: SizeBytes = size_calculator.calculate_size_of_files(files, use_cache=True)
    assert size_cached == exp_size

    size_uncached: SizeBytes = size_calculator.calculate_size_of_files(files, use_cache=False)
    assert size_uncached == SizeBytes(len(content1))


@pytest.mark.performance
def test_calculate_note_files_performance(size_calculator: SizeCalculator, td: Data):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(lambda: size_calculator.calculate_note_files(note, True), number=100_000)
    assert execution_time <= 0.5


def test_get_cache_size(size_calculator: SizeCalculator, td: Data):
    assert size_calculator.get_cache_size() == 0
    note1: Note = td.create_note_with_files()
    size_calculator.get_note_size(note1.id, SizeType.TOTAL, use_cache=True)
    assert size_calculator.get_cache_size() == 5
    size_calculator.get_note_size(note1.id, SizeType.TOTAL, use_cache=True)
    assert size_calculator.get_cache_size() == 5
    note2: Note = td.create_note_without_files()
    size_calculator.get_note_size(note2.id, SizeType.TEXTS, use_cache=True)
    assert size_calculator.get_cache_size() == 6
    size_calculator.evict_note(note1.id)
    assert size_calculator.get_cache_size() == 1
    size_calculator.invalidate_cache()
    assert size_calculator.get_cache_size() == 0


def test_evict_note(size_calculator: SizeCalculator, td: Data):
    assert size_calculator.get_cache_size() == 0
    assert size_calculator.as_dict_list() == [{SizeType.TOTAL: {},
                                               SizeType.TEXTS: {},
                                               SizeType.FILES: {}},
                                              {},
                                              {}]
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()
    nid1: NoteId = note1.id
    nid2: NoteId = note2.id
    size_calculator.get_note_size(nid1, SizeType.TOTAL, use_cache=True)
    size_calculator.get_note_size(nid1, SizeType.TOTAL, use_cache=True)
    size_calculator.get_note_size(nid2, SizeType.TEXTS, use_cache=True)
    assert size_calculator.get_cache_size() == 6
    assert size_calculator.as_dict_list() == [{SizeType.TOTAL: {nid1: 143},
                                               SizeType.TEXTS: {nid1: 122, nid2: 70},
                                               SizeType.FILES: {nid1: 21}},
                                              {nid1: {FileNames.animation, FileNames.sound, FileNames.picture}},
                                              {nid1: {FileNames.animation: 9, FileNames.picture: 7,
                                                      FileNames.sound: 5}}]
    size_calculator.evict_note(nid1)
    assert size_calculator.get_cache_size() == 1
    assert size_calculator.as_dict_list() == [{SizeType.TOTAL: {},
                                               SizeType.TEXTS: {nid2: 70},
                                               SizeType.FILES: {}},
                                              {},
                                              {}]


def test_get_note_size(size_calculator: SizeCalculator, td: Data):
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
def test_get_note_size_performance(size_calculator: SizeCalculator, td: Data):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True),
        number=250_000)
    assert execution_time <= 1


def test_get_note_files(size_calculator: SizeCalculator, td: Data):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    files: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files == {FileNames.animation, FileNames.sound, FileNames.picture}

    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    files_cached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=True)
    assert files_cached == {FileNames.animation, FileNames.sound, FileNames.picture}
    files_uncached: set[MediaFile] = size_calculator.get_note_files(note_id, use_cache=False)
    assert files_uncached == {FileNames.sound, FileNames.picture, FileNames.animation}


def test_get_note_files_absent(size_calculator: SizeCalculator, td: Data):
    with raises(NotFoundError):
        note_id: NoteId = NoteId(-1)
        size_calculator.get_note_files(note_id, use_cache=True)


def test_get_notes_file_sizes(size_calculator: SizeCalculator, td: Data):
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()
    note_ids: Sequence[NoteId] = [note1.id, note2.id]
    file_sizes: dict[MediaFile, SizeBytes] = size_calculator.get_notes_file_sizes(note_ids, use_cache=True)
    assert file_sizes == {FileNames.animation: 9, FileNames.picture: 7, FileNames.sound: 5}
