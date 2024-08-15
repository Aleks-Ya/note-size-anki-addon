import pytest
from anki.notes import Note
from pytestqt.qtbot import QtBot

from note_size.button.ui.details_dialog import DetailsDialog
from note_size.types import MediaFile
from tests.data import Data


@pytest.mark.skip(reason="For manual running")
def test_details_dialog_wide(details_dialog: DetailsDialog, td: Data, qtbot: QtBot):
    note: Note = td.create_note_with_files()
    media_file: MediaFile = MediaFile(
        "100_symbols_long_long_long_long_long_long_long_long_long_long_long_long_long_long_long_long_long.png")
    td.write_file(media_file, "abc")
    td.append_front_field(note, f'<img src="{media_file}">')
    details_dialog.show_note(note)
    qtbot.wait_for_window_shown(details_dialog)
    qtbot.stop()


@pytest.mark.skip(reason="For manual running")
def test_details_dialog_narrow(details_dialog: DetailsDialog, td: Data, qtbot: QtBot):
    note: Note = td.create_note_with_files()
    details_dialog.show_note(note)
    qtbot.wait_for_window_shown(details_dialog)
    qtbot.stop()


@pytest.mark.skip(reason="For manual running")
def test_details_dialog_no_files(details_dialog: DetailsDialog, td: Data, qtbot: QtBot):
    note: Note = td.create_note_without_files()
    details_dialog.show_note(note)
    qtbot.wait_for_window_shown(details_dialog)
    qtbot.stop()


@pytest.mark.skip(reason="For manual running")
def test_details_dialog_wider_than_screen(details_dialog: DetailsDialog, td: Data, qtbot: QtBot):
    note: Note = td.create_note_with_files()
    length: int = 250
    media_file: MediaFile = MediaFile("a" * (length - 4) + ".png")
    td.write_file(media_file, "abc")
    td.append_front_field(note, f'<img src="{media_file}">')
    details_dialog.show_note(note)
    qtbot.wait_for_window_shown(details_dialog)
    qtbot.stop()


@pytest.mark.skip(reason="For manual running")
def test_details_dialog_higher_than_screen(details_dialog: DetailsDialog, td: Data, qtbot: QtBot):
    note: Note = td.create_note_with_files()
    file_number: int = 50
    for i in range(file_number):
        media_file: MediaFile = MediaFile(f"file-{i}.png")
        td.write_file(media_file, "aa" * i)
        td.append_front_field(note, f'<img src="{media_file}">')
    details_dialog.show_note(note)
    qtbot.wait_for_window_shown(details_dialog)
    qtbot.stop()

@pytest.mark.skip(reason="For manual running")
def test_details_dialog_larger_than_screen(details_dialog: DetailsDialog, td: Data, qtbot: QtBot):
    note: Note = td.create_note_with_files()
    file_number: int = 50
    length: int = 230
    for i in range(file_number):
        media_file: MediaFile = MediaFile(str(i) + "a" * length + ".png")
        td.write_file(media_file, "aa" * i)
        td.append_front_field(note, f'<img src="{media_file}">')
    details_dialog.show_note(note)
    qtbot.wait_for_window_shown(details_dialog)
    qtbot.stop()