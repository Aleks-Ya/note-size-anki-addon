from anki.collection import Collection
from anki.notes import Note
from aqt.theme import ThemeManager

from note_size.cache.str_note_size_cache import StrNoteSizeCache
from note_size.cache.bytes_size_cache import BytesSizeCache
from note_size.core.common.collection_holder import CollectionHolder
from note_size.config.config import Config
from note_size.cache.media_cache import MediaCache
from note_size.cache.bytes_note_size_cache import BytesNoteSizeCache
from note_size.config.level_parser import LevelParser
from note_size.ui.editor.button.editor_button_formatter import EditorButtonFormatter
from note_size.ui.editor.button.editor_button_label import EditorButtonLabel
from note_size.core.common.types import SizeBytes, SizeType, ColorName
from tests.data import Data, Colors


def test_get_zero_size_label(editor_button_formatter: EditorButtonFormatter):
    label: EditorButtonLabel = editor_button_formatter.get_zero_size_label()
    assert label == EditorButtonLabel("0 B", Colors.pale_green)


def test_get_add_mode_label(td: Data, editor_button_formatter: EditorButtonFormatter):
    note: Note = td.create_note_with_files()
    label: EditorButtonLabel = editor_button_formatter.get_add_mode_label(note)
    assert label == EditorButtonLabel("143 B", Colors.pale_green)


def test_get_edit_mode_label(td: Data, editor_button_formatter: EditorButtonFormatter, bytes_note_size_cache: BytesNoteSizeCache):
    note: Note = td.create_note_with_files()
    label: EditorButtonLabel = editor_button_formatter.get_edit_mode_label(note.id)
    assert bytes_note_size_cache.calculate_note_size(note, SizeType.TOTAL, use_cache=False) == SizeBytes(143)
    assert label == EditorButtonLabel("143 B", Colors.pale_green)


def test_get_edit_mode_label_no_cache(col: Collection, td: Data, editor_button_formatter: EditorButtonFormatter,
                                      bytes_note_size_cache: BytesNoteSizeCache):
    note: Note = td.create_note_with_files()
    label: EditorButtonLabel = editor_button_formatter.get_edit_mode_label(note.id)
    assert bytes_note_size_cache.calculate_note_size(note, SizeType.TOTAL, use_cache=False) == SizeBytes(143)
    assert label == EditorButtonLabel("143 B", Colors.pale_green)
    Data.update_front_field(note, 'updated')
    assert bytes_note_size_cache.calculate_note_size(col.get_note(note.id), SizeType.TOTAL, use_cache=False) == SizeBytes(86)
    assert editor_button_formatter.get_edit_mode_label(note.id) == EditorButtonLabel("86 B", Colors.pale_green)


def test_disabled_color(collection_holder: CollectionHolder, td: Data, bytes_size_cache: BytesSizeCache,
                        level_parser: LevelParser, theme_manager: ThemeManager):
    config: Config = td.read_config_updated({'Size Button': {'Color': {'Enabled': False}}})
    media_cache: MediaCache = MediaCache(collection_holder, config)
    bytes_note_size_cache: BytesNoteSizeCache = BytesNoteSizeCache(collection_holder, media_cache)
    str_note_size_cache: StrNoteSizeCache = StrNoteSizeCache(bytes_note_size_cache, bytes_size_cache)
    editor_button_formatter: EditorButtonFormatter = EditorButtonFormatter(
        str_note_size_cache, bytes_note_size_cache, bytes_size_cache, level_parser, theme_manager, config)
    assert editor_button_formatter.get_zero_size_label() == EditorButtonLabel("0 B", ColorName(""))
    note: Note = td.create_note_with_files()
    assert editor_button_formatter.get_add_mode_label(note) == EditorButtonLabel("143 B", ColorName(""))
    assert editor_button_formatter.get_edit_mode_label(note.id) == EditorButtonLabel("143 B", ColorName(""))
