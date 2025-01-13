import timeit

import pytest

from note_size.calculator.size_formatter import SizeFormatter
from note_size.common.types import SizeBytes, SizeStr, SizePrecision
from tests.data import Precisions


@pytest.mark.parametrize("size_bytes,precision,size_str", [
    (5, Precisions.zero, '5 B'),
    (5, Precisions.one, '5 B'),
    (5, Precisions.three, '5 B'),
    (20, Precisions.zero, '20 B'),
    (20, Precisions.one, '20 B'),
    (20, Precisions.three, '20 B'),
    (456, Precisions.zero, '456 B'),
    (456, Precisions.one, '456 B'),
    (456, Precisions.three, '456 B'),

    (1024, Precisions.zero, '1 KB'),
    (1024, Precisions.one, '1.0 KB'),
    (1024, Precisions.three, '1.000 KB'),
    (45_654, Precisions.zero, '45 KB'),
    (45_654, Precisions.one, '44.6 KB'),
    (45_654, Precisions.three, '44.584 KB'),
    (987_654, Precisions.zero, '965 KB'),
    (987_654, Precisions.one, '964.5 KB'),
    (987_654, Precisions.three, '964.506 KB'),

    (1_234_567, Precisions.zero, '1 MB'),
    (1_234_567, Precisions.one, '1.2 MB'),
    (1_234_567, Precisions.three, '1.177 MB'),

    (1_123_234_567, Precisions.zero, '1 GB'),
    (1_123_234_567, Precisions.one, '1.0 GB'),
    (1_123_234_567, Precisions.three, '1.046 GB'),
    (1_567_123_234_567, Precisions.zero, '1459 GB'),
    (1_567_123_234_567, Precisions.one, '1459.5 GB'),
    (1_567_123_234_567, Precisions.three, '1459.497 GB'),
])
def test_bytes_to_str(size_formatter: SizeFormatter, size_bytes: int, precision: SizePrecision, size_str: str):
    assert size_formatter.bytes_to_str(SizeBytes(size_bytes), precision) == SizeStr(size_str)


@pytest.mark.parametrize("size_str,size_bytes", [
    ("0 B", 0),
    ("456 B", 456),
    ("456B", 456),
    ("1.4 KB", 1_433),
    ("1.4KB", 1_433),
    ("1.5 MB", 1_572_864),
    ("1626.8 GB", 1_746_763_199_283),
])
def test_str_to_bytes(size_formatter: SizeFormatter, size_str: str, size_bytes: int):
    assert size_formatter.str_to_bytes(SizeStr(size_str)) == SizeBytes(size_bytes)


@pytest.mark.performance
def test_bytes_to_str_performance(size_formatter: SizeFormatter):
    execution_time: float = timeit.timeit(lambda: __run_bytes_to_str(size_formatter), number=1)
    assert execution_time <= 0.5


def __run_bytes_to_str(size_formatter: SizeFormatter):
    for i in range(0, 50_000):
        size_formatter.bytes_to_str(SizeBytes(i), Precisions.one)


@pytest.mark.performance
def test_str_to_bytes_performance(size_formatter: SizeFormatter):
    execution_time: float = timeit.timeit(lambda: __run_str_to_bytes(size_formatter), number=1)
    assert execution_time <= 0.5


def test_get_cache_size(size_formatter: SizeFormatter):
    assert size_formatter.get_cache_size() == 0
    size_formatter.bytes_to_str(SizeBytes(0), Precisions.one)
    assert size_formatter.get_cache_size() == 1
    size_formatter.bytes_to_str(SizeBytes(0), Precisions.one)
    assert size_formatter.get_cache_size() == 1
    size_formatter.bytes_to_str(SizeBytes(1), Precisions.one)
    assert size_formatter.get_cache_size() == 2
    size_formatter.invalidate_cache()
    assert size_formatter.get_cache_size() == 0


def __run_str_to_bytes(size_formatter: SizeFormatter):
    for i in range(0, 100_000):
        size_formatter.str_to_bytes(SizeStr(f"{i} B"))
