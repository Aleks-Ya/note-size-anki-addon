import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note

from note_size import Config
from note_size.cache.media_cache import MediaCache
from note_size.types import SizeBytes, MediaFile
from note_size.calculator.size_calculator import SizeCalculator
from tests.data import Data, NoteData


class TestSizeCalculator(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: Data = Data(self.col)
        self.note_data: NoteData = self.td.create_note_with_files()
        self.note: Note = self.note_data.note
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        self.size_calculator: SizeCalculator = SizeCalculator(media_cache)

    def test_calculate_texts_size(self):
        act_size: SizeBytes = SizeCalculator.calculate_texts_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(self.note_data.front_field_content.encode()) +
                                        len(self.note_data.back_field_content.encode()))
        self.assertEqual(exp_size, act_size)

    def test_calculate_texts_size_unicode(self):
        note_data: NoteData = self.td.create_note_without_files()
        note: Note = note_data.note
        note[note_data.front_field_name] = '∑￡'
        note[note_data.back_field_name] = '∆∏∦'
        size: SizeBytes = SizeCalculator.calculate_texts_size(note)
        self.assertEqual(SizeBytes(15), size)

    def test_calculate_files_size(self):
        act_size: SizeBytes = self.size_calculator.calculate_files_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(self.note_data.file_contents[0]) + len(self.note_data.file_contents[1]) +
                                        len(self.note_data.file_contents[2]))
        self.assertEqual(exp_size, act_size)

    def test_calculate_note_size(self):
        act_size: SizeBytes = self.size_calculator.calculate_note_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(self.note_data.front_field_content.encode())
                                        + len(self.note_data.back_field_content.encode())
                                        + len(self.note_data.file_contents[0]) + len(self.note_data.file_contents[1]) +
                                        len(self.note_data.file_contents[2]))
        self.assertEqual(exp_size, act_size)

    def test_calculate_note_size_missing_file(self):
        content: str = 'Missing file: <img src="absents.png"> ￡'
        self.note[self.note_data.front_field_name] = content
        act_size: SizeBytes = self.size_calculator.calculate_note_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(content.encode()) + len(self.note_data.back_field_content.encode())
                                        + len(self.note_data.file_contents[0]) + len(self.note_data.file_contents[2]))
        self.assertEqual(exp_size, act_size)

    def test_file_sizes(self):
        act_file_sizes: dict[MediaFile, SizeBytes] = self.size_calculator.file_sizes(self.note)
        exp_file_sizes: dict[MediaFile, SizeBytes] = {
            self.note_data.files[0]: SizeBytes(len(self.note_data.file_contents[0])),
            self.note_data.files[1]: SizeBytes(len(self.note_data.file_contents[1])),
            self.note_data.files[2]: SizeBytes(len(self.note_data.file_contents[2]))}
        self.assertDictEqual(exp_file_sizes, act_file_sizes)

    def test_sort_by_size_desc(self):
        unsorted_dict: dict[MediaFile, SizeBytes] = {
            self.note_data.files[0]: SizeBytes(len(self.note_data.file_contents[0])),
            self.note_data.files[1]: SizeBytes(len(self.note_data.file_contents[1])),
            self.note_data.files[2]: SizeBytes(len(self.note_data.file_contents[2]))}
        self.assertEqual("{'picture.jpg': 7, 'sound.mp3': 5, 'animation.gif': 9}", str(unsorted_dict))
        sorted_dict: dict[MediaFile, SizeBytes] = SizeCalculator.sort_by_size_desc(unsorted_dict)
        self.assertEqual("{'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5}", str(sorted_dict))

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()