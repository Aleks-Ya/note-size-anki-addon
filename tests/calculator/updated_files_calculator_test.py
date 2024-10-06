from anki.notes import Note, NoteId

from note_size.cache.media_cache import MediaCache
from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.types import MediaFile, FileContent
from tests.data import Data, DefaultFields, FileNames, MediaFiles, FileContents


def test_get_notes_having_updated_files(updated_files_calculator: UpdatedFilesCalculator, td: Data):
    updated_files_calculator.set_initialized(True)
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFiles.picture: FileContents.picture,
            MediaFile(FileNames.video): FileContent('video')
        },
        DefaultFields.back_field_name: {
            MediaFiles.sound: FileContents.sound,
            MediaFile(FileNames.image): FileContent('image')
        }
    })
    td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFile(FileNames.photo): FileContent('photo')
        },
        DefaultFields.back_field_name: {
            MediaFile(FileNames.movie): FileContent('movie')
        }
    })
    assert updated_files_calculator.get_notes_having_updated_files() == set()
    td.write_file(MediaFiles.picture, "new content")
    updated_notes: set[NoteId] = updated_files_calculator.get_notes_having_updated_files()
    assert updated_notes == {note1.id, note2.id}


def test_evict_note(updated_files_calculator: UpdatedFilesCalculator, td: Data):
    updated_files_calculator.set_initialized(True)
    assert updated_files_calculator.as_dict_list() == [{}]
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFiles.picture: FileContents.picture,
            MediaFile(FileNames.video): FileContent('video')
        },
        DefaultFields.back_field_name: {
            MediaFiles.sound: FileContents.sound,
            MediaFile(FileNames.image): FileContent('image')
        }
    })
    note3: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFile(FileNames.photo): FileContent('photo')
        },
        DefaultFields.back_field_name: {
            MediaFile(FileNames.movie): FileContent('movie')
        }
    })
    assert updated_files_calculator.as_dict_list() == [{}]

    assert updated_files_calculator.get_notes_having_updated_files() == set()
    assert updated_files_calculator.as_dict_list() == [{}]

    td.write_file(MediaFiles.picture, "new content")
    updated_files_calculator.get_notes_having_updated_files()
    assert updated_files_calculator.as_dict_list() == [{FileNames.animation: {note1.id},
                                                        FileNames.image: {note2.id},
                                                        FileNames.movie: {note3.id},
                                                        FileNames.photo: {note3.id},
                                                        FileNames.picture: {note1.id, note2.id},
                                                        FileNames.sound: {note1.id, note2.id},
                                                        FileNames.video: {note2.id}}]
    updated_files_calculator.evict_note(note1.id)
    assert updated_files_calculator.as_dict_list() == [{FileNames.animation: set(),
                                                        FileNames.image: {note2.id},
                                                        FileNames.movie: {note3.id},
                                                        FileNames.photo: {note3.id},
                                                        FileNames.picture: {note2.id},
                                                        FileNames.sound: {note2.id},
                                                        FileNames.video: {note2.id}}]


def test_initialized(updated_files_calculator: UpdatedFilesCalculator):
    assert not updated_files_calculator.is_initialized()
    updated_files_calculator.set_initialized(True)
    assert updated_files_calculator.is_initialized()
    updated_files_calculator.set_initialized(False)
    assert not updated_files_calculator.is_initialized()


def test_get_cache_size(updated_files_calculator: UpdatedFilesCalculator, media_cache: MediaCache, td: Data):
    updated_files_calculator.set_initialized(True)
    assert updated_files_calculator.get_cache_size() == 0
    media_cache.get_file_size(MediaFiles.picture, use_cache=True)
    td.create_note_with_files()
    td.write_file(MediaFiles.picture, "new content")
    updated_files_calculator.get_notes_having_updated_files()
    assert updated_files_calculator.get_cache_size() == 3
