import timeit

from note_size.cache.media_cache import MediaCache
from note_size.types import SizeBytes
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
