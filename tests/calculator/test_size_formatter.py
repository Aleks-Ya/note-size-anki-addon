import timeit

from note_size.types import SizeBytes, MediaFile, SizeStr
from note_size.calculator.size_formatter import SizeFormatter


def test_bytes_to_str(size_formatter: SizeFormatter):
    assert size_formatter.bytes_to_str(SizeBytes(0)) == SizeStr("0 B")
    assert size_formatter.bytes_to_str(SizeBytes(456)) == SizeStr("456 B")
    assert size_formatter.bytes_to_str(SizeBytes(1_456)) == SizeStr("1.4 KB")
    assert size_formatter.bytes_to_str(SizeBytes(1_600_456)) == SizeStr("1.5 MB")
    assert size_formatter.bytes_to_str(SizeBytes(1_784_600_456)) == SizeStr("1.7 GB")
    assert size_formatter.bytes_to_str(SizeBytes(1_746_784_600_456)) == SizeStr("1626.8 GB")


def test_str_to_bytes(size_formatter: SizeFormatter):
    assert size_formatter.str_to_bytes(SizeStr("0 B")) == SizeBytes(0)
    assert size_formatter.str_to_bytes(SizeStr("456 B")) == SizeBytes(456)
    assert size_formatter.str_to_bytes(SizeStr("456B")) == SizeBytes(456)
    assert size_formatter.str_to_bytes(SizeStr("1.4 KB")) == SizeBytes(1_433)
    assert size_formatter.str_to_bytes(SizeStr("1.4KB")) == SizeBytes(1_433)
    assert size_formatter.str_to_bytes(SizeStr("1.5 MB")) == SizeBytes(1_572_864)
    assert size_formatter.str_to_bytes(SizeStr("1626.8 GB")) == SizeBytes(1_746_763_199_283)


def test_file_size_to_str(size_formatter: SizeFormatter):
    file: MediaFile = MediaFile('picture.jpg')
    size: SizeBytes = SizeBytes(50)
    act_file_str, act_size_str = size_formatter.file_size_to_str(file, size, 50)
    assert act_file_str == 'picture.jpg'
    assert act_size_str == '50 B'


def test_file_size_to_str_prune_long_file_name(size_formatter: SizeFormatter):
    max_length: int = 30
    file: MediaFile = MediaFile('long_long_long_long_long_long.jpg')
    size: SizeBytes = SizeBytes(17)
    act_file_str, act_size_str = size_formatter.file_size_to_str(file, size, max_length)
    assert act_file_str == 'long_long_...g_long.jpg'
    assert act_size_str == '17 B'
    assert len(f"{act_size_str}: {act_size_str}") <= max_length


def test_bytes_to_str_performance(size_formatter: SizeFormatter):
    execution_time: float = timeit.timeit(lambda: __run_bytes_to_str(size_formatter), number=1)
    assert execution_time <= 0.5


def test_file_size_to_str_performance(size_formatter: SizeFormatter):
    execution_time: float = timeit.timeit(lambda: __run_file_size_to_str(size_formatter), number=1)
    assert execution_time <= 0.5


def __run_bytes_to_str(size_formatter: SizeFormatter):
    for i in range(0, 100_000):
        size_formatter.bytes_to_str(SizeBytes(i))


def __run_file_size_to_str(size_formatter: SizeFormatter):
    file: MediaFile = MediaFile('long_long_long_long_long_long.jpg')
    for i in range(0, 100_000):
        size_formatter.file_size_to_str(file, SizeBytes(i), 10)
