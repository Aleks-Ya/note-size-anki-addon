import tempfile
import unittest
from pathlib import Path

from anki.collection import Collection
from aqt import gui_hooks

from note_size.button.button_formatter import ButtonFormatter
from note_size.button.button_hooks import ButtonHooks
from note_size.button.details_formatter import DetailsFormatter
from note_size.config.config import Config
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from tests.data import Data


class TestButtonHooks(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.addon_dir: Path = Path(__file__).parent.parent.parent.joinpath("note_size")
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        details_formatter: DetailsFormatter = DetailsFormatter(self.addon_dir, size_calculator, config)
        button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, size_calculator)
        self.button_hooks: ButtonHooks = ButtonHooks(details_formatter, button_formatter, config)

    def test_setup_hooks_enabled(self):
        self.__assert_no_hooks()
        self.button_hooks.setup_hooks()
        self.assertEqual(1, gui_hooks.editor_did_init.count())
        self.assertEqual(1, gui_hooks.editor_did_init_buttons.count())
        self.assertEqual(3, gui_hooks.editor_did_load_note.count())
        self.assertEqual(1, gui_hooks.editor_did_unfocus_field.count())
        self.assertEqual(1, gui_hooks.editor_did_fire_typing_timer.count())
        self.button_hooks.remove_hooks()
        self.__assert_no_hooks()

    def test_setup_hooks_disabled(self):
        config: Config = Data.read_config_updated({'Size Button': {'Enabled': False}})
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        item_id_cache: ItemIdCache = ItemIdCache(self.col, size_calculator, config)
        details_formatter: DetailsFormatter = DetailsFormatter(self.addon_dir, size_calculator, config)
        button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, size_calculator)
        button_hooks: ButtonHooks = ButtonHooks(details_formatter, button_formatter, config)
        self.__assert_no_hooks()
        button_hooks.setup_hooks()
        self.__assert_no_hooks()
        button_hooks.remove_hooks()
        self.__assert_no_hooks()

    def __assert_no_hooks(self):
        self.assertEqual(0, gui_hooks.editor_did_init.count())
        self.assertEqual(0, gui_hooks.editor_did_init_buttons.count())
        self.assertEqual(2, gui_hooks.editor_did_load_note.count())
        self.assertEqual(0, gui_hooks.editor_did_unfocus_field.count())
        self.assertEqual(0, gui_hooks.editor_did_fire_typing_timer.count())

    def tearDown(self):
        self.button_hooks.remove_hooks()
        self.col.close()


if __name__ == '__main__':
    unittest.main()
