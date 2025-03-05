from typing import Generator

import pytest
from anki.collection import Collection
from anki import hooks
from anki.errors import NotFoundError
from anki.notes import Note
from aqt import gui_hooks

from note_size.cache.cache_hooks import CacheHooks
from note_size.cache.cache_initializer import CacheInitializer
from note_size.cache.cache_manager import CacheManager
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.calculator.size_calculator import SizeCalculator
from note_size.common.types import SizeType, FileSize, SizeBytes
from tests.data import Data, MediaFiles


@pytest.fixture
def cache_hooks(cache_manager: CacheManager, cache_initializer: CacheInitializer,
                updated_files_calculator: UpdatedFilesCalculator) -> Generator[CacheHooks, None, None]:
    cache_hooks: CacheHooks = CacheHooks(cache_manager, cache_initializer, updated_files_calculator)
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


def test_add_cards_did_add_note(cache_hooks: CacheHooks, td: Data, item_id_cache: ItemIdCache,
                                size_calculator: SizeCalculator):
    cache_hooks.setup_hooks()
    note: Note = td.create_note_with_files()
    assert size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True) == 143


def test_notes_will_be_deleted(cache_hooks: CacheHooks, col: Collection, td: Data, item_id_cache: ItemIdCache,
                               size_calculator: SizeCalculator):
    cache_hooks.setup_hooks()
    note: Note = td.create_note_with_files()
    assert size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True) == 143
    col.remove_notes([note.id])
    with pytest.raises(NotFoundError):
        size_calculator.get_note_size(note.id, SizeType.TOTAL, use_cache=True)


def test_media_sync_did_start_or_stop(cache_hooks: CacheHooks, col: Collection, td: Data, media_cache: MediaCache,
                                      updated_files_calculator: UpdatedFilesCalculator):
    cache_hooks.setup_hooks()
    td.create_note_with_files()
    original_file_size: FileSize = FileSize(SizeBytes(7))

    assert media_cache.get_file_size(MediaFiles.picture, use_cache=True) == original_file_size
    new_content: str = "abc"
    td.write_file(MediaFiles.picture, new_content)
    assert media_cache.get_file_size(MediaFiles.picture, use_cache=True) == original_file_size
    gui_hooks.media_sync_did_start_or_stop(True)
    assert media_cache.get_file_size(MediaFiles.picture, use_cache=True) == original_file_size

    assert not updated_files_calculator.is_initialized()
    gui_hooks.media_sync_did_start_or_stop(False)
    assert media_cache.get_file_size(MediaFiles.picture, use_cache=True) == original_file_size

    updated_files_calculator.set_initialized(True)
    gui_hooks.media_sync_did_start_or_stop(False)
    assert media_cache.get_file_size(MediaFiles.picture, use_cache=True) == FileSize(SizeBytes(len(new_content)))
