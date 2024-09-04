from anki.collection import Collection
from anki.notes import Note

from note_size.button.button_label import ButtonLabel
from note_size.config.config import Config
from note_size.button.button_formatter import ButtonFormatter
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.config.settings import Settings
from note_size.types import SizeBytes
from tests.data import Data


def test_get_zero_size_label(button_formatter: ButtonFormatter):
    label: ButtonLabel = button_formatter.get_zero_size_label()
    assert label == ButtonLabel("0 B", "PaleGreen")


def test_get_add_mode_label(td: Data, button_formatter: ButtonFormatter):
    note: Note = td.create_note_with_files()
    label: ButtonLabel = button_formatter.get_add_mode_label(note)
    assert label == ButtonLabel("143 B", "PaleGreen")


def test_get_edit_mode_label(td: Data, button_formatter: ButtonFormatter, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    label: ButtonLabel = button_formatter.get_edit_mode_label(note.id)
    assert size_calculator.calculate_note_size(note, use_cache=False) == SizeBytes(143)
    assert label == ButtonLabel("143 B", "PaleGreen")


def test_get_edit_mode_label_no_cache(col: Collection, td: Data, button_formatter: ButtonFormatter,
                                      size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    label: ButtonLabel = button_formatter.get_edit_mode_label(note.id)
    assert size_calculator.calculate_note_size(note, use_cache=False) == SizeBytes(143)
    assert label == ButtonLabel("143 B", "PaleGreen")
    Data.update_front_field(note, 'updated')
    assert size_calculator.calculate_note_size(col.get_note(note.id), use_cache=False) == SizeBytes(86)
    assert button_formatter.get_edit_mode_label(note.id) == ButtonLabel("86 B", "PaleGreen")


def test_disabled_color(col: Collection, td: Data, settings: Settings, media_cache: MediaCache):
    config: Config = td.read_config_updated({'Size Button': {'Color': {'Enabled': False}}})
    media_cache: MediaCache = MediaCache(col, config)
    size_calculator = SizeCalculator(col, media_cache)
    item_id_cache: ItemIdCache = ItemIdCache(col, size_calculator, media_cache, config, settings)
    button_formatter = ButtonFormatter(item_id_cache, size_calculator, config)
    assert button_formatter.get_zero_size_label() == ButtonLabel("0 B", "")
    note: Note = td.create_note_with_files()
    assert button_formatter.get_add_mode_label(note) == ButtonLabel("143 B", "")
    assert button_formatter.get_edit_mode_label(note.id) == ButtonLabel("143 B", "")
