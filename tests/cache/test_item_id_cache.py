import timeit

from anki.notes import NoteId, Note

from note_size.cache.item_id_cache import ItemIdCache
from note_size.types import SizeBytes, SizeStr, SizeType
from tests.data import Data, DefaultFields


def test_get_note_size_bytes_no_cache(td: Data, item_id_cache: ItemIdCache):
    exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                      len(DefaultFields.back_field_content.encode()) +
                                      len(DefaultFields.content0) + len(DefaultFields.content1) +
                                      len(DefaultFields.content2))
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeBytes = item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == exp_size_1

    content: str = 'updated'
    Data.update_front_field(note, content)
    act_size_2: SizeBytes = item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
    exp_size_2: SizeBytes = SizeBytes(len(content.encode()) +
                                      len(DefaultFields.back_field_content.encode()) +
                                      len(DefaultFields.content0) +
                                      len(DefaultFields.content2))
    assert act_size_2 == exp_size_2


def test_get_note_size_bytes_use_cache(td: Data, item_id_cache: ItemIdCache):
    exp_size_1: SizeBytes = SizeBytes(len(DefaultFields.front_field_content.encode()) +
                                      len(DefaultFields.back_field_content.encode()) +
                                      len(DefaultFields.content0) +
                                      len(DefaultFields.content1) +
                                      len(DefaultFields.content2))
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeBytes = item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == exp_size_1

    Data.update_front_field(note, 'updated')
    act_size_2: SizeBytes = item_id_cache.get_note_size_bytes(note_id, SizeType.TOTAL, use_cache=True)
    assert act_size_2 == exp_size_1


def test_get_note_size_bytes_performance(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    execution_time: float = timeit.timeit(
        lambda: item_id_cache.get_note_size_bytes(note.id, SizeType.TOTAL, use_cache=True),
        number=1_000_000)
    assert execution_time <= 1


def test_get_note_size_str_no_cache(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeStr = item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == "143 B"

    Data.update_front_field(note, 'updated')
    act_size_2: SizeStr = item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_2 == "86 B"


def test_get_note_size_str_use_cache(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    act_size_1: SizeStr = item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=False)
    assert act_size_1 == "143 B"

    Data.update_front_field(note, 'updated')
    act_size_2: SizeStr = item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True)
    assert act_size_2 == "143 B"


def test_get_total_texts_size(td: Data, item_id_cache: ItemIdCache):
    assert item_id_cache.get_total_texts_size() == SizeBytes(0)

    note1: Note = td.create_note_with_files()
    size1: SizeBytes = item_id_cache.get_note_size_bytes(note1.id, SizeType.TEXTS, use_cache=True)
    assert size1 == item_id_cache.get_total_texts_size()

    note2: Note = td.create_note_without_files()
    size2: SizeBytes = item_id_cache.get_note_size_bytes(note2.id, SizeType.TEXTS, use_cache=True)
    assert size1 + size2 == item_id_cache.get_total_texts_size()


def test_evict_note(td: Data, item_id_cache: ItemIdCache):
    assert item_id_cache.get_total_texts_size() == SizeBytes(0)

    note1: Note = td.create_note_with_files()
    size1: SizeBytes = item_id_cache.get_note_size_bytes(note1.id, SizeType.TEXTS, use_cache=True)
    assert size1 == item_id_cache.get_total_texts_size()

    note2: Note = td.create_note_without_files()
    size2: SizeBytes = item_id_cache.get_note_size_bytes(note2.id, SizeType.TEXTS, use_cache=True)
    assert size1 + size2 == item_id_cache.get_total_texts_size()

    item_id_cache.evict_note(note1.id)
    assert size2 == item_id_cache.get_total_texts_size()


def test_refresh_note(td: Data, item_id_cache: ItemIdCache):
    note: Note = td.create_note_with_files()
    note_id: NoteId = note.id
    assert item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True) == "143 B"

    Data.update_front_field(note, 'updated')
    assert item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True) == "143 B"

    item_id_cache.refresh_note(note_id)
    assert item_id_cache.get_note_size_str(note_id, SizeType.TOTAL, use_cache=True) == "86 B"


def test_is_initialized(item_id_cache: ItemIdCache):
    assert not item_id_cache.is_initialized()
    item_id_cache.warm_up_cache()
    assert item_id_cache.is_initialized()
