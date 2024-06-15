import tempfile
import timeit
import unittest

from anki.collection import Collection
from anki.notes import Note, NoteId

from note_size import ItemIdCache
from note_size.size_calculator import SizeBytes
from note_size.size_formatter import SizeStr
from tests.data import TestData


class SizeFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.item_id_cache: ItemIdCache = ItemIdCache(self.col)
        self.td: TestData = TestData()
        self.note: Note = self.td.create_note_with_files(self.col)

    def test_get_note_size_no_cache(self):
        exp_size_1: SizeBytes = SizeBytes(len(self.td.front_field_content_with_files.encode()) +
                                          len(self.td.back_field_content_with_files.encode()) +
                                          len(self.td.content1) + len(self.td.content2) + len(self.td.content3))
        note_id: NoteId = self.note.id
        act_size_1: SizeBytes = self.item_id_cache.get_note_size(note_id, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: SizeBytes = self.item_id_cache.get_note_size(note_id, use_cache=False)
        exp_size_2: SizeBytes = SizeBytes(len(content.encode()) + len(self.td.back_field_content_with_files.encode())
                                          + len(self.td.content1) + len(self.td.content3))
        self.assertEqual(exp_size_2, act_size_2)

    def test_get_note_size_use_cache(self):
        exp_size_1: SizeBytes = SizeBytes(len(self.td.front_field_content_with_files.encode()) +
                                          len(self.td.back_field_content_with_files.encode()) +
                                          len(self.td.content1) + len(self.td.content2) + len(self.td.content3))
        note_id: NoteId = self.note.id
        act_size_1: SizeBytes = self.item_id_cache.get_note_size(note_id, use_cache=False)
        self.assertEqual(exp_size_1, act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: SizeBytes = self.item_id_cache.get_note_size(note_id, use_cache=True)
        self.assertEqual(exp_size_1, act_size_2)

    def test_get_note_size_performance_no_cache(self):
        execution_time: float = timeit.timeit(
            lambda: self.item_id_cache.get_note_size(self.note.id, use_cache=False), number=100_000)
        self.assertLessEqual(execution_time, 15)

    def test_get_note_size_performance_use_cache(self):
        execution_time: float = timeit.timeit(
            lambda: self.item_id_cache.get_note_size(self.note.id, use_cache=True), number=100_000)
        self.assertLessEqual(execution_time, 0.5)

    def _run_get_note_size(self, use_cache: bool):
        for _ in range(0, 100_000):
            self.item_id_cache.get_note_size(self.note.id, use_cache=use_cache)

    def test_get_note_size_str_no_cache(self):
        note_id: NoteId = self.note.id
        act_size_1: SizeStr = self.item_id_cache.get_note_size_str(note_id, use_cache=False)
        self.assertEqual("142B", act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: SizeStr = self.item_id_cache.get_note_size_str(note_id, use_cache=False)
        self.assertEqual("85B", act_size_2)

    def test_get_note_size_str_use_cache(self):
        note_id: NoteId = self.note.id
        act_size_1: SizeStr = self.item_id_cache.get_note_size_str(note_id, use_cache=False)
        self.assertEqual("142B", act_size_1)

        content: str = 'updated'
        self.note[self.td.front_field_name] = content
        self.col.update_note(self.note)
        act_size_2: SizeStr = self.item_id_cache.get_note_size_str(note_id, use_cache=True)
        self.assertEqual("142B", act_size_2)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
