import tempfile
import timeit
import unittest

from anki.collection import Collection
from anki.notes import Note, NoteId

from note_size import Config
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, SizeStr, SizeType
from tests.data import Data


class ItemIdCacheTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        self.item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        self.td: Data = Data(self.col)
        self.note: Note = self.td.create_note_with_files()

    def test_get_note_size_bytes_no_cache(self):
        exp_size_1: SizeBytes = SizeBytes(len(Data.front_field_content_with_files.encode()) +
                                          len(Data.back_field_content_with_files.encode()) +
                                          len(Data.content1) + len(Data.content2) + len(Data.content3))
        note_id: NoteId = self.note.id
        act_size_1: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        content: str = 'updated'
        Data.update_front_field(self.note, content)
        act_size_2: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
        exp_size_2: SizeBytes = SizeBytes(len(content.encode()) + len(Data.back_field_content_with_files.encode())
                                          + len(Data.content1) + len(Data.content3))
        self.assertEqual(exp_size_2, act_size_2)

    def test_get_note_size_bytes_use_cache(self):
        exp_size_1: SizeBytes = SizeBytes(len(Data.front_field_content_with_files.encode()) +
                                          len(Data.back_field_content_with_files.encode()) +
                                          len(Data.content1) + len(Data.content2) + len(Data.content3))
        note_id: NoteId = self.note.id
        act_size_1: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        Data.update_front_field(self.note, 'updated')
        act_size_2: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=True)
        self.assertEqual(exp_size_1, act_size_2)

    def test_get_note_size_bytes_performance(self):
        execution_time: float = timeit.timeit(
            lambda: self.item_id_cache.get_note_size_bytes(self.note.id, SizeType.TOTAL, use_cache=True),
            number=1_000_000)
        self.assertLessEqual(execution_time, 1)

    def test_get_note_size_str_no_cache(self):
        note_id: NoteId = self.note.id
        act_size_1: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual("142B", act_size_1)

        Data.update_front_field(self.note, 'updated')
        act_size_2: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual("85B", act_size_2)

    def test_get_note_size_str_use_cache(self):
        note_id: NoteId = self.note.id
        act_size_1: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual("142B", act_size_1)

        Data.update_front_field(self.note, 'updated')
        act_size_2: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True)
        self.assertEqual("142B", act_size_2)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
