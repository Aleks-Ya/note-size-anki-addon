import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note

from note_size.button.button_label import ButtonLabel
from note_size.config.config import Config
from note_size.button.button_formatter import ButtonFormatter
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeBytes
from tests.data import Data


class TestButtonFormatter(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: Data = Data(self.col)
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        self.size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, self.size_calculator, config)
        self.button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, self.size_calculator, config)

    def test_get_zero_size_label(self):
        label: ButtonLabel = self.button_formatter.get_zero_size_label()
        self.assertEqual(ButtonLabel("0 B", "PaleGreen"), label)

    def test_get_add_mode_label(self):
        note: Note = self.td.create_note_with_files()
        label: ButtonLabel = self.button_formatter.get_add_mode_label(note)
        self.assertEqual(ButtonLabel("143 B", "PaleGreen"), label)

    def test_get_edit_mode_label(self):
        note: Note = self.td.create_note_with_files()
        label: ButtonLabel = self.button_formatter.get_edit_mode_label(note.id)
        self.assertEqual(SizeBytes(143), self.size_calculator.calculate_note_size(note, use_cache=False))
        self.assertEqual(ButtonLabel("143 B", "PaleGreen"), label)

    def test_get_edit_mode_label_no_cache(self):
        note: Note = self.td.create_note_with_files()
        label: ButtonLabel = self.button_formatter.get_edit_mode_label(note.id)
        self.assertEqual(SizeBytes(143), self.size_calculator.calculate_note_size(note, use_cache=False))
        self.assertEqual(ButtonLabel("143 B", "PaleGreen"), label)
        Data.update_front_field(note, 'updated')
        self.assertEqual(SizeBytes(86), self.size_calculator.calculate_note_size(self.col.get_note(note.id),
                                                                                 use_cache=False))
        self.assertEqual(ButtonLabel("86 B", "PaleGreen"), self.button_formatter.get_edit_mode_label(note.id))

    def test_disabled_color(self):
        config: Config = Data.read_config_updated({'Size Button': {'Color': {'Enabled': False}}})
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, size_calculator, config)
        self.assertEqual(ButtonLabel("0 B", ""), button_formatter.get_zero_size_label())
        note: Note = self.td.create_note_with_files()
        self.assertEqual(ButtonLabel("143 B", ""), button_formatter.get_add_mode_label(note))
        self.assertEqual(ButtonLabel("143 B", ""), button_formatter.get_edit_mode_label(note.id))

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
