from anki.notes import Note

from note_size.common.types import SizeBytes, FileSize
from note_size.ui.details_dialog.details_model import DetailsModel
from note_size.ui.details_dialog.details_model_filler import DetailsModelFiller
from tests.data import Data, MediaFiles


def test_prepare_note_model(details_model_filler: DetailsModelFiller, td: Data):
    note: Note = td.create_note_with_files()
    model: DetailsModel = details_model_filler.prepare_note_model(note)
    assert model.total_note_size_text == 'Total note size: 143 B'
    assert model.texts_note_size_text == 'Texts size: 122 B'
    assert model.files_note_size_text == 'Size of 3 files (3 existing and 0 missing): 21 B'
    assert model.file_sizes == {MediaFiles.animation: FileSize(SizeBytes(9)),
                                MediaFiles.picture: FileSize(SizeBytes(7)),
                                MediaFiles.sound: FileSize(SizeBytes(5))}
