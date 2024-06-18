import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note

from note_size.cache.media_cache import MediaCache
from note_size.types import SizeBytes, MediaFile
from note_size.calculator.size_calculator import SizeCalculator
from tests.data import Data


class SizeCalculatorTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: Data = Data(self.col)
        self.note: Note = self.td.create_note_with_files()
        media_cache: MediaCache = MediaCache(self.col)
        self.size_calculator: SizeCalculator = SizeCalculator(media_cache)

    def test_calculate_texts_size(self):
        act_size: SizeBytes = SizeCalculator.calculate_texts_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(Data.front_field_content_with_files.encode()) +
                                        len(Data.back_field_content_with_files.encode()))
        self.assertEqual(exp_size, act_size)

    def test_calculate_texts_size_unicode(self):
        note: Note = self.td.create_note_without_files()
        note[Data.front_field_name] = '∑￡'
        note[Data.back_field_name] = '∆∏∦'
        size: SizeBytes = SizeCalculator.calculate_texts_size(note)
        self.assertEqual(SizeBytes(15), size)

    def test_calculate_files_size(self):
        act_size: SizeBytes = self.size_calculator.calculate_files_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(Data.content1) + len(Data.content2) + len(Data.content3))
        self.assertEqual(exp_size, act_size)

    def test_calculate_note_size(self):
        act_size: SizeBytes = self.size_calculator.calculate_note_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(Data.front_field_content_with_files.encode())
                                        + len(Data.back_field_content_with_files.encode())
                                        + len(Data.content1) + len(Data.content2) + len(Data.content3))
        self.assertEqual(exp_size, act_size)

    def test_calculate_note_size_missing_file(self):
        content: str = 'Missing file: <img src="absents.png"> ￡'
        self.note[Data.front_field_name] = content
        act_size: SizeBytes = self.size_calculator.calculate_note_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(content.encode()) + len(Data.back_field_content_with_files.encode())
                                        + len(Data.content1) + len(Data.content3))
        self.assertEqual(exp_size, act_size)

    def test_file_sizes(self):
        act_file_sizes: dict[MediaFile, SizeBytes] = self.size_calculator.file_sizes(self.note)
        exp_file_sizes: dict[MediaFile, SizeBytes] = {Data.file1: SizeBytes(len(Data.content1)),
                                                      Data.file2: SizeBytes(len(Data.content2)),
                                                      Data.file3: SizeBytes(len(Data.content3))}
        self.assertDictEqual(exp_file_sizes, act_file_sizes)

    def test_sort_by_size_desc(self):
        unsorted_dict: dict[MediaFile, SizeBytes] = {Data.file1: SizeBytes(len(Data.content1)),
                                                     Data.file2: SizeBytes(len(Data.content2)),
                                                     Data.file3: SizeBytes(len(Data.content3))}
        self.assertEqual("{'picture.jpg': 7, 'sound.mp3': 5, 'animation.gif': 9}", str(unsorted_dict))
        sorted_dict: dict[MediaFile, SizeBytes] = SizeCalculator.sort_by_size_desc(unsorted_dict)
        self.assertEqual("{'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5}", str(sorted_dict))

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
