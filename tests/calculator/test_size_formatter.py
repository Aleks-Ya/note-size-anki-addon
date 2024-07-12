import tempfile
import timeit
import unittest

from anki.collection import Collection

from note_size.types import SizeBytes, MediaFile, SizeStr
from note_size.calculator.size_formatter import SizeFormatter


class TestSizeFormatter(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.size_formatter: SizeFormatter = SizeFormatter()

    def test_bytes_to_str(self):
        self.assertEqual(SizeStr("0 B"), self.size_formatter.bytes_to_str(SizeBytes(0)))
        self.assertEqual(SizeStr("456 B"), self.size_formatter.bytes_to_str(SizeBytes(456)))
        self.assertEqual(SizeStr("1.4 KB"), self.size_formatter.bytes_to_str(SizeBytes(1_456)))
        self.assertEqual(SizeStr("1.5 MB"), self.size_formatter.bytes_to_str(SizeBytes(1_600_456)))
        self.assertEqual(SizeStr("1.7 GB"), self.size_formatter.bytes_to_str(SizeBytes(1_784_600_456)))
        self.assertEqual(SizeStr("1626.8 GB"), self.size_formatter.bytes_to_str(SizeBytes(1_746_784_600_456)))

    def test_file_size_to_str(self):
        file: MediaFile = MediaFile('picture.jpg')
        size: SizeBytes = SizeBytes(50)
        act_file_str, act_size_str = self.size_formatter.file_size_to_str(file, size, 50)
        self.assertEqual('picture.jpg', act_file_str)
        self.assertEqual('50 B', act_size_str)

    def test_file_size_to_str_prune_long_file_name(self):
        max_length: int = 30
        file: MediaFile = MediaFile('long_long_long_long_long_long.jpg')
        size: SizeBytes = SizeBytes(17)
        act_file_str, act_size_str = self.size_formatter.file_size_to_str(file, size, max_length)
        self.assertEqual('long_long_...g_long.jpg', act_file_str)
        self.assertEqual('17 B', act_size_str)
        self.assertLessEqual(len(f"{act_size_str}: {act_size_str}"), max_length)

    def test_bytes_to_str_performance(self):
        execution_time: float = timeit.timeit(self._run_bytes_to_str, number=1)
        self.assertLessEqual(execution_time, 0.5)

    def test_file_size_to_str_performance(self):
        execution_time: float = timeit.timeit(self._run_file_size_to_str, number=1)
        self.assertLessEqual(execution_time, 0.5)

    def _run_bytes_to_str(self):
        for i in range(0, 100_000):
            self.size_formatter.bytes_to_str(SizeBytes(i))

    def _run_file_size_to_str(self):
        file: MediaFile = MediaFile('long_long_long_long_long_long.jpg')
        for i in range(0, 100_000):
            self.size_formatter.file_size_to_str(file, SizeBytes(i), 10)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
