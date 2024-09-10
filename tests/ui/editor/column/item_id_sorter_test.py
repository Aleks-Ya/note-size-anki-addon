from typing import Sequence

from anki.notes import Note
from aqt.browser import ItemId

from note_size.ui.editor.column.item_id_sorter import ItemIdSorter
from note_size.types import SizeType
from tests.data import Data


def test_sort_item_ids(td: Data, item_id_sorter: ItemIdSorter):
    note1: Note = td.create_note_without_files()
    note2: Note = td.create_note_without_files()
    note3: Note = td.create_note_with_files()
    td.update_front_field(note1, "abc")
    item_ids: Sequence[ItemId] = [note1.id, note2.id, note3.id]
    act_item_ids: Sequence[ItemId] = item_id_sorter.sort_item_ids(item_ids, SizeType.TOTAL, True)
    exp_item_ids: Sequence[ItemId] = [note3.id, note2.id, note1.id]
    assert act_item_ids == exp_item_ids
