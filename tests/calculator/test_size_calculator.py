import pytest
from anki.notes import Note

from note_size.types import SizeBytes, MediaFile
from note_size.calculator.size_calculator import SizeCalculator
from tests.data import Data, DefaultFields


@pytest.fixture
def note(td: Data) -> Note:
    return td.create_note_with_files()


def test_calculate_texts_size(note: Note):
    act_size: SizeBytes = SizeCalculator.calculate_texts_size(note)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                    len(DefaultFields.back_field_content.encode()))
    assert act_size == exp_size


def test_calculate_texts_size_unicode(td: Data):
    note: Note = td.create_note_without_files()
    note[DefaultFields.front_field_name] = '∑￡'
    note[DefaultFields.back_field_name] = '∆∏∦'
    size: SizeBytes = SizeCalculator.calculate_texts_size(note)
    assert size == SizeBytes(15)


def test_calculate_files_size(note: Note, size_calculator: SizeCalculator):
    act_size: SizeBytes = size_calculator.calculate_files_size(note, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.content0) +
                                    len(DefaultFields.content1) +
                                    len(DefaultFields.content2))
    assert act_size == exp_size


def test_calculate_note_size(note: Note, size_calculator: SizeCalculator):
    act_size: SizeBytes = size_calculator.calculate_note_size(note, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                    len(DefaultFields.back_field_content.encode()) +
                                    len(DefaultFields.content0) +
                                    len(DefaultFields.content1) +
                                    len(DefaultFields.content2))
    assert act_size == exp_size


def test_calculate_note_size_missing_file(note: Note, size_calculator: SizeCalculator):
    content: str = 'Missing file: <img src="absents.png"> ￡'
    note[DefaultFields.front_field_name] = content
    act_size: SizeBytes = size_calculator.calculate_note_size(note, use_cache=False)
    exp_size: SizeBytes = SizeBytes(len(content.encode()) +
                                    len(DefaultFields.back_field_content.encode()) +
                                    len(DefaultFields.content0) +
                                    len(DefaultFields.content2))
    assert act_size == exp_size


def test_file_sizes(note: Note, size_calculator: SizeCalculator):
    act_file_sizes: dict[MediaFile, SizeBytes] = size_calculator.file_sizes(note, use_cache=False)
    exp_file_sizes: dict[MediaFile, SizeBytes] = {
        DefaultFields.file0: SizeBytes(len(DefaultFields.content0)),
        DefaultFields.file1: SizeBytes(len(DefaultFields.content1)),
        DefaultFields.file2: SizeBytes(len(DefaultFields.content2))}
    assert act_file_sizes == exp_file_sizes


def test_sort_by_size_desc():
    unsorted_dict: dict[MediaFile, SizeBytes] = {
        DefaultFields.file0: SizeBytes(len(DefaultFields.content0)),
        DefaultFields.file1: SizeBytes(len(DefaultFields.content1)),
        DefaultFields.file2: SizeBytes(len(DefaultFields.content2))}
    assert str(unsorted_dict) == "{'picture.jpg': 7, 'sound.mp3': 5, 'animation.gif': 9}"
    sorted_dict: dict[MediaFile, SizeBytes] = SizeCalculator.sort_by_size_desc(unsorted_dict)
    assert str(sorted_dict) == "{'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5}"
