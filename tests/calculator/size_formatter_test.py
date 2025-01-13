import timeit

import pytest

from note_size.calculator.size_formatter import SizeFormatter
from note_size.common.types import SizeBytes, SizeStr, SignificantDigits
from tests.data import Digits


@pytest.mark.parametrize("size_bytes,significant_digits,size_str", [
    (5, Digits.zero, '5 B'),
    (5, Digits.one, '5 B'),
    (5, Digits.two, '5 B'),
    (5, Digits.three, '5 B'),
    (20, Digits.zero, '20 B'),
    (20, Digits.one, '20 B'),
    (20, Digits.two, '20 B'),
    (20, Digits.three, '20 B'),
    (456, Digits.zero, '456 B'),
    (456, Digits.one, '456 B'),
    (456, Digits.two, '456 B'),
    (456, Digits.three, '456 B'),
    (1023, Digits.zero, '1023 B'),
    (1023, Digits.one, '1023 B'),
    (1023, Digits.two, '1023 B'),
    (1023, Digits.three, '1023 B'),

    (1024, Digits.zero, '1 KB'),
    (1024, Digits.one, '1 KB'),
    (1024, Digits.two, '1.0 KB'),
    (1024, Digits.three, '1.00 KB'),
    (45_654, Digits.zero, '45 KB'),
    (45_654, Digits.one, '45 KB'),
    (45_654, Digits.two, '45 KB'),
    (45_654, Digits.three, '44.6 KB'),
    (987_654, Digits.zero, '965 KB'),
    (987_654, Digits.one, '965 KB'),
    (987_654, Digits.two, '965 KB'),
    (987_654, Digits.three, '965 KB'),

    (1_234_567, Digits.zero, '1 MB'),
    (1_234_567, Digits.one, '1 MB'),
    (1_234_567, Digits.two, '1.2 MB'),
    (1_234_567, Digits.three, '1.18 MB'),

    (1_123_234_567, Digits.zero, '1 GB'),
    (1_123_234_567, Digits.one, '1 GB'),
    (1_123_234_567, Digits.two, '1.0 GB'),
    (1_123_234_567, Digits.three, '1.05 GB'),
    (1_567_123_234_567, Digits.zero, '1459 GB'),
    (1_567_123_234_567, Digits.one, '1459 GB'),
    (1_567_123_234_567, Digits.two, '1459 GB'),
    (1_567_123_234_567, Digits.three, '1459 GB'),

    (10180, Digits.two, '9.9 KB'),
    (10239, Digits.two, '10.0 KB'),
    (10254, Digits.two, '10 KB'),
    (10800, Digits.two, '11 KB'),
])
def test_bytes_to_str(size_formatter: SizeFormatter, size_bytes: int, significant_digits: SignificantDigits,
                      size_str: str):
    assert size_formatter.bytes_to_str(SizeBytes(size_bytes), significant_digits) == SizeStr(size_str)


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
        size_formatter.bytes_to_str(SizeBytes(i), Digits.one)


@pytest.mark.performance
def test_str_to_bytes_performance(size_formatter: SizeFormatter):
    execution_time: float = timeit.timeit(lambda: __run_str_to_bytes(size_formatter), number=1)
    assert execution_time <= 0.5


def test_get_cache_size(size_formatter: SizeFormatter):
    assert size_formatter.get_cache_size() == 0
    size_formatter.bytes_to_str(SizeBytes(0), Digits.one)
    assert size_formatter.get_cache_size() == 1
    size_formatter.bytes_to_str(SizeBytes(0), Digits.one)
    assert size_formatter.get_cache_size() == 1
    size_formatter.bytes_to_str(SizeBytes(1), Digits.one)
    assert size_formatter.get_cache_size() == 2
    size_formatter.invalidate_cache()
    assert size_formatter.get_cache_size() == 0


def __run_str_to_bytes(size_formatter: SizeFormatter):
    for i in range(0, 100_000):
        size_formatter.str_to_bytes(SizeStr(f"{i} B"))
