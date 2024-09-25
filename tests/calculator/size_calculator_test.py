import timeit

import pytest
from anki.collection import Collection
from anki.notes import Note

from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, MediaFile, SizeType
from tests.data import Data, DefaultFields


@pytest.fixture
def note(td: Data) -> Note:
    return td.create_note_with_files()


def test_calculate_note_texts_size(note: Note, size_calculator: SizeCalculator):
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TEXTS, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                    len(DefaultFields.back_field_content.encode()))
    assert act_size == exp_size


def test_calculate_note_texts_size_unicode(td: Data, size_calculator: SizeCalculator):
    note: Note = td.create_note_without_files()
    note[DefaultFields.front_field_name] = '∑￡'
    note[DefaultFields.back_field_name] = '∆∏∦'
    size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TEXTS, use_cache=False)
    assert size == SizeBytes(15)


@pytest.mark.performance
def test_calculate_note_texts_size_performance(note: Note, size_calculator: SizeCalculator):
    execution_time: float = timeit.timeit(
        lambda: size_calculator.calculate_note_size(note, SizeType.TEXTS, use_cache=True), number=500_000)
    assert execution_time <= 1


def test_calculate_note_files_size(note: Note, size_calculator: SizeCalculator):
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.FILES, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.content0) +
                                    len(DefaultFields.content1) +
                                    len(DefaultFields.content2))
    assert act_size == exp_size


def test_calculate_note_total_size(note: Note, size_calculator: SizeCalculator):
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                    len(DefaultFields.back_field_content.encode()) +
                                    len(DefaultFields.content0) +
                                    len(DefaultFields.content1) +
                                    len(DefaultFields.content2))
    assert act_size == exp_size


def test_calculate_note_total_size_missing_file(note: Note, size_calculator: SizeCalculator):
    content: str = 'Missing file: <img src="absents.png"> ￡'
    note[DefaultFields.front_field_name] = content
    act_size: SizeBytes = size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(content.encode()) +
                                    len(DefaultFields.back_field_content.encode()) +
                                    len(DefaultFields.content0) +
                                    len(DefaultFields.content2))
    assert act_size == exp_size


@pytest.mark.performance
def test_calculate_note_total_size_performance(note: Note, size_calculator: SizeCalculator):
    execution_time: float = timeit.timeit(
        lambda: size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=True), number=500_000)
    assert execution_time <= 1


def test_calculate_note_file_sizes(note: Note, size_calculator: SizeCalculator):
    act_file_sizes: dict[MediaFile, SizeBytes] = size_calculator.calculate_note_file_sizes(note, use_cache=False)
    exp_file_sizes: dict[MediaFile, SizeBytes] = {
        DefaultFields.file0: SizeBytes(len(DefaultFields.content0)),
        DefaultFields.file1: SizeBytes(len(DefaultFields.content1)),
        DefaultFields.file2: SizeBytes(len(DefaultFields.content2))}
    assert act_file_sizes == exp_file_sizes


@pytest.mark.performance
def test_calculate_note_file_sizes_performance(note: Note, size_calculator: SizeCalculator):
    execution_time: float = timeit.timeit(lambda: size_calculator.calculate_note_file_sizes(note, use_cache=True),
                                          number=500_000)
    assert execution_time <= 1


def test_calculate_size_of_files(col: Collection, size_calculator: SizeCalculator):
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
