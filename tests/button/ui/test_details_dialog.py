from anki.notes import Note
from aqt.qt import QLabel

from note_size.button.ui.details_dialog import DetailsDialog
from tests.data import Data


def test_show_note(details_dialog: DetailsDialog, td: Data):
    note: Note = td.create_note_with_files()
    details_dialog.show_note(note)
    label: QLabel = details_dialog.findChild(QLabel)
    assert label.text() == 'Total note size: 143 B'
