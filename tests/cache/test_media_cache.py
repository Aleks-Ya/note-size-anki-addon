import tempfile
import timeit
import unittest

from anki.collection import Collection

from note_size import Config
from note_size.cache.media_cache import MediaCache
from note_size.types import SizeBytes
from tests.data import Data, NoteData


class TestMediaCache(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        self.media_cache: MediaCache = MediaCache(self.col, config)
        self.td: Data = Data(self.col)

    def test_get_file_size(self):
        note_data: NoteData = self.td.create_note_with_files()
        act_file_size_1: SizeBytes = self.media_cache.get_file_size(note_data.files[0], use_cache=False)
        exp_file_size_1: SizeBytes = SizeBytes(len(note_data.file_contents[0]))
        self.assertEqual(exp_file_size_1, act_file_size_1)

    def test_get_file_size_cached(self):
        note_data: NoteData = self.td.create_note_with_files()
        execution_time: float = timeit.timeit(
            lambda: self.media_cache.get_file_size(note_data.files[0], use_cache=True), number=1_000_000)
        self.assertLessEqual(execution_time, 1)

    def test_get_total_size(self):
        note_data: NoteData = self.td.create_note_with_files()
        self.media_cache.get_file_size(note_data.files[0], use_cache=True)
        self.media_cache.get_file_size(note_data.files[1], use_cache=True)
        self.media_cache.get_file_size(note_data.files[1], use_cache=True)  # check for duplicating
        act_total_size: SizeBytes = self.media_cache.get_total_size()
        exp_total_size: SizeBytes = SizeBytes(len(note_data.file_contents[0]) + len(note_data.file_contents[1]))
        self.assertEqual(exp_total_size, act_total_size)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
