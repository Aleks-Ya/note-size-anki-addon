from note_size.calculator.used_files_calculator import UsedFilesCalculator, UsedFiles
from note_size.common.types import MediaFile, FileContent, NotesNumber, FilesNumber, SizeBytes
from tests.data import Data, DefaultFields, MediaFiles


def test_get_used_files_size(td: Data, used_files_calculator: UsedFilesCalculator):
    assert used_files_calculator.get_used_files_size(use_cache=True) == UsedFiles(
        SizeBytes(0), FilesNumber(0), FilesNumber(0), FilesNumber(0), NotesNumber(0))
    media_file_1: MediaFile = MediaFiles.picture
    media_file_2: MediaFile = MediaFiles.sound
    media_file_3: MediaFile = MediaFiles.animation
    content_1: FileContent = FileContent('picture')
    content_2: FileContent = FileContent('sound')
    content_3: FileContent = FileContent('animation')
    content_length_1: int = len(content_1.encode()) + len(content_2.encode()) + len(content_3.encode())
    td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            media_file_1: content_1,
            media_file_2: content_2
        },
        DefaultFields.back_field_name: {
            media_file_1: content_1,
            media_file_3: content_3
        }
    })
    assert used_files_calculator.get_used_files_size(use_cache=True) == UsedFiles(
        SizeBytes(content_length_1), FilesNumber(3), FilesNumber(3), FilesNumber(0), NotesNumber(1))

    media_file_4: MediaFile = MediaFile('video.mp4')
    content_4: FileContent = FileContent('video')
    td.create_note_with_given_files({
        DefaultFields.front_field_name: {
            media_file_1: content_1
        },
        DefaultFields.back_field_name: {
            media_file_4: content_4
        }
    })
    content_length_2: int = content_length_1 + len(content_4.encode())
    assert used_files_calculator.get_used_files_size(use_cache=True) == UsedFiles(
        SizeBytes(content_length_2), FilesNumber(4), FilesNumber(4), FilesNumber(0), NotesNumber(2))
