import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note

from note_size.size_calculator import SizeCalculator, SizeBytes, MediaFile
from tests.data import TestData


class SizeCalculatorTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: TestData = TestData()
        self.note: Note = self.td.create_note_with_files(self.col)

    def test_total_text_size(self):
        act_size: SizeBytes = SizeCalculator.total_text_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(self.td.front_field_content_with_files) +
                                        len(self.td.back_field_content_with_files))
        self.assertEqual(exp_size, act_size)

    def test_total_file_size(self):
        act_size: SizeBytes = SizeCalculator.total_file_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(self.td.content1) + len(self.td.content2) + len(self.td.content3))
        self.assertEqual(exp_size, act_size)

    def test_calculate_note_size(self):
        act_size: SizeBytes = SizeCalculator.calculate_note_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(self.td.front_field_content_with_files)
                                        + len(self.td.back_field_content_with_files)
                                        + len(self.td.content1) + len(self.td.content2) + len(self.td.content3))
        self.assertEqual(exp_size, act_size)

    def test_calculate_note_size_missing_file(self):
        content: str = 'Missing file: <img src="absents.png">'
        self.note[self.td.front_field_name] = content
        act_size: SizeBytes = SizeCalculator.calculate_note_size(self.note)
        exp_size: SizeBytes = SizeBytes(len(content) + len(self.td.back_field_content_with_files)
                                        + len(self.td.content1) + len(self.td.content3))
        self.assertEqual(exp_size, act_size)

    def test_file_sizes(self):
        act_file_sizes: dict[MediaFile, SizeBytes] = SizeCalculator.file_sizes(self.note)
        exp_file_sizes: dict[MediaFile, SizeBytes] = {self.td.filename1: SizeBytes(len(self.td.content1)),
                                                      self.td.filename2: SizeBytes(len(self.td.content2)),
                                                      self.td.filename3: SizeBytes(len(self.td.content3))}
        self.assertDictEqual(exp_file_sizes, act_file_sizes)

    def test_sort_by_size_desc(self):
        unsorted_dict: dict[MediaFile, SizeBytes] = {self.td.filename1: SizeBytes(len(self.td.content1)),
                                                     self.td.filename2: SizeBytes(len(self.td.content2)),
                                                     self.td.filename3: SizeBytes(len(self.td.content3))}
        self.assertEqual("{'picture.jpg': 7, 'sound.mp3': 5, 'animation.gif': 9}", str(unsorted_dict))
        sorted_dict: dict[MediaFile, SizeBytes] = SizeCalculator.sort_by_size_desc(unsorted_dict)
        self.assertEqual("{'animation.gif': 9, 'picture.jpg': 7, 'sound.mp3': 5}", str(sorted_dict))

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
