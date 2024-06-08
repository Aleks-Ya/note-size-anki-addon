import tempfile
import unittest

from anki.collection import Collection

from note_size.size_formatter import SizeFormatter


class SizeFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.size_formatter: SizeFormatter = SizeFormatter()

    def test_bytes_to_human_str(self):
        self.assertEqual("0B", self.size_formatter.bytes_to_human_str(0))
        self.assertEqual("456B", self.size_formatter.bytes_to_human_str(456))
        self.assertEqual("1.4KB", self.size_formatter.bytes_to_human_str(1_456))
        self.assertEqual("1.5MB", self.size_formatter.bytes_to_human_str(1_600_456))
        self.assertEqual("1.7GB", self.size_formatter.bytes_to_human_str(1_784_600_456))
        self.assertEqual("1626.8GB", self.size_formatter.bytes_to_human_str(1_746_784_600_456))

    def test_file_size_to_human_string(self):
        act_file_str, act_size_str = self.size_formatter.file_size_to_human_string('picture.jpg', 50, 50)
        self.assertEqual('picture.jpg', act_file_str)
        self.assertEqual('50B', act_size_str)

    def test_file_size_to_human_string_prune_long_file_name(self):
        max_length: int = 30
        file: str = 'long_long_long_long_long_long.jpg'
        size: int = 17
        act_file_str, act_size_str = self.size_formatter.file_size_to_human_string(file, size, max_length)
        self.assertEqual('long_long_l...ng_long.jpg', act_file_str)
        self.assertEqual('17B', act_size_str)
        self.assertLessEqual(len(f"{act_size_str}: {act_size_str}"), max_length)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
