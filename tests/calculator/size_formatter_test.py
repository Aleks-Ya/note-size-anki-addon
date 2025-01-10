import timeit

import pytest

from note_size.calculator.size_formatter import SizeFormatter
from note_size.types import SizeBytes, SizeStr
from tests.data import Precisions


def test_bytes_to_str(size_formatter: SizeFormatter):
    assert size_formatter.bytes_to_str(SizeBytes(0), Precisions.one) == SizeStr("0 B")
    assert size_formatter.bytes_to_str(SizeBytes(456), Precisions.one) == SizeStr("456 B")
    assert size_formatter.bytes_to_str(SizeBytes(1_456), Precisions.one) == SizeStr("1.4 KB")
    assert size_formatter.bytes_to_str(SizeBytes(1_600_456), Precisions.one) == SizeStr("1.5 MB")
    assert size_formatter.bytes_to_str(SizeBytes(1_784_600_456), Precisions.one) == SizeStr("1.7 GB")
    assert size_formatter.bytes_to_str(SizeBytes(1_746_784_600_456), Precisions.one) == SizeStr("1626.8 GB")


def test_str_to_bytes(size_formatter: SizeFormatter):
    assert size_formatter.str_to_bytes(SizeStr("0 B")) == SizeBytes(0)
    assert size_formatter.str_to_bytes(SizeStr("456 B")) == SizeBytes(456)
    assert size_formatter.str_to_bytes(SizeStr("456B")) == SizeBytes(456)
    assert size_formatter.str_to_bytes(SizeStr("1.4 KB")) == SizeBytes(1_433)
    assert size_formatter.str_to_bytes(SizeStr("1.4KB")) == SizeBytes(1_433)
    assert size_formatter.str_to_bytes(SizeStr("1.5 MB")) == SizeBytes(1_572_864)
    assert size_formatter.str_to_bytes(SizeStr("1626.8 GB")) == SizeBytes(1_746_763_199_283)


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
