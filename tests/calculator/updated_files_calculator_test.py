from anki.notes import Note, NoteId

from note_size.cache.media_cache import MediaCache
from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.types import MediaFile, FileContent
from tests.data import Data, DefaultFields


def test_get_notes_having_updated_files(updated_files_calculator: UpdatedFilesCalculator, td: Data):
    updated_files_calculator.set_initialized(True)
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            DefaultFields.file0: DefaultFields.content0,
            MediaFile('video.mov'): FileContent('video')
        },
        DefaultFields.back_field_name: {
            DefaultFields.file1: DefaultFields.content1,
            MediaFile('image.png'): FileContent('image')
        }
    })
    td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFile('photo.tiff'): FileContent('photo')
        },
        DefaultFields.back_field_name: {
            MediaFile('movie.mp4'): FileContent('movie')
        }
    })
    assert updated_files_calculator.get_notes_having_updated_files() == set()
    td.write_file(DefaultFields.file0, "new content")
    updated_notes: set[NoteId] = updated_files_calculator.get_notes_having_updated_files()
    assert updated_notes == {note1.id, note2.id}


def test_evict_note(updated_files_calculator: UpdatedFilesCalculator, td: Data):
    updated_files_calculator.set_initialized(True)
    assert updated_files_calculator.as_dict_list() == [{}]
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            DefaultFields.file0: DefaultFields.content0,
            MediaFile('video.mov'): FileContent('video')
        },
        DefaultFields.back_field_name: {
            DefaultFields.file1: DefaultFields.content1,
            MediaFile('image.png'): FileContent('image')
        }
    })
    note3: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFile('photo.tiff'): FileContent('photo')
        },
        DefaultFields.back_field_name: {
            MediaFile('movie.mp4'): FileContent('movie')
        }
    })
    assert updated_files_calculator.as_dict_list() == [{}]

    assert updated_files_calculator.get_notes_having_updated_files() == set()
    assert updated_files_calculator.as_dict_list() == [{}]

    td.write_file(DefaultFields.file0, "new content")
    updated_files_calculator.get_notes_having_updated_files()
    assert updated_files_calculator.as_dict_list() == [{'animation.gif': {note1.id},
                                                        'image.png': {note2.id},
                                                        'movie.mp4': {note3.id},
                                                        'photo.tiff': {note3.id},
                                                        'picture.jpg': {note1.id, note2.id},
                                                        'sound.mp3': {note1.id, note2.id},
                                                        'video.mov': {note2.id}}]
    updated_files_calculator.evict_note(note1.id)
    assert updated_files_calculator.as_dict_list() == [{'animation.gif': set(),
                                                        'image.png': {note2.id},
                                                        'movie.mp4': {note3.id},
                                                        'photo.tiff': {note3.id},
                                                        'picture.jpg': {note2.id},
                                                        'sound.mp3': {note2.id},
                                                        'video.mov': {note2.id}}]


def test_initialized(updated_files_calculator: UpdatedFilesCalculator):
    assert not updated_files_calculator.is_initialized()
    updated_files_calculator.set_initialized(True)
    assert updated_files_calculator.is_initialized()
    updated_files_calculator.set_initialized(False)
    assert not updated_files_calculator.is_initialized()


def test_get_cache_size(updated_files_calculator: UpdatedFilesCalculator, media_cache: MediaCache, td: Data):
    updated_files_calculator.set_initialized(True)
    assert updated_files_calculator.get_cache_size() == 0
    media_cache.get_file_size(DefaultFields.file0, use_cache=True)
    td.create_note_with_files()
    td.write_file(DefaultFields.file0, "new content")
    updated_files_calculator.get_notes_having_updated_files()
    assert updated_files_calculator.get_cache_size() == 3
