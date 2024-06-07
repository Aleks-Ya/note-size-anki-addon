import tempfile
import unittest

from anki.collection import Collection

from note_size.size_formatter import SizeFormatter


class SizeFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])

    def test_bytes_to_human_str(self):
        self.assertEqual("0B", SizeFormatter.bytes_to_human_str(0))
        self.assertEqual("456B", SizeFormatter.bytes_to_human_str(456))
        self.assertEqual("1.4KB", SizeFormatter.bytes_to_human_str(1_456))
        self.assertEqual("1.5MB", SizeFormatter.bytes_to_human_str(1_600_456))
        self.assertEqual("1.7GB", SizeFormatter.bytes_to_human_str(1_784_600_456))
        self.assertEqual("1626.8GB", SizeFormatter.bytes_to_human_str(1_746_784_600_456))

    def test_file_sizes_to_human_str(self):
        file_sizes: dict[str, int] = {'picture.jpg': 7, 'sound.mp3': 5, 'animation.gif': 9}
        act_human_strings: list[str] = SizeFormatter.file_sizes_to_human_strings(file_sizes, 50)
        exp_human_strings: list[str] = ['picture.jpg: 7B', 'sound.mp3: 5B', 'animation.gif: 9B']
        self.assertListEqual(exp_human_strings, act_human_strings)

    def test_prune_long_file_names(self):
        file_sizes: dict[str, int] = {'long_long_long_long_long_long.jpg': 17, 'short_short.jpg': 7}
        max_length: int = 30
        act_human_strings: list[str] = SizeFormatter.file_sizes_to_human_strings(file_sizes, max_length)
        exp_human_strings: list[str] = ['long_long_l...ng_long.jpg: 17B', 'short_short.jpg: 7B']
        self.assertListEqual(exp_human_strings, act_human_strings)
        for act_human_string in act_human_strings:
            self.assertLessEqual(len(act_human_string), max_length)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
