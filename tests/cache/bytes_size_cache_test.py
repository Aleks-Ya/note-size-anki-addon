import timeit

import pytest

from note_size.cache.bytes_size_cache import BytesSizeCache
from note_size.core.common.types import SizeBytes
from tests.data import Digits


@pytest.mark.performance
def test_bytes_to_str_performance(bytes_size_cache: BytesSizeCache):
    execution_time: float = timeit.timeit(lambda: __run_bytes_to_str(bytes_size_cache), number=1)
    assert execution_time <= 0.5


def __run_bytes_to_str(bytes_size_cache: BytesSizeCache):
    for i in range(0, 50_000):
        bytes_size_cache.bytes_to_str(SizeBytes(i), Digits.one)


def test_get_cache_size(bytes_size_cache: BytesSizeCache):
    assert bytes_size_cache.get_cache_size() == 0
    bytes_size_cache.bytes_to_str(SizeBytes(0), Digits.one)
    assert bytes_size_cache.get_cache_size() == 1
    bytes_size_cache.bytes_to_str(SizeBytes(0), Digits.one)
    assert bytes_size_cache.get_cache_size() == 1
    bytes_size_cache.bytes_to_str(SizeBytes(1), Digits.one)
    assert bytes_size_cache.get_cache_size() == 2
    bytes_size_cache.invalidate_cache()
    assert bytes_size_cache.get_cache_size() == 0
