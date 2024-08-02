import timeit

from anki.notes import Note

from note_size.cache.media_cache import MediaCache
from note_size.types import SizeBytes, FilesNumber
from tests.data import Data, DefaultFields


def test_get_file_size(td: Data, media_cache: MediaCache):
    td.create_note_with_files()
    act_file_size_1: SizeBytes = media_cache.get_file_size(DefaultFields.file0, use_cache=False)
    exp_file_size_1: SizeBytes = SizeBytes(len(DefaultFields.content0))
    assert act_file_size_1 == exp_file_size_1


def test_get_file_size_cached(td: Data, media_cache: MediaCache):
    td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: media_cache.get_file_size(DefaultFields.file0, use_cache=True), number=1_000_000)
    assert execution_time <= 1


def test_get_total_size(td: Data, media_cache: MediaCache):
    td.create_note_with_files()
    media_cache.get_file_size(DefaultFields.file0, use_cache=True)
    media_cache.get_file_size(DefaultFields.file1, use_cache=True)
    media_cache.get_file_size(DefaultFields.file1, use_cache=True)  # check for duplicating
    act_total_size: SizeBytes = media_cache.get_total_files_size()
    exp_total_size: SizeBytes = SizeBytes(len(DefaultFields.content0) + len(DefaultFields.content1))
    assert exp_total_size == act_total_size


def test_get_unused_files_size(td: Data, media_cache: MediaCache):
    assert media_cache.get_unused_files_size(use_cache=True) == (SizeBytes(0), FilesNumber(0))
    note: Note = td.create_note_with_files()
    assert media_cache.get_unused_files_size(use_cache=True) == (SizeBytes(0), FilesNumber(0))
    Data.replace_in_front_field(note, '<img src="picture.jpg">', '')
    Data.replace_in_front_field(note, '<img src="animation.gif">', '')
    assert media_cache.get_unused_files_size(use_cache=True) == (SizeBytes(0), FilesNumber(0))
    assert media_cache.get_unused_files_size(use_cache=False) == (SizeBytes(0), FilesNumber(0))  # TODO fix it
