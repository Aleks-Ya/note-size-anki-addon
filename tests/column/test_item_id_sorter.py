import tempfile
import unittest
from typing import Sequence

from anki.collection import Collection
from anki.notes import Note
from aqt.browser import ItemId

from note_size.config.config import Config
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.column.item_id_sorter import ItemIdSorter
from note_size.types import SizeType
from tests.data import Data


class TestItemIdSorter(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        self.td: Data = Data(self.col)
        self.item_id_sorter: ItemIdSorter = ItemIdSorter(item_id_cache)

    def test_sort_item_ids(self):
        note1: Note = self.td.create_note_without_files()
        note2: Note = self.td.create_note_without_files()
        note3: Note = self.td.create_note_with_files()
        self.td.update_front_field(note1, "abc")
        item_ids: Sequence[ItemId] = [note1.id, note2.id, note3.id]
        act_item_ids: Sequence[ItemId] = self.item_id_sorter.sort_item_ids(item_ids, SizeType.TOTAL, True)
        exp_item_ids: Sequence[ItemId] = [note3.id, note2.id, note1.id]
        self.assertSequenceEqual(exp_item_ids, act_item_ids)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
