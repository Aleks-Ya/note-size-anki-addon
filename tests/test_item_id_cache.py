import tempfile
import time
import unittest

from anki.collection import Collection
from anki.notes import Note, NoteId

from note_size import ItemIdCache
from note_size.size_formatter import SizeStr
from tests.data import TestData


class SizeFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.size_item_id_cache: ItemIdCache = ItemIdCache(self.col)
        self.td: TestData = TestData()
        self.note: Note = self.td.create_note_with_files(self.col)

    def test_get_note_size_no_cache(self):
        exp_size_1: int = (len(self.td.front_field_content_with_files) + len(self.td.back_field_content_with_files)
                           + len(self.td.content1) + len(self.td.content2) + len(self.td.content3))
        note_id: NoteId = self.note.id
        act_size_1: int = self.size_item_id_cache.get_note_size(note_id, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: int = self.size_item_id_cache.get_note_size(note_id, use_cache=False)
        exp_size_2: int = (len(content) + len(self.td.back_field_content_with_files)
                           + len(self.td.content1) + len(self.td.content3))
        self.assertEqual(exp_size_2, act_size_2)

    def test_get_note_size_use_cache(self):
        exp_size_1: int = (len(self.td.front_field_content_with_files) + len(self.td.back_field_content_with_files)
                           + len(self.td.content1) + len(self.td.content2) + len(self.td.content3))
        note_id: NoteId = self.note.id
        act_size_1: int = self.size_item_id_cache.get_note_size(note_id, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: int = self.size_item_id_cache.get_note_size(note_id, use_cache=True)
        self.assertEqual(exp_size_1, act_size_2)

    def test_get_note_size_performance_no_cache(self):
        start_time: float = time.time()
        for _ in range(0, 100_000):
            self.size_item_id_cache.get_note_size(self.note.id, use_cache=False)
        end_time: float = time.time()
        duration_sec: float = end_time - start_time
        self.assertLessEqual(duration_sec, 8)

    def test_get_note_size_performance_use_cache(self):
        start_time: float = time.time()
        for _ in range(0, 100_000):
            self.size_item_id_cache.get_note_size(self.note.id, use_cache=True)
        end_time: float = time.time()
        duration_sec: float = end_time - start_time
        self.assertLessEqual(duration_sec, 0.5)

    def test_get_note_human_str_no_cache(self):
        note_id: NoteId = self.note.id
        act_size_1: SizeStr = self.size_item_id_cache.get_note_human_str(note_id, use_cache=False)
        self.assertEqual("129B", act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: SizeStr = self.size_item_id_cache.get_note_human_str(note_id, use_cache=False)
        self.assertEqual("79B", act_size_2)

    def test_get_note_human_str_use_cache(self):
        note_id: NoteId = self.note.id
        act_size_1: SizeStr = self.size_item_id_cache.get_note_human_str(note_id, use_cache=False)
        self.assertEqual("129B", act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: SizeStr = self.size_item_id_cache.get_note_human_str(note_id, use_cache=True)
        self.assertEqual("129B", act_size_2)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
