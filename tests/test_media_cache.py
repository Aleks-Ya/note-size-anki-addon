import tempfile
import timeit
import unittest

from anki.collection import Collection
from anki.notes import Note

from note_size.media_cache import MediaCache
from note_size.types import SizeBytes
from tests.data import TestData


class MediaCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.media_cache: MediaCache = MediaCache(self.col)
        self.td: TestData = TestData()

    def test_get_file_size(self):
        self.note: Note = self.td.create_note_with_files(self.col)
        act_file_size_1: SizeBytes = self.media_cache.get_file_size(self.td.filename1, use_cache=False)
        exp_file_size_1: SizeBytes = SizeBytes(len(self.td.content1))
        self.assertEqual(exp_file_size_1, act_file_size_1)

    def test_get_file_size_cached(self):
        self.td.create_note_with_files(self.col)
        execution_time: float = timeit.timeit(
            lambda: self.media_cache.get_file_size(self.td.filename1, use_cache=True), number=1_000_000)
        self.assertLessEqual(execution_time, 1)

    def test_get_total_size(self):
        self.note: Note = self.td.create_note_with_files(self.col)
        self.media_cache.get_file_size(self.td.filename1, use_cache=True)
        self.media_cache.get_file_size(self.td.filename2, use_cache=True)
        self.media_cache.get_file_size(self.td.filename2, use_cache=True)  # check for duplicating
        act_total_size: SizeBytes = self.media_cache.get_total_size()
        exp_total_size: SizeBytes = SizeBytes(len(self.td.content1) + len(self.td.content2))
        self.assertEqual(exp_total_size, act_total_size)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
