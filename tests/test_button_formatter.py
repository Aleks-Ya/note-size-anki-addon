import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note

from note_size import ButtonFormatter, ItemIdCache, SizeCalculator
from note_size.button_formatter import ButtonLabel
from note_size.size_calculator import SizeBytes
from tests.data import TestData


class ButtonFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: TestData = TestData()
        item_id_cache: ItemIdCache = ItemIdCache(self.col)
        self.button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache)

    def test_get_zero_size_label(self):
        label: ButtonLabel = ButtonFormatter.get_zero_size_label()
        self.assertEqual("Size: 0B", label)

    def test_get_add_mode_label(self):
        note: Note = self.td.create_note_with_files(self.col)
        label: ButtonLabel = ButtonFormatter.get_add_mode_label(note)
        self.assertEqual("Size: 129B", label)

    def test_get_edit_mode_label(self):
        note: Note = self.td.create_note_with_files(self.col)
        label: ButtonLabel = self.button_formatter.get_edit_mode_label(note.id)
        self.assertEqual(SizeBytes(129), SizeCalculator.calculate_note_size(note))
        self.assertEqual("Size: 129B", label)

    def test_get_edit_mode_label_no_cache(self):
        note: Note = self.td.create_note_with_files(self.col)
        label: ButtonLabel = self.button_formatter.get_edit_mode_label(note.id)
        self.assertEqual(SizeBytes(129), SizeCalculator.calculate_note_size(note))
        self.assertEqual("Size: 129B", label)
        content: str = 'updated'
        note[self.td.front_field_name] = content
        self.col.update_note(note)
        self.assertEqual(SizeBytes(79), SizeCalculator.calculate_note_size(self.col.get_note(note.id)))
        self.assertEqual("Size: 79B", self.button_formatter.get_edit_mode_label(note.id))

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
