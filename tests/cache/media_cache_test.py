import timeit

import pytest
from anki.notes import Note

from note_size.cache.media_cache import MediaCache
from note_size.common.types import SizeBytes, FilesNumber, MediaFile, FileSize
from tests.data import Data, MediaFiles, FileContents


def test_get_file_size(td: Data, media_cache: MediaCache):
    td.create_note_with_files()
    act_file_size_1: FileSize = media_cache.get_file_size(MediaFiles.picture, use_cache=False)
    exp_file_size_1: FileSize = FileSize(SizeBytes(len(FileContents.picture)))
    assert act_file_size_1 == exp_file_size_1


def test_get_missing_files_number(td: Data, media_cache: MediaCache):
    media_files: set[MediaFile] = {MediaFiles.picture, MediaFiles.sound, MediaFiles.animation, MediaFiles.video}
    assert media_cache.get_missing_files_number(media_files, use_cache=False) == (FilesNumber(0), FilesNumber(4))
    td.create_note_with_files()
    assert media_cache.get_missing_files_number(media_files, use_cache=False) == (FilesNumber(3), FilesNumber(1))


@pytest.mark.performance
def test_get_file_size_cached_performance(media_cache: MediaCache, td: Data):
    td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: media_cache.get_file_size(MediaFiles.picture, use_cache=True), number=450_000)
    assert execution_time <= 1


def test_get_unused_files_size(media_cache: MediaCache, td: Data):
    assert media_cache.get_unused_files_size(use_cache=True) == (SizeBytes(0), FilesNumber(0))
    note: Note = td.create_note_with_files()
    assert media_cache.get_unused_files_size(use_cache=True) == (SizeBytes(0), FilesNumber(0))
    assert media_cache.get_unused_files_size(use_cache=False) == (SizeBytes(0), FilesNumber(0))
    Data.replace_in_front_field(note, f'<img src="{MediaFiles.sound}">', '')
    assert media_cache.get_unused_files_size(use_cache=True) == (SizeBytes(5), FilesNumber(1))
    assert media_cache.get_unused_files_size(use_cache=False) == (SizeBytes(5), FilesNumber(1))


def test_get_cache_size(media_cache: MediaCache, td: Data):
    assert media_cache.get_cache_size() == 0
    td.create_note_with_files()
    media_cache.get_file_size(MediaFiles.picture, use_cache=True)
    assert media_cache.get_cache_size() == 1
    media_cache.invalidate_cache()
    assert media_cache.get_cache_size() == 0


def test_get_updated_files(media_cache: MediaCache, td: Data):
    td.create_note_with_files()
    exp_size_0: FileSize = FileSize(SizeBytes(7))
    exp_size_1: FileSize = FileSize(SizeBytes(5))
    exp_size_2: FileSize = FileSize(SizeBytes(9))
    assert media_cache.get_file_size(MediaFiles.picture, use_cache=True) == exp_size_0
    assert media_cache.get_file_size(MediaFiles.sound, use_cache=True) == exp_size_1
    assert media_cache.get_file_size(MediaFiles.animation, use_cache=True) == exp_size_2
    td.write_file(MediaFiles.sound, "new content 1")
    td.write_file(MediaFiles.animation, "new content 2")
    assert media_cache.get_file_size(MediaFiles.picture, use_cache=True) == exp_size_0
    assert media_cache.get_file_size(MediaFiles.sound, use_cache=True) == exp_size_1
    assert media_cache.get_file_size(MediaFiles.animation, use_cache=True) == exp_size_2
    updated_files: set[MediaFile] = media_cache.get_updated_files()
    assert updated_files == {MediaFiles.sound, MediaFiles.animation}
