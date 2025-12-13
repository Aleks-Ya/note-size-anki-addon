from note_size.core.cache.bytes_note_size_cache import BytesNoteSizeCache
from tests.conftest import bytes_note_size_cache


def test_cache_id(bytes_note_size_cache: BytesNoteSizeCache):
    assert bytes_note_size_cache.cache_id() == "BytesNoteSizeCache"
