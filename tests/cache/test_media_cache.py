import tempfile
import timeit
import unittest

from anki.collection import Collection

from note_size.config.config import Config
from note_size.cache.media_cache import MediaCache
from note_size.types import SizeBytes
from tests.data import Data, DefaultFields


class TestMediaCache(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        self.media_cache: MediaCache = MediaCache(self.col, config)
        self.td: Data = Data(self.col)

    def test_get_file_size(self):
        self.td.create_note_with_files()
        act_file_size_1: SizeBytes = self.media_cache.get_file_size(DefaultFields.file0, use_cache=False)
        exp_file_size_1: SizeBytes = SizeBytes(len(DefaultFields.content0))
        self.assertEqual(exp_file_size_1, act_file_size_1)

    def test_get_file_size_cached(self):
        self.td.create_note_with_files()
        execution_time: float = timeit.timeit(
            lambda: self.media_cache.get_file_size(DefaultFields.file0, use_cache=True), number=1_000_000)
        self.assertLessEqual(execution_time, 1)

    def test_get_total_size(self):
        self.td.create_note_with_files()
        self.media_cache.get_file_size(DefaultFields.file0, use_cache=True)
        self.media_cache.get_file_size(DefaultFields.file1, use_cache=True)
        self.media_cache.get_file_size(DefaultFields.file1, use_cache=True)  # check for duplicating
        act_total_size: SizeBytes = self.media_cache.get_total_size()
        exp_total_size: SizeBytes = SizeBytes(len(DefaultFields.content0) + len(DefaultFields.content1))
        self.assertEqual(exp_total_size, act_total_size)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
