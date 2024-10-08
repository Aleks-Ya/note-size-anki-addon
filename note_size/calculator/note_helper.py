import logging
from logging import Logger

from anki.notes import Note, NoteId

log: Logger = logging.getLogger(__name__)


class NoteHelper:

    @staticmethod
    def is_note_saved(note: Note) -> bool:
        return note and note.id and note.id != 0

    @staticmethod
    def is_note_id_saved(note_id: NoteId) -> bool:
        return note_id and note_id != 0
