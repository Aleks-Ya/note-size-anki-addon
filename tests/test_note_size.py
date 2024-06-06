import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note

from note_size.note_size import NoteSize


class NoteSizeTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.content1: bytes = b'picture'
        self.content2: bytes = b'sound'
        self.content3: bytes = b'animation'
        self.filename1: str = self.col.media.write_data('picture.jpg', self.content1)
        self.filename2: str = self.col.media.write_data('sound.mp3', self.content2)
        self.filename3: str = self.col.media.write_data('animation.gif', self.content3)
        self.note: Note = self.col.newNote()
        self.front: str = f'Files: <img src="{self.filename1}"> <img src="{self.filename2}">'
        self.back: str = f'Files: <img src="{self.filename1}"> <img src="{self.filename3}">'
        self.note['Front'] = self.front
        self.note['Back'] = self.back
        self.col.addNote(self.note)

    def test_bytes_to_human_str(self):
        self.assertEqual("1.6MB", NoteSize.bytes_to_human_str(1_600_456))

    def test_total_text_size(self):
        act_size: int = NoteSize.total_text_size(self.note)
        exp_size: int = len(self.front) + len(self.back)
        self.assertEqual(exp_size, act_size)

    def test_total_file_size(self):
        act_size: int = NoteSize.total_file_size(self.note)
        exp_size: int = len(self.content1) + len(self.content2) + len(self.content3)
        self.assertEqual(exp_size, act_size)

    def test_calculate_note_size(self):
        act_size: int = NoteSize.calculate_note_size(self.note)
        exp_size: int = len(self.front) + len(self.back) + len(self.content1) + len(self.content2) + len(self.content3)
        self.assertEqual(exp_size, act_size)

    def test_file_sizes(self):
        act_file_sizes: dict[str, int] = NoteSize.file_sizes(self.note)
        exp_file_sizes: dict[str, int] = {self.filename1: len(self.content1),
                                          self.filename2: len(self.content2),
                                          self.filename3: len(self.content3)}
        self.assertDictEqual(exp_file_sizes, act_file_sizes)

    def test_sort_by_size_desc(self):
        unsorted_dict: dict[str, int] = {self.filename1: len(self.content1),
                                         self.filename2: len(self.content2),
                                         self.filename3: len(self.content3)}
        self.assertEqual("{'picture.jpg': 7, 'sound.mp3': 5, 'animation.gif': 9}", str(unsorted_dict))
        sorted_dict: dict[str, int] = NoteSize.sort_by_size_desc(unsorted_dict)
        self.assertEqual("{'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5}", str(sorted_dict))

    def test_file_sizes_to_human_str(self):
        file_sizes: dict[str, int] = NoteSize.file_sizes(self.note)
        act_human_strings: list[str] = NoteSize.file_sizes_to_human_strings(file_sizes)
        exp_human_strings: list[str] = ['picture.jpg: 7B', 'sound.mp3: 5B', 'animation.gif: 9B']
        self.assertListEqual(exp_human_strings, act_human_strings)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
