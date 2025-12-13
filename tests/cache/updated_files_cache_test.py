from anki.notes import Note, NoteId

from note_size.cache.media_cache import MediaCache
from note_size.cache.updated_files_cache import UpdatedFilesCache
from note_size.common.types import FileContent
from tests.data import Data, DefaultFields, MediaFiles, FileContents


def test_get_notes_having_updated_files(updated_files_cache: UpdatedFilesCache, td: Data):
    updated_files_cache.set_initialized(True)
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFiles.picture: FileContents.picture,
            MediaFiles.video: FileContent('video')
        },
        DefaultFields.back_field_name: {
            MediaFiles.sound: FileContents.sound,
            MediaFiles.image: FileContent('image')
        }
    })
    td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFiles.photo: FileContent('photo')
        },
        DefaultFields.back_field_name: {
            MediaFiles.movie: FileContent('movie')
        }
    })
    assert updated_files_cache.get_notes_having_updated_files() == set()
    td.write_file(MediaFiles.picture, "new content")
    updated_notes: set[NoteId] = updated_files_cache.get_notes_having_updated_files()
    assert updated_notes == {note1.id, note2.id}


def test_evict_note(updated_files_cache: UpdatedFilesCache, td: Data):
    updated_files_cache.set_initialized(True)
    assert updated_files_cache.as_dict_list() == [{}]
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFiles.picture: FileContents.picture,
            MediaFiles.video: FileContent('video')
        },
        DefaultFields.back_field_name: {
            MediaFiles.sound: FileContents.sound,
            MediaFiles.image: FileContent('image')
        }
    })
    note3: Note = td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            MediaFiles.photo: FileContent('photo')
        },
        DefaultFields.back_field_name: {
            MediaFiles.movie: FileContent('movie')
        }
    })
    assert updated_files_cache.as_dict_list() == [{}]

    assert updated_files_cache.get_notes_having_updated_files() == set()
    assert updated_files_cache.as_dict_list() == [{}]

    td.write_file(MediaFiles.picture, "new content")
    updated_files_cache.get_notes_having_updated_files()
    assert updated_files_cache.as_dict_list() == [{MediaFiles.animation: {note1.id},
                                                   MediaFiles.image: {note2.id},
                                                   MediaFiles.movie: {note3.id},
                                                   MediaFiles.photo: {note3.id},
                                                   MediaFiles.picture: {note1.id, note2.id},
                                                   MediaFiles.sound: {note1.id, note2.id},
                                                   MediaFiles.video: {note2.id}}]
    updated_files_cache.evict_note(note1.id)
    assert updated_files_cache.as_dict_list() == [{MediaFiles.animation: set(),
                                                   MediaFiles.image: {note2.id},
                                                   MediaFiles.movie: {note3.id},
                                                   MediaFiles.photo: {note3.id},
                                                   MediaFiles.picture: {note2.id},
                                                   MediaFiles.sound: {note2.id},
                                                   MediaFiles.video: {note2.id}}]


def test_initialized(updated_files_cache: UpdatedFilesCache):
    assert not updated_files_cache.is_initialized()
    updated_files_cache.set_initialized(True)
    assert updated_files_cache.is_initialized()
    updated_files_cache.set_initialized(False)
    assert not updated_files_cache.is_initialized()


def test_get_cache_size(updated_files_cache: UpdatedFilesCache, media_cache: MediaCache, td: Data):
    updated_files_cache.set_initialized(True)
    assert updated_files_cache.get_cache_size() == 0
    media_cache.get_file_size(MediaFiles.picture, use_cache=True)
    td.create_note_with_files()
    td.write_file(MediaFiles.picture, "new content")
    updated_files_cache.get_notes_having_updated_files()
    assert updated_files_cache.get_cache_size() == 3
