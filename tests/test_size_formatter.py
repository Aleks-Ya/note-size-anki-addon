import tempfile
import time
import unittest

from anki.collection import Collection

from note_size.size_calculator import SizeBytes, MediaFile
from note_size.size_formatter import SizeFormatter, SizeStr


class SizeFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.size_formatter: SizeFormatter = SizeFormatter()

    def test_bytes_to_human_str(self):
        self.assertEqual(SizeStr("0B"), self.size_formatter.bytes_to_human_str(SizeBytes(0)))
        self.assertEqual(SizeStr("456B"), self.size_formatter.bytes_to_human_str(SizeBytes(456)))
        self.assertEqual(SizeStr("1.4KB"), self.size_formatter.bytes_to_human_str(SizeBytes(1_456)))
        self.assertEqual(SizeStr("1.5MB"), self.size_formatter.bytes_to_human_str(SizeBytes(1_600_456)))
        self.assertEqual(SizeStr("1.7GB"), self.size_formatter.bytes_to_human_str(SizeBytes(1_784_600_456)))
        self.assertEqual(SizeStr("1626.8GB"), self.size_formatter.bytes_to_human_str(SizeBytes(1_746_784_600_456)))

    def test_file_size_to_human_string(self):
        file: MediaFile = MediaFile('picture.jpg')
        size: SizeBytes = SizeBytes(50)
        act_file_str, act_size_str = self.size_formatter.file_size_to_human_string(file, size, 50)
        self.assertEqual('picture.jpg', act_file_str)
        self.assertEqual('50B', act_size_str)

    def test_file_size_to_human_string_prune_long_file_name(self):
        max_length: int = 30
        file: MediaFile = MediaFile('long_long_long_long_long_long.jpg')
        size: SizeBytes = SizeBytes(17)
        act_file_str, act_size_str = self.size_formatter.file_size_to_human_string(file, size, max_length)
        self.assertEqual('long_long_l...ng_long.jpg', act_file_str)
        self.assertEqual('17B', act_size_str)
        self.assertLessEqual(len(f"{act_size_str}: {act_size_str}"), max_length)

    def test_bytes_to_human_str_performance(self):
        start_time: float = time.time()
        for i in range(0, 100_000):
            self.size_formatter.bytes_to_human_str(SizeBytes(i))
        end_time: float = time.time()
        duration_sec: float = end_time - start_time
        self.assertLessEqual(duration_sec, 2)

    def test_file_size_to_human_string_performance(self):
        start_time: float = time.time()
        file: MediaFile = MediaFile('long_long_long_long_long_long.jpg')
        for i in range(0, 100_000):
            self.size_formatter.file_size_to_human_string(file, SizeBytes(i), 10)
        end_time: float = time.time()
        duration_sec: float = end_time - start_time
        self.assertLessEqual(duration_sec, 4)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
