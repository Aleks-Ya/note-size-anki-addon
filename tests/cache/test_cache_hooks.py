import time
from pathlib import Path

import pytest
from anki.collection import Collection
from anki import hooks
from anki.errors import NotFoundError
from anki.notes import Note
from aqt import gui_hooks

from note_size.cache.cache_hooks import CacheHooks
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.types import SizeType
from tests.data import Data


@pytest.fixture
def cache_hooks(media_cache: MediaCache, size_calculator: SizeCalculator, item_id_cache: ItemIdCache) -> CacheHooks:
    cache_hooks = CacheHooks(media_cache, item_id_cache, size_calculator)
    yield cache_hooks
    cache_hooks.remove_hooks()


def test_setup_hooks(cache_hooks: CacheHooks):
    assert gui_hooks.add_cards_did_add_note.count() == 0
    assert hooks.notes_will_be_deleted.count() == 0
    assert gui_hooks.media_sync_did_start_or_stop.count() == 0
    assert gui_hooks.media_sync_did_progress.count() == 0
    cache_hooks.setup_hooks()
    assert gui_hooks.add_cards_did_add_note.count() == 1
    assert hooks.notes_will_be_deleted.count() == 1
    assert gui_hooks.media_sync_did_start_or_stop.count() == 1
    assert gui_hooks.media_sync_did_progress.count() == 1
    cache_hooks.remove_hooks()
    assert gui_hooks.add_cards_did_add_note.count() == 0
    assert hooks.notes_will_be_deleted.count() == 0
    assert gui_hooks.media_sync_did_start_or_stop.count() == 0
    assert gui_hooks.media_sync_did_progress.count() == 0


def test_add_cards_did_add_note(td: Data, cache_hooks: CacheHooks, item_id_cache: ItemIdCache):
    cache_hooks.setup_hooks()
    note: Note = td.create_note_with_files()
    assert item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True) == 143


def test_notes_will_be_deleted(col: Collection, td: Data, cache_hooks: CacheHooks, item_id_cache: ItemIdCache):
    cache_hooks.setup_hooks()
    note: Note = td.create_note_with_files()
    assert item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True) == 143
    col.remove_notes([note.id])
    with pytest.raises(NotFoundError):
        assert item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True) == 0


def test_media_sync_did_start_or_stop(col: Collection, td: Data, cache_hooks: CacheHooks, media_cache: MediaCache):
    cache_hooks.setup_hooks()
    td.create_note_with_files()
    assert media_cache.get_total_files_size() == 21
    Path(col.media.dir(), "image.png").write_text("abc")
    assert media_cache.get_total_files_size() == 21
    gui_hooks.media_sync_did_start_or_stop(True)
    assert media_cache.get_total_files_size() == 21
    gui_hooks.media_sync_did_start_or_stop(False)
    assert media_cache.get_total_files_size() == 24


def test_media_sync_did_progress(col: Collection, td: Data, cache_hooks: CacheHooks, media_cache: MediaCache):
    cache_hooks.setup_hooks()
    td.create_note_with_files()
    assert media_cache.get_total_files_size() == 21
    Path(col.media.dir(), "image.png").write_text("abc")
    assert media_cache.get_total_files_size() == 21
    gui_hooks.media_sync_did_progress("")
    assert media_cache.get_total_files_size() == 21
    time.sleep(3)
    gui_hooks.media_sync_did_progress("")
    assert media_cache.get_total_files_size() == 24
