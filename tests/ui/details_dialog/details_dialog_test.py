from anki.notes import Note
from aqt.qt import QLabel
from PyQtPath.path_chain_pyqt6 import path

from note_size.ui.details_dialog.details_dialog import DetailsDialog
from note_size.ui.details_dialog.files_table import FilesTable
from tests.data import Data


def test_show_note(details_dialog: DetailsDialog, td: Data):
    note: Note = td.create_note_with_files()
    details_dialog.show_note(note)
    label: QLabel = details_dialog.findChild(QLabel)
    assert label.text() == 'Total note size: 143 B'


def test_show_note_without_files(details_dialog: DetailsDialog, td: Data):
    note_without_file: Note = td.create_note_without_files()
    details_dialog.show_note(note_without_file)
    assert path(details_dialog).label(0).get().text() == 'Total note size: 70 B'
    assert path(details_dialog).label(1).get().text() == 'Texts size: 70 B'
    assert path(details_dialog).label(2).get().text() == 'Size of 0 files (0 existing and 0 missing): 0 B'
    files_table: FilesTable = path(details_dialog).table().get()
    assert files_table.rowCount() == 0
    assert files_table.isHidden()

    note_with_file: Note = td.create_note_with_files()
    details_dialog.show_note(note_with_file)
    assert path(details_dialog).label(0).get().text() == 'Total note size: 143 B'
    assert path(details_dialog).label(1).get().text() == 'Texts size: 122 B'
    assert path(details_dialog).label(2).get().text() == 'Size of 3 files (3 existing and 0 missing): 21 B'
    files_table: FilesTable = path(details_dialog).table().get()
    assert files_table.rowCount() == 3
    assert not files_table.isHidden()

    details_dialog.show_note(note_without_file)
    assert path(details_dialog).label(0).get().text() == 'Total note size: 70 B'
    assert path(details_dialog).label(1).get().text() == 'Texts size: 70 B'
    assert path(details_dialog).label(2).get().text() == 'Size of 0 files (0 existing and 0 missing): 0 B'
    files_table: FilesTable = path(details_dialog).table().get()
    assert files_table.rowCount() == 0
    assert files_table.isHidden()
