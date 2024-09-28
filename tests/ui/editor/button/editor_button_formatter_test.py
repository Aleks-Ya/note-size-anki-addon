from anki.collection import Collection
from anki.notes import Note

from note_size.cache.size_str_cache import SizeStrCache
from note_size.calculator.size_formatter import SizeFormatter
from note_size.config.config import Config
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.config.level_parser import LevelParser
from note_size.ui.editor.button.editor_button_formatter import EditorButtonFormatter
from note_size.ui.editor.button.editor_button_label import EditorButtonLabel
from note_size.types import SizeBytes, SizeType
from tests.data import Data


def test_get_zero_size_label(editor_button_formatter: EditorButtonFormatter):
    label: EditorButtonLabel = editor_button_formatter.get_zero_size_label()
    assert label == EditorButtonLabel("0 B", "PaleGreen")


def test_get_add_mode_label(td: Data, editor_button_formatter: EditorButtonFormatter):
    note: Note = td.create_note_with_files()
    label: EditorButtonLabel = editor_button_formatter.get_add_mode_label(note)
    assert label == EditorButtonLabel("143 B", "PaleGreen")


def test_get_edit_mode_label(td: Data, editor_button_formatter: EditorButtonFormatter, size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    label: EditorButtonLabel = editor_button_formatter.get_edit_mode_label(note.id)
    assert size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=False) == SizeBytes(143)
    assert label == EditorButtonLabel("143 B", "PaleGreen")


def test_get_edit_mode_label_no_cache(col: Collection, td: Data, editor_button_formatter: EditorButtonFormatter,
                                      size_calculator: SizeCalculator):
    note: Note = td.create_note_with_files()
    label: EditorButtonLabel = editor_button_formatter.get_edit_mode_label(note.id)
    assert size_calculator.calculate_note_size(note, SizeType.TOTAL, use_cache=False) == SizeBytes(143)
    assert label == EditorButtonLabel("143 B", "PaleGreen")
    Data.update_front_field(note, 'updated')
    assert size_calculator.calculate_note_size(col.get_note(note.id), SizeType.TOTAL, use_cache=False) == SizeBytes(86)
    assert editor_button_formatter.get_edit_mode_label(note.id) == EditorButtonLabel("86 B", "PaleGreen")


def test_disabled_color(col: Collection, td: Data, size_formatter: SizeFormatter, level_parser: LevelParser):
    config: Config = td.read_config_updated({'Size Button': {'Color': {'Enabled': False}}})
    media_cache: MediaCache = MediaCache(col, config)
    size_calculator: SizeCalculator = SizeCalculator(col, media_cache)
    size_str_cache: SizeStrCache = SizeStrCache(col, size_calculator, size_formatter)
    editor_button_formatter: EditorButtonFormatter = EditorButtonFormatter(
        size_str_cache, size_calculator, size_formatter, level_parser, config)
    assert editor_button_formatter.get_zero_size_label() == EditorButtonLabel("0 B", "")
    note: Note = td.create_note_with_files()
    assert editor_button_formatter.get_add_mode_label(note) == EditorButtonLabel("143 B", "")
    assert editor_button_formatter.get_edit_mode_label(note.id) == EditorButtonLabel("143 B", "")
