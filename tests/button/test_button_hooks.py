import tempfile
import unittest
from pathlib import Path

from anki.collection import Collection
from aqt import gui_hooks

from note_size.button.button_formatter import ButtonFormatter
from note_size.button.button_hooks import ButtonHooks
from note_size.button.details_formatter import DetailsFormatter
from note_size import ItemIdCache, SizeCalculator, MediaCache, Config


class ButtonHooksTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])

    def test_setup_hooks(self):
        self.assertEqual(0, gui_hooks.editor_did_init.count())
        self.assertEqual(0, gui_hooks.editor_did_init_buttons.count())
        self.assertEqual(2, gui_hooks.editor_did_load_note.count())
        self.assertEqual(0, gui_hooks.editor_did_unfocus_field.count())
        self.assertEqual(0, gui_hooks.editor_did_fire_typing_timer.count())

        addon_dir: Path = Path(__file__).parent.parent.parent.joinpath("note_size")
        media_cache: MediaCache = MediaCache(self.col)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator)
        config: Config = Config.from_path(addon_dir.joinpath("config.json"))
        details_formatter: DetailsFormatter = DetailsFormatter(addon_dir, size_calculator, config)
        button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, size_calculator)
        button_hooks: ButtonHooks = ButtonHooks(details_formatter, button_formatter)
        button_hooks.setup_hooks()

        self.assertEqual(1, gui_hooks.editor_did_init.count())
        self.assertEqual(1, gui_hooks.editor_did_init_buttons.count())
        self.assertEqual(3, gui_hooks.editor_did_load_note.count())
        self.assertEqual(1, gui_hooks.editor_did_unfocus_field.count())
        self.assertEqual(1, gui_hooks.editor_did_fire_typing_timer.count())

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
