import timeit

import pytest

from note_size.types import FileType, MediaFile
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper
from tests.data import MediaFiles


def test_get_file_type(file_type_helper: FileTypeHelper):
    assert file_type_helper.get_file_type(MediaFiles.image) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.jpg")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.jpglarge")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.jpeg")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.JPEG")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.gif")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.bmp")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.webp")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.svg")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.ashx")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.axd")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.cms")) == FileType.IMAGE
    assert file_type_helper.get_file_type(MediaFile("image.ico")) == FileType.IMAGE

    assert file_type_helper.get_file_type(MediaFile("audio.mp3")) == FileType.AUDIO
    assert file_type_helper.get_file_type(MediaFile("audio.ogg")) == FileType.AUDIO
    assert file_type_helper.get_file_type(MediaFile("audio.wav")) == FileType.AUDIO

    assert file_type_helper.get_file_type(MediaFile("video.mp4")) == FileType.VIDEO
    assert file_type_helper.get_file_type(MediaFile("video.avi")) == FileType.VIDEO
    assert file_type_helper.get_file_type(MediaFiles.video) == FileType.VIDEO

    assert file_type_helper.get_file_type(MediaFile("other")) == FileType.OTHER
    assert file_type_helper.get_file_type(MediaFile("other.json")) == FileType.OTHER
    assert file_type_helper.get_file_type(MediaFile("other.pdf")) == FileType.OTHER
    assert file_type_helper.get_file_type(MediaFile("other.txt")) == FileType.OTHER
    assert file_type_helper.get_file_type(MediaFile("other.css")) == FileType.OTHER
    assert file_type_helper.get_file_type(MediaFile("other.Default")) == FileType.OTHER
    assert file_type_helper.get_file_type(MediaFile("other.js")) == FileType.OTHER


@pytest.mark.performance
def test_get_file_type_performance(file_type_helper: FileTypeHelper):
    execution_time: float = timeit.timeit(lambda: file_type_helper.get_file_type(MediaFiles.image), number=500_000)
    assert execution_time <= 1


def test_get_cache_size(file_type_helper: FileTypeHelper):
    assert file_type_helper.get_cache_size() == 0
    file_type_helper.get_file_type(MediaFiles.image)
    file_type_helper.get_file_type(MediaFile("image.jpg"))
    assert file_type_helper.get_cache_size() == 2
    file_type_helper.get_file_type(MediaFile("image.jpg"))
    assert file_type_helper.get_cache_size() == 2
    file_type_helper.invalidate_cache()
    assert file_type_helper.get_cache_size() == 0
