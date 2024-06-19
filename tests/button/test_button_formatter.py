import tempfile
import unittest

from anki.collection import Collection

from note_size import Config
from note_size.button.button_formatter import ButtonFormatter
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes, ButtonLabel
from tests.data import Data, NoteData


class TestButtonFormatter(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: Data = Data(self.col)
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        self.size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, self.size_calculator, config)
        self.button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, self.size_calculator)

    def test_get_zero_size_label(self):
        label: ButtonLabel = ButtonFormatter.get_zero_size_label()
        self.assertEqual("Size: 0B", label)

    def test_get_add_mode_label(self):
        note_data: NoteData = self.td.create_note_with_files()
        label: ButtonLabel = self.button_formatter.get_add_mode_label(note_data.note)
        self.assertEqual("Size: 142B", label)

    def test_get_edit_mode_label(self):
        note_data: NoteData = self.td.create_note_with_files()
        label: ButtonLabel = self.button_formatter.get_edit_mode_label(note_data.note.id)
        self.assertEqual(SizeBytes(142), self.size_calculator.calculate_note_size(note_data.note))
        self.assertEqual("Size: 142B", label)

    def test_get_edit_mode_label_no_cache(self):
        note_data: NoteData = self.td.create_note_with_files()
        label: ButtonLabel = self.button_formatter.get_edit_mode_label(note_data.note.id)
        self.assertEqual(SizeBytes(142), self.size_calculator.calculate_note_size(note_data.note))
        self.assertEqual("Size: 142B", label)
        Data.update_front_field(note_data.note, 'updated')
        self.assertEqual(SizeBytes(85), self.size_calculator.calculate_note_size(self.col.get_note(note_data.note.id)))
        self.assertEqual("Size: 85B", self.button_formatter.get_edit_mode_label(note_data.note.id))

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
