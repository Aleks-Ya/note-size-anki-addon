from anki.notes import Note, NoteId

from note_size.calculator.note_helper import NoteHelper
from tests.data import Data


def test_is_note_saved(td: Data):
    saved_note: Note = td.create_note_without_files(new_note=False)
    assert NoteHelper.is_note_saved(saved_note)
    new_note: Note = td.create_note_without_files(new_note=True)
    assert not NoteHelper.is_note_saved(new_note)


def test_is_note_id_saved(td: Data):
    saved_note_id: NoteId = td.create_note_without_files(new_note=False).id
    assert NoteHelper.is_note_id_saved(saved_note_id)
    saved_note_id: NoteId = td.create_note_without_files(new_note=True).id
    assert not NoteHelper.is_note_id_saved(saved_note_id)
