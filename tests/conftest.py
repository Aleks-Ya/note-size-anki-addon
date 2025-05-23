import shutil
import tempfile
from pathlib import Path
from typing import Callable, Any, Generator

import aqt
import pytest
from anki.collection import Collection
from aqt import AnkiQt, ProfileManager, QApplication, QDesktopServices, QWidget, utils
from aqt.addons import AddonManager
from aqt.browser import Browser
from aqt.editor import Editor
from aqt.progress import ProgressManager
from aqt.taskman import TaskManager
from aqt.theme import ThemeManager
from mock.mock import MagicMock
from pytestqt.qtbot import QtBot

from note_size.calculator.db_size_calculator import DbSizeCalculator
from note_size.common.collection_holder import CollectionHolder

utils.tr = MagicMock()
from aqt.deckbrowser import DeckBrowser
from note_size.cache.cache_initializer import CacheInitializer
from note_size.cache.cache_manager import CacheManager
from note_size.cache.cache_storage import CacheStorage
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.cache.size_str_cache import SizeStrCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.calculator.updated_files_calculator import UpdatedFilesCalculator
from note_size.calculator.used_files_calculator import UsedFilesCalculator
from note_size.config.config import Config
from note_size.config.config_loader import ConfigLoader
from note_size.config.level_parser import LevelParser
from note_size.config.settings import Settings
from note_size.config.url_manager import UrlManager
from note_size.log.logs import Logs
from note_size.profiler.profiler import Profiler
from note_size.ui.browser.button.browser_button_manager import BrowserButtonManager
from note_size.ui.config.config_ui import ConfigUi
from note_size.ui.config.model_converter import ModelConverter
from note_size.ui.config.ui_model import UiModel
from note_size.ui.deck_browser.deck_browser_formatter import DeckBrowserFormatter
from note_size.ui.deck_browser.trash import Trash
from note_size.ui.deck_browser.deck_browser_js import DeckBrowserJs
from note_size.ui.deck_browser.deck_browser_updater import DeckBrowserUpdater
from note_size.ui.details_dialog.details_dialog import DetailsDialog
from note_size.ui.details_dialog.details_model_filler import DetailsModelFiller
from note_size.ui.details_dialog.file_type_helper import FileTypeHelper
from note_size.ui.editor.button.editor_button_creator import EditorButtonCreator
from note_size.ui.editor.button.editor_button_formatter import EditorButtonFormatter
from note_size.ui.editor.button.editor_button_js import EditorButtonJs
from note_size.ui.browser.column.item_id_sorter import ItemIdSorter
from note_size.ui.editor.button.editor_button_hooks import EditorButtonHooks
from note_size.cache.cache_hooks import CacheHooks
from note_size.config.config_hooks import ConfigHooks
from note_size.ui.deck_browser.deck_browser_hooks import DeckBrowserHooks
from note_size.ui.browser.column.column_hooks import ColumnHooks
from note_size.ui.browser.button.browser_hooks import BrowserHooks
from note_size.ui.theme.theme_hooks import ThemeHooks
from tests.data import Data


@pytest.fixture
def module_name() -> str:
    return "1188705668"


@pytest.fixture
def profile_manager(base_dir: Path, profile_name: str) -> ProfileManager:
    anki_base_dir: Path = ProfileManager.get_created_base_folder(str(base_dir))
    pm: ProfileManager = ProfileManager(base=anki_base_dir)
    pm.setupMeta()
    pm.create(profile_name)
    pm.openProfile(profile_name)
    pm.save()
    return pm


@pytest.fixture
def profile_dir(profile_manager: ProfileManager) -> Path:
    return Path(profile_manager.profileFolder())


@pytest.fixture
def media_trash_dir(profile_dir: Path) -> Path:
    return profile_dir / "media.trash"


@pytest.fixture
def col(profile_manager: ProfileManager) -> Generator[Collection, None, None]:
    collection_file: str = profile_manager.collectionPath()
    col: Collection = Collection(collection_file)
    yield col
    col.close()


@pytest.fixture
def collection_holder(col: Collection) -> CollectionHolder:
    collection_holder: CollectionHolder = CollectionHolder()
    collection_holder.set_collection(col)
    return collection_holder


@pytest.fixture
def td(collection_holder: CollectionHolder, module_dir: Path) -> Data:
    return Data(collection_holder, module_dir)


@pytest.fixture
def project_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def base_dir() -> Path:
    return Path(tempfile.mkdtemp(prefix="anki-base-dir"))


@pytest.fixture
def logs_dir(base_dir: Path, module_name: str) -> Path:
    return base_dir / "logs" / "addons" / module_name


@pytest.fixture
def profile_name() -> str:
    return "User1"


@pytest.fixture
def addons_dir(base_dir: Path) -> Path:
    return base_dir / "addons21"


@pytest.fixture
def module_dir(addons_dir: Path, module_name: str, project_dir: Path) -> Path:
    addon_project_dir: Path = project_dir.joinpath("note_size")
    module_dir: Path = addons_dir.joinpath(module_name)
    ignore_patterns: Callable[[Any, list[str]], set[str]] = shutil.ignore_patterns("__pycache__")
    shutil.copytree(addon_project_dir, module_dir, ignore=ignore_patterns)
    return module_dir


@pytest.fixture
def settings(module_dir: Path, module_name: str, logs_dir: Path, profile_manager: ProfileManager) -> Settings:
    return Settings(module_dir, module_name, logs_dir, profile_manager)


@pytest.fixture
def config(col: Collection, td: Data) -> Config:
    return td.read_config()


@pytest.fixture
def media_cache(collection_holder: CollectionHolder, config: Config) -> MediaCache:
    return MediaCache(collection_holder, config)


@pytest.fixture
def size_calculator(collection_holder: CollectionHolder, media_cache: MediaCache) -> SizeCalculator:
    return SizeCalculator(collection_holder, media_cache)


@pytest.fixture
def item_id_cache(collection_holder: CollectionHolder) -> ItemIdCache:
    return ItemIdCache(collection_holder)


@pytest.fixture
def current_cache_version() -> int:
    return 5


@pytest.fixture
def cache_storage(current_cache_version: int, settings: Settings) -> CacheStorage:
    return CacheStorage(current_cache_version, settings)


@pytest.fixture
def task_manager(mw: AnkiQt) -> TaskManager:
    return mw.taskman


@pytest.fixture
def deck_browser(mw: AnkiQt) -> DeckBrowser:
    return DeckBrowser(mw)


@pytest.fixture
def cache_initializer(mw: AnkiQt, task_manager: TaskManager, progress_manager: ProgressManager,
                      cache_manager: CacheManager, cache_storage: CacheStorage, deck_browser: DeckBrowser,
                      config: Config) -> CacheInitializer:
    return CacheInitializer(mw, cache_manager, cache_storage, deck_browser, task_manager, progress_manager, config)


@pytest.fixture
def item_id_sorter(item_id_cache: ItemIdCache, size_calculator: SizeCalculator) -> ItemIdSorter:
    return ItemIdSorter(item_id_cache, size_calculator)


@pytest.fixture
def editor_button_formatter(config: Config, size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                            size_str_cache: SizeStrCache, level_parser: LevelParser,
                            theme_manager: ThemeManager) -> EditorButtonFormatter:
    return EditorButtonFormatter(size_str_cache, size_calculator, size_formatter, level_parser, theme_manager, config)


@pytest.fixture
def size_formatter() -> SizeFormatter:
    return SizeFormatter()


@pytest.fixture
def deck_browser_js(config: Config, config_ui: ConfigUi) -> DeckBrowserJs:
    return DeckBrowserJs(config, config_ui)


@pytest.fixture
def deck_browser_updater(deck_browser: DeckBrowser, deck_browser_formatter: DeckBrowserFormatter,
                         config: Config) -> DeckBrowserUpdater:
    return DeckBrowserUpdater(deck_browser, deck_browser_formatter, config)


@pytest.fixture
def trash(collection_holder: CollectionHolder) -> Trash:
    return Trash(collection_holder)


@pytest.fixture
def db_size_calculator(collection_holder: CollectionHolder) -> DbSizeCalculator:
    return DbSizeCalculator(collection_holder)


@pytest.fixture
def deck_browser_formatter(collection_holder: CollectionHolder, item_id_cache: ItemIdCache, media_cache: MediaCache,
                           size_formatter: SizeFormatter, used_files_calculator: UsedFilesCalculator,
                           db_size_calculator: DbSizeCalculator, trash: Trash, theme_manager: ThemeManager,
                           config: Config, settings: Settings) -> DeckBrowserFormatter:
    return DeckBrowserFormatter(collection_holder, item_id_cache, media_cache, trash, size_formatter,
                                used_files_calculator, db_size_calculator, theme_manager, config, settings)


@pytest.fixture
def addon_manager(addons_dir: Path) -> AddonManager:
    mw: MagicMock = MagicMock()
    mw.pm.addonFolder.return_value = addons_dir
    return AddonManager(mw)


@pytest.fixture
def config_loader(addon_manager: AddonManager, settings: Settings) -> ConfigLoader:
    return ConfigLoader(addon_manager, settings)


@pytest.fixture
def logs(settings: Settings) -> Logs:
    return Logs(settings)


@pytest.fixture
def desktop_services() -> QDesktopServices:
    return QDesktopServices()


@pytest.fixture
def config_ui(config: Config, config_loader: ConfigLoader, logs: Logs, cache_initializer: CacheInitializer,
              desktop_services: QDesktopServices, level_parser: LevelParser, url_manager: UrlManager,
              deck_browser: DeckBrowser, theme_manager: ThemeManager, settings: Settings) -> ConfigUi:
    return ConfigUi(config, config_loader, logs, cache_initializer, desktop_services, level_parser, url_manager,
                    deck_browser, theme_manager, settings)


@pytest.fixture
def mw(profile_manager: ProfileManager, qapp: QApplication) -> AnkiQt:
    mw_mock: MagicMock = MagicMock()
    mw_mock.pm = profile_manager
    mw_mock.app = qapp
    mw_mock.taskman = TaskManager(mw_mock)
    mw_mock.progress = ProgressManager(mw_mock)
    aqt.mw = mw_mock
    return mw_mock


@pytest.fixture
def progress_manager(mw: AnkiQt) -> ProgressManager:
    return mw.progress


def __editor(mw: AnkiQt, add_mode: bool) -> Editor:
    widget: QWidget = QWidget()
    parent_widget: QWidget = QWidget()
    return Editor(mw, widget, parent_widget, add_mode)


@pytest.fixture
def editor_add_mode(mw: AnkiQt) -> Editor:
    return __editor(mw, True)


@pytest.fixture
def editor_edit_mode(mw: AnkiQt) -> Editor:
    return __editor(mw, False)


@pytest.fixture
def ui_model() -> UiModel:
    return UiModel()


@pytest.fixture
def details_dialog(qtbot: QtBot, size_calculator: SizeCalculator, size_formatter: SizeFormatter, config_ui: ConfigUi,
                   config: Config, settings: Settings, ui_model: UiModel, theme_manager: ThemeManager,
                   file_type_helper: FileTypeHelper, details_model_filler: DetailsModelFiller) -> DetailsDialog:
    ModelConverter.apply_config_to_model(ui_model, config)
    details_dialog: DetailsDialog = DetailsDialog(size_calculator, size_formatter, file_type_helper,
                                                  details_model_filler, theme_manager, config_ui, config, settings)
    theme_manager.apply_style()
    qtbot.addWidget(details_dialog)
    return details_dialog


@pytest.fixture
def theme_manager() -> ThemeManager:
    return ThemeManager()


@pytest.fixture
def file_type_helper() -> FileTypeHelper:
    return FileTypeHelper()


@pytest.fixture
def level_parser(size_formatter: SizeFormatter) -> LevelParser:
    return LevelParser(size_formatter)


@pytest.fixture
def details_model_filler(size_calculator: SizeCalculator, size_formatter: SizeFormatter,
                         media_cache: MediaCache, config: Config) -> DetailsModelFiller:
    return DetailsModelFiller(size_calculator, size_formatter, media_cache, config)


@pytest.fixture
def editor_button_js(editor_button_formatter: EditorButtonFormatter) -> EditorButtonJs:
    return EditorButtonJs(editor_button_formatter)


@pytest.fixture
def editor_button_creator(editor_button_formatter: EditorButtonFormatter,
                          details_dialog: DetailsDialog) -> EditorButtonCreator:
    return EditorButtonCreator(editor_button_formatter, details_dialog)


@pytest.fixture
def browser_button_manager(item_id_cache: ItemIdCache, size_str_cache: SizeStrCache, details_dialog: DetailsDialog,
                           progress_manager: ProgressManager, config: Config) -> BrowserButtonManager:
    return BrowserButtonManager(item_id_cache, size_str_cache, details_dialog, progress_manager, config)


@pytest.fixture
def browser() -> Browser:
    return MagicMock()


@pytest.fixture
def cache_manager(media_cache: MediaCache, item_id_cache: ItemIdCache, size_calculator: SizeCalculator,
                  size_formatter: SizeFormatter, file_type_helper: FileTypeHelper,
                  size_str_cache: SizeStrCache, updated_files_calculator: UpdatedFilesCalculator) -> CacheManager:
    return CacheManager(media_cache, item_id_cache, size_calculator, size_formatter, file_type_helper, size_str_cache,
                        updated_files_calculator)


@pytest.fixture
def size_str_cache(size_calculator: SizeCalculator, size_formatter: SizeFormatter) -> SizeStrCache:
    return SizeStrCache(size_calculator, size_formatter)


@pytest.fixture
def used_files_calculator(collection_holder: CollectionHolder, size_calculator: SizeCalculator,
                          media_cache: MediaCache) -> UsedFilesCalculator:
    return UsedFilesCalculator(collection_holder, size_calculator, media_cache)


@pytest.fixture
def updated_files_calculator(collection_holder: CollectionHolder, size_calculator: SizeCalculator,
                             media_cache: MediaCache) -> UpdatedFilesCalculator:
    return UpdatedFilesCalculator(collection_holder, size_calculator, media_cache)


@pytest.fixture
def profiler(config: Config, settings: Settings) -> Profiler:
    return Profiler(config, settings)


@pytest.fixture
def url_manager() -> UrlManager:
    return UrlManager()


@pytest.fixture
def editor_button_hooks(editor_button_creator: EditorButtonCreator, editor_button_js: EditorButtonJs,
                        settings: Settings, config: Config) -> Generator[EditorButtonHooks, None, None]:
    editor_button_hooks: EditorButtonHooks = EditorButtonHooks(
        editor_button_creator, editor_button_js, settings, config)
    yield editor_button_hooks
    editor_button_hooks.remove_hooks()


@pytest.fixture
def cache_hooks(cache_manager: CacheManager, cache_initializer: CacheInitializer,
                updated_files_calculator: UpdatedFilesCalculator) -> Generator[CacheHooks, None, None]:
    cache_hooks: CacheHooks = CacheHooks(cache_manager, cache_initializer, updated_files_calculator)
    yield cache_hooks
    cache_hooks.remove_hooks()


@pytest.fixture
def config_hooks(config_ui: ConfigUi, desktop_services: QDesktopServices,
                 url_manager: UrlManager) -> Generator[ConfigHooks, None, None]:
    config_hooks: ConfigHooks = ConfigHooks(config_ui, desktop_services, url_manager)
    yield config_hooks
    config_hooks.remove_hooks()


@pytest.fixture
def deck_browser_hooks(deck_browser_updater: DeckBrowserUpdater,
                       deck_browser_js: DeckBrowserJs) -> Generator[DeckBrowserHooks, None, None]:
    deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(deck_browser_updater, deck_browser_js)
    yield deck_browser_hooks
    deck_browser_hooks.remove_hooks()


@pytest.fixture
def column_hooks(item_id_cache: ItemIdCache, size_str_cache: SizeStrCache, item_id_sorter: ItemIdSorter,
                 config: Config) -> Generator[ColumnHooks, None, None]:
    column_hooks: ColumnHooks = ColumnHooks(item_id_cache, size_str_cache, item_id_sorter, config)
    yield column_hooks
    column_hooks.remove_hooks()


@pytest.fixture
def browser_hooks(browser_button_manager: BrowserButtonManager, config: Config) -> Generator[BrowserHooks, None, None]:
    browser_hooks: BrowserHooks = BrowserHooks(browser_button_manager, config)
    yield browser_hooks
    browser_hooks.remove_hooks()


@pytest.fixture
def theme_hooks(deck_browser_updater: DeckBrowserUpdater,
                details_dialog: DetailsDialog) -> Generator[ThemeHooks, None, None]:
    theme_hooks: ThemeHooks = ThemeHooks(deck_browser_updater, details_dialog)
    yield theme_hooks
    theme_hooks.remove_hooks()


def assert_no_hooks() -> None:
    from aqt import gui_hooks
    assert gui_hooks.editor_did_init.count() == 0
    assert gui_hooks.editor_did_init_buttons.count() == 0
    assert gui_hooks.editor_did_load_note.count() == 2
    assert gui_hooks.editor_did_unfocus_field.count() == 0
    assert gui_hooks.editor_did_fire_typing_timer.count() == 0
    assert gui_hooks.webview_will_set_content.count() == 0
    assert gui_hooks.add_cards_did_add_note.count() == 0
    assert gui_hooks.media_sync_did_start_or_stop.count() == 0
    assert gui_hooks.profile_did_open.count() == 1
    assert gui_hooks.profile_will_close.count() == 1
    assert gui_hooks.browser_did_fetch_columns.count() == 0
    assert gui_hooks.browser_did_fetch_row.count() == 0
    assert gui_hooks.browser_will_search.count() == 0
    assert gui_hooks.browser_did_search.count() == 0
    assert gui_hooks.main_window_did_init.count() == 0
    assert gui_hooks.browser_will_show.count() == 0
    assert gui_hooks.deck_browser_will_render_content.count() == 0
    assert gui_hooks.webview_did_receive_js_message.count() == 0
    assert gui_hooks.collection_did_load.count() == 1

    from anki import hooks
    assert hooks.notes_will_be_deleted.count() == 0
    assert hooks.note_will_flush.count() == 0
