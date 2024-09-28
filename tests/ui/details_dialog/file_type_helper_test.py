import timeit

import pytest

from note_size.types import FileType
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper


def test_get_file_type(file_type_helper: FileTypeHelper):
    assert file_type_helper.get_file_type("image.png") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.jpg") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.jpglarge") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.jpeg") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.JPEG") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.gif") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.bmp") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.webp") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.svg") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.ashx") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.axd") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.cms") == FileType.IMAGE
    assert file_type_helper.get_file_type("image.ico") == FileType.IMAGE

    assert file_type_helper.get_file_type("audio.mp3") == FileType.AUDIO
    assert file_type_helper.get_file_type("audio.ogg") == FileType.AUDIO
    assert file_type_helper.get_file_type("audio.wav") == FileType.AUDIO

    assert file_type_helper.get_file_type("video.mp4") == FileType.VIDEO
    assert file_type_helper.get_file_type("video.avi") == FileType.VIDEO
    assert file_type_helper.get_file_type("video.mov") == FileType.VIDEO

    assert file_type_helper.get_file_type("other") == FileType.OTHER
    assert file_type_helper.get_file_type("other.json") == FileType.OTHER
    assert file_type_helper.get_file_type("other.pdf") == FileType.OTHER
    assert file_type_helper.get_file_type("other.txt") == FileType.OTHER
    assert file_type_helper.get_file_type("other.css") == FileType.OTHER
    assert file_type_helper.get_file_type("other.Default") == FileType.OTHER
    assert file_type_helper.get_file_type("other.js") == FileType.OTHER


@pytest.mark.performance
def test_get_file_type_performance(file_type_helper: FileTypeHelper):
    execution_time: float = timeit.timeit(lambda: file_type_helper.get_file_type("image.png"), number=500_000)
    assert execution_time <= 1


def test_get_cache_size(file_type_helper: FileTypeHelper):
    assert file_type_helper.get_cache_size() == 0
    file_type_helper.get_file_type("image.png")
    file_type_helper.get_file_type("image.jpg")
    assert file_type_helper.get_cache_size() == 2
    file_type_helper.get_file_type("image.jpg")
    assert file_type_helper.get_cache_size() == 2
    file_type_helper.invalidate_cache()
    assert file_type_helper.get_cache_size() == 0
