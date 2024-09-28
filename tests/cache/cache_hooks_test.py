from pathlib import Path

import pytest
from anki.collection import Collection
from anki import hooks
from anki.errors import NotFoundError
from anki.notes import Note
from aqt import gui_hooks

from note_size.cache.cache_hooks import CacheHooks
from note_size.cache.cache_initializer import CacheInitializer
from note_size.cache.file_note_id_cache import FileNoteIdCache
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeType, MediaFile
from tests.data import Data


@pytest.fixture
def cache_hooks(media_cache: MediaCache, size_calculator: SizeCalculator, item_id_cache: ItemIdCache,
                cache_initializer: CacheInitializer, file_note_id_cache: FileNoteIdCache) -> CacheHooks:
    cache_hooks = CacheHooks(media_cache, item_id_cache, size_calculator, cache_initializer, file_note_id_cache)
    yield cache_hooks
    cache_hooks.remove_hooks()


def test_setup_hooks(cache_hooks: CacheHooks):
    assert gui_hooks.add_cards_did_add_note.count() == 0
    assert hooks.notes_will_be_deleted.count() == 0
    assert gui_hooks.media_sync_did_start_or_stop.count() == 0
    assert hooks.note_will_flush.count() == 0
    assert gui_hooks.profile_did_open.count() == 0
    assert gui_hooks.profile_will_close.count() == 1
    cache_hooks.setup_hooks()
    assert gui_hooks.add_cards_did_add_note.count() == 1
    assert hooks.notes_will_be_deleted.count() == 1
    assert gui_hooks.media_sync_did_start_or_stop.count() == 1
    assert hooks.note_will_flush.count() == 1
    assert gui_hooks.profile_did_open.count() == 1
    assert gui_hooks.profile_will_close.count() == 2
    cache_hooks.remove_hooks()
    assert gui_hooks.add_cards_did_add_note.count() == 0
    assert hooks.notes_will_be_deleted.count() == 0
    assert gui_hooks.media_sync_did_start_or_stop.count() == 0
    assert hooks.note_will_flush.count() == 0
    assert gui_hooks.profile_did_open.count() == 0
    assert gui_hooks.profile_will_close.count() == 1


def test_add_cards_did_add_note(td: Data, cache_hooks: CacheHooks, item_id_cache: ItemIdCache,
                                size_calculator: SizeCalculator):
    cache_hooks.setup_hooks()
    note: Note = td.create_note_with_files()
    assert size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True) == 143


@pytest.mark.skip("TODO fix it")
def test_notes_will_be_deleted(col: Collection, td: Data, cache_hooks: CacheHooks, item_id_cache: ItemIdCache,
                               size_calculator: SizeCalculator):
    cache_hooks.setup_hooks()
    note: Note = td.create_note_with_files()
    assert size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True) == 143
    col.remove_notes([note.id])
    with pytest.raises(NotFoundError):
        size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)


@pytest.mark.skip("TODO fix it")
def test_media_sync_did_start_or_stop(col: Collection, td: Data, cache_hooks: CacheHooks, media_cache: MediaCache,
                                      item_id_cache: ItemIdCache):
    cache_hooks.setup_hooks()
    td.create_note_with_files()
    filename: str = "image.png"
    assert media_cache.get_file_size(MediaFile(filename), use_cache=True) == 0
    content: str = "abc"
    Path(col.media.dir(), "image.png").write_text(content)
    assert media_cache.get_file_size(MediaFile(filename), use_cache=True) == 0
    gui_hooks.media_sync_did_start_or_stop(True)
    assert media_cache.get_file_size(MediaFile(filename), use_cache=True) == 0

    assert not item_id_cache.is_initialized()
    gui_hooks.media_sync_did_start_or_stop(False)
    assert media_cache.get_file_size(MediaFile(filename), use_cache=True) == 0

    item_id_cache.set_initialized(True)
    gui_hooks.media_sync_did_start_or_stop(False)
    assert media_cache.get_file_size(MediaFile(filename), use_cache=True) == len(content)
