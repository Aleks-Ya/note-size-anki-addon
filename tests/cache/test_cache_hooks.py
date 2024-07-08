import tempfile
import time
import unittest
from pathlib import Path

from anki.collection import Collection
from anki import hooks
from anki.notes import Note
from aqt import gui_hooks

from note_size.cache.cache_hooks import CacheHooks
from note_size.config.config import Config
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from tests.data import Data


class TestCacheHooks(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: Data = Data(self.col)
        config: Config = Data.read_config()
        self.media_cache: MediaCache = MediaCache(self.col, config)
        self.size_calculator: SizeCalculator = SizeCalculator(self.media_cache)
        self.item_id_cache: ItemIdCache = ItemIdCache(self.col, self.size_calculator, config)
        self.cache_hooks: CacheHooks = CacheHooks(self.media_cache, self.item_id_cache, self.size_calculator)

    def test_setup_hooks(self):
        self.assertEqual(0, gui_hooks.add_cards_did_add_note.count())
        self.assertEqual(0, hooks.notes_will_be_deleted.count())
        self.assertEqual(0, gui_hooks.media_sync_did_start_or_stop.count())
        self.assertEqual(0, gui_hooks.media_sync_did_progress.count())
        self.cache_hooks.setup_hooks()
        self.assertEqual(1, gui_hooks.add_cards_did_add_note.count())
        self.assertEqual(1, hooks.notes_will_be_deleted.count())
        self.assertEqual(1, gui_hooks.media_sync_did_start_or_stop.count())
        self.assertEqual(1, gui_hooks.media_sync_did_progress.count())
        self.cache_hooks.remove_hooks()
        self.assertEqual(0, gui_hooks.add_cards_did_add_note.count())
        self.assertEqual(0, hooks.notes_will_be_deleted.count())
        self.assertEqual(0, gui_hooks.media_sync_did_start_or_stop.count())
        self.assertEqual(0, gui_hooks.media_sync_did_progress.count())

    def test_add_cards_did_add_note(self):
        self.cache_hooks.setup_hooks()
        self.assertEqual(0, self.item_id_cache.get_total_texts_size())
        self.td.create_note_with_files()
        self.assertEqual(122, self.item_id_cache.get_total_texts_size())

    def test_notes_will_be_deleted(self):
        self.cache_hooks.setup_hooks()
        note: Note = self.td.create_note_with_files()
        self.assertEqual(122, self.item_id_cache.get_total_texts_size())
        self.col.remove_notes([note.id])
        self.assertEqual(0, self.item_id_cache.get_total_texts_size())

    def test_media_sync_did_start_or_stop(self):
        self.cache_hooks.setup_hooks()
        self.td.create_note_with_files()
        self.assertEqual(21, self.media_cache.get_total_files_size())
        Path(self.col.media.dir(), "image.png").write_text("abc")
        self.assertEqual(21, self.media_cache.get_total_files_size())
        gui_hooks.media_sync_did_start_or_stop(True)
        self.assertEqual(21, self.media_cache.get_total_files_size())
        gui_hooks.media_sync_did_start_or_stop(False)
        self.assertEqual(24, self.media_cache.get_total_files_size())

    def test_media_sync_did_progress(self):
        self.cache_hooks.setup_hooks()
        self.td.create_note_with_files()
        self.assertEqual(21, self.media_cache.get_total_files_size())
        Path(self.col.media.dir(), "image.png").write_text("abc")
        self.assertEqual(21, self.media_cache.get_total_files_size())
        gui_hooks.media_sync_did_progress("")
        self.assertEqual(21, self.media_cache.get_total_files_size())
        time.sleep(3)
        gui_hooks.media_sync_did_progress("")
        self.assertEqual(24, self.media_cache.get_total_files_size())

    def tearDown(self):
        self.cache_hooks.remove_hooks()
        self.col.close()


if __name__ == '__main__':
    unittest.main()
