from note_size.types import FileSize, SizeBytes


def test_file_size_equals():
    assert FileSize(SizeBytes(10)) == FileSize(SizeBytes(10))
