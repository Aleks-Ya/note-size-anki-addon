import tempfile
import timeit
import unittest

from anki.collection import Collection
from anki.notes import NoteId, Note

from note_size.config.config import Config
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, SizeStr, SizeType
from tests.data import Data, DefaultFields


class TestItemIdCache(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        self.item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        self.td: Data = Data(self.col)

    def test_get_note_size_bytes_no_cache(self):
        exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                          len(DefaultFields.back_field_content.encode()) +
                                          len(DefaultFields.content0) + len(DefaultFields.content1) +
                                          len(DefaultFields.content2))
        note: Note = self.td.create_note_with_files()
        note_id: NoteId = note.id
        act_size_1: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        content: str = 'updated'
        Data.update_front_field(note, content)
        act_size_2: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
        exp_size_2: SizeBytes = SizeBytes(len(content.encode()) +
                                          len(DefaultFields.back_field_content.encode()) +
                                          len(DefaultFields.content0) +
                                          len(DefaultFields.content2))
        self.assertEqual(exp_size_2, act_size_2)

    def test_get_note_size_bytes_use_cache(self):
        exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                          len(DefaultFields.back_field_content.encode()) +
                                          len(DefaultFields.content0) +
                                          len(DefaultFields.content1) +
                                          len(DefaultFields.content2))
        note: Note = self.td.create_note_with_files()
        note_id: NoteId = note.id
        act_size_1: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        Data.update_front_field(note, 'updated')
        act_size_2: SizeBytes = self.item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=True)
        self.assertEqual(exp_size_1, act_size_2)

    def test_get_note_size_bytes_performance(self):
        note: Note = self.td.create_note_with_files()
        execution_time: float = timeit.timeit(
            lambda: self.item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True),
            number=1_000_000)
        self.assertLessEqual(execution_time, 1)

    def test_get_note_size_str_no_cache(self):
        note: Note = self.td.create_note_with_files()
        note_id: NoteId = note.id
        act_size_1: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual("143 B", act_size_1)

        Data.update_front_field(note, 'updated')
        act_size_2: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual("86 B", act_size_2)

    def test_get_note_size_str_use_cache(self):
        note: Note = self.td.create_note_with_files()
        note_id: NoteId = note.id
        act_size_1: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
        self.assertEqual("143 B", act_size_1)

        Data.update_front_field(note, 'updated')
        act_size_2: SizeStr = self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True)
        self.assertEqual("143 B", act_size_2)

    def test_get_total_texts_size(self):
        self.assertEqual(SizeBytes(0), self.item_id_cache.get_total_texts_size())

        note1: Note = self.td.create_note_with_files()
        size1: SizeBytes = self.item_id_cache.get_note_size_bytes(note1.id, SizeType.TEXTS, use_cache=True)
        self.assertEqual(size1, self.item_id_cache.get_total_texts_size())

        note2: Note = self.td.create_note_without_files()
        size2: SizeBytes = self.item_id_cache.get_note_size_bytes(note2.id, SizeType.TEXTS, use_cache=True)
        self.assertEqual(size1 + size2, self.item_id_cache.get_total_texts_size())

    def test_evict_note(self):
        self.assertEqual(SizeBytes(0), self.item_id_cache.get_total_texts_size())

        note1: Note = self.td.create_note_with_files()
        size1: SizeBytes = self.item_id_cache.get_note_size_bytes(note1.id, SizeType.TEXTS, use_cache=True)
        self.assertEqual(size1, self.item_id_cache.get_total_texts_size())

        note2: Note = self.td.create_note_without_files()
        size2: SizeBytes = self.item_id_cache.get_note_size_bytes(note2.id, SizeType.TEXTS, use_cache=True)
        self.assertEqual(size1 + size2, self.item_id_cache.get_total_texts_size())

        self.item_id_cache.evict_note(note1.id)
        self.assertEqual(size2, self.item_id_cache.get_total_texts_size())

    def test_refresh_note(self):
        note: Note = self.td.create_note_with_files()
        note_id: NoteId = note.id
        self.assertEqual("143 B", self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True))

        Data.update_front_field(note, 'updated')
        self.assertEqual("143 B", self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True))

        self.item_id_cache.refresh_note(note_id)
        self.assertEqual("86 B", self.item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True))

    def test_is_initialized(self):
        self.assertFalse(self.item_id_cache.is_initialized())
        self.item_id_cache.warm_up_cache()
        self.assertTrue(self.item_id_cache.is_initialized())

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
