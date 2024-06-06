import tempfile
import unittest

from anki.collection import Collection

from note_size.size_formatter import SizeFormatter


class SizeFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])

    def test_bytes_to_human_str(self):
        self.assertEqual("1.6MB", SizeFormatter.bytes_to_human_str(1_600_456))

    def test_file_sizes_to_human_str(self):
        file_sizes: dict[str, int] = {'picture.jpg': 7, 'sound.mp3': 5, 'animation.gif': 9}
        act_human_strings: list[str] = SizeFormatter.file_sizes_to_human_strings(file_sizes)
        exp_human_strings: list[str] = ['picture.jpg: 7B', 'sound.mp3: 5B', 'animation.gif: 9B']
        self.assertListEqual(exp_human_strings, act_human_strings)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
