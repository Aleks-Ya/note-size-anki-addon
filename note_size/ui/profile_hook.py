import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from ..common.collection_holder import CollectionHolder
from ..profiler.profiler import Profiler


class ProfileHook:
    def __init__(self, collection_holder: CollectionHolder):
        self.__collection_holder: CollectionHolder = collection_holder
        self.__profiler: Optional[Profiler] = None
        self.__initialized: bool = False

    def initialize(self) -> None:
        from aqt import mw, QDesktopServices, theme
        from aqt.deckbrowser import DeckBrowser
        from aqt.progress import ProgressManager
        from aqt.taskman import TaskManager
        from aqt import ProfileManager
        from aqt.theme import ThemeManager

        from ..config.config import Config
        from ..config.config_loader import ConfigLoader
        from ..config.config_hooks import ConfigHooks
        from ..config.settings import Settings
        from ..config.level_parser import LevelParser
        from ..config.url_manager import UrlManager
        from ..calculator.size_calculator import SizeCalculator
        from ..calculator.size_formatter import SizeFormatter
        from ..calculator.updated_files_calculator import UpdatedFilesCalculator
        from ..calculator.used_files_calculator import UsedFilesCalculator
        from ..cache.cache_hooks import CacheHooks
        from ..cache.cache_initializer import CacheInitializer
        from ..cache.item_id_cache import ItemIdCache
        from ..cache.media_cache import MediaCache
        from ..cache.cache_storage import CacheStorage
        from ..cache.cache_manager import CacheManager
        from ..cache.size_str_cache import SizeStrCache
        from .deck_browser.deck_browser_js import DeckBrowserJs
        from .deck_browser.deck_browser_updater import DeckBrowserUpdater
        from ..log.logs import Logs
        from ..ui.config.config_ui import ConfigUi
        from ..ui.deck_browser.deck_browser_formatter import DeckBrowserFormatter
        from ..ui.deck_browser.deck_browser_hooks import DeckBrowserHooks
        from ..ui.deck_browser.trash import Trash
        from ..ui.details_dialog.details_dialog import DetailsDialog
        from ..ui.details_dialog.details_model_filler import DetailsModelFiller
        from ..ui.details_dialog.file_type_helper import FileTypeHelper
        from ..ui.editor.button.editor_button_formatter import EditorButtonFormatter
        from ..ui.editor.button.editor_button_hooks import EditorButtonHooks
        from ..ui.browser.column.column_hooks import ColumnHooks
        from ..ui.browser.column.item_id_sorter import ItemIdSorter
        from ..ui.editor.button.editor_button_js import EditorButtonJs
        from ..ui.editor.button.editor_button_creator import EditorButtonCreator
        from ..ui.browser.button.browser_hooks import BrowserHooks
        from ..ui.browser.button.browser_button_manager import BrowserButtonManager
        from ..ui.theme.theme_hooks import ThemeHooks

        profile_manager: ProfileManager = mw.pm
        if self.__initialized:
            log: Logger = logging.getLogger(__name__)
            log.info(f"Switched to profile: '{profile_manager.name}'")
            return
        self.__initialized = True

        module_dir: Path = Path(__file__).parent.parent
        module_name: str = module_dir.stem
        mw.addonManager.setWebExports(module_name, r"ui/web/.*(css|js|png)")
        settings: Settings = Settings(module_dir, module_name, mw.addonManager.logs_folder(module_name),
                                      profile_manager)
        logs: Logs = Logs(settings)
        log: Logger = logs.root_logger()
        log.info(f"NoteSize addon version: {settings.module_dir.joinpath('version.txt').read_text()}")
        config_loader: ConfigLoader = ConfigLoader(mw.addonManager, settings)
        config: Config = config_loader.load_config()

        self.__profiler = Profiler(config, settings)
        self.__profiler.start_profiling()

        log_level: str = config.get_log_level()
        log.info(f"Set log level from Config: {log_level}")
        logs.set_level(log_level)
        media_cache: MediaCache = MediaCache(self.__collection_holder, config)
        size_calculator: SizeCalculator = SizeCalculator(self.__collection_holder, media_cache)
        size_formatter: SizeFormatter = SizeFormatter()
        item_id_cache: ItemIdCache = ItemIdCache(self.__collection_holder)
        item_id_sorter: ItemIdSorter = ItemIdSorter(item_id_cache, size_calculator)
        size_str_cache: SizeStrCache = SizeStrCache(size_calculator, size_formatter)
        column_hooks: ColumnHooks = ColumnHooks(item_id_cache, size_str_cache, item_id_sorter, config)
        column_hooks.setup_hooks()
        level_parser: LevelParser = LevelParser(size_formatter)
        theme_manager: ThemeManager = theme.theme_manager
        editor_button_formatter: EditorButtonFormatter = EditorButtonFormatter(
            size_str_cache, size_calculator, size_formatter, level_parser, theme_manager, config)
        trash: Trash = Trash(self.__collection_holder)
        current_cache_version: int = 1
        cache_storage: CacheStorage = CacheStorage(current_cache_version, settings)
        file_type_helper: FileTypeHelper = FileTypeHelper()
        updated_files_calculator: UpdatedFilesCalculator = UpdatedFilesCalculator(self.__collection_holder,
                                                                                  size_calculator,
                                                                                  media_cache)
        cache_manager: CacheManager = CacheManager(
            media_cache, item_id_cache, size_calculator, size_formatter, file_type_helper, size_str_cache,
            updated_files_calculator)
        deck_browser: DeckBrowser = mw.deckBrowser
        progress_manager: ProgressManager = mw.progress
        task_manager: TaskManager = mw.taskman
        cache_initializer: CacheInitializer = CacheInitializer(mw, cache_manager, cache_storage, deck_browser,
                                                               task_manager, progress_manager, config)
        used_files_calculator: UsedFilesCalculator = UsedFilesCalculator(self.__collection_holder, size_calculator,
                                                                         media_cache)
        deck_browser_formatter: DeckBrowserFormatter = DeckBrowserFormatter(
            self.__collection_holder, item_id_cache, media_cache, trash, size_formatter, used_files_calculator,
            theme_manager, config, settings)
        desktop_services: QDesktopServices = QDesktopServices()
        url_manager: UrlManager = UrlManager()
        config_ui: ConfigUi = ConfigUi(config, config_loader, logs, cache_initializer, desktop_services, level_parser,
                                       url_manager, deck_browser, settings)
        details_model_filler: DetailsModelFiller = DetailsModelFiller(
            size_calculator, size_formatter, media_cache, config)
        details_dialog: DetailsDialog = DetailsDialog(size_calculator, size_formatter, file_type_helper,
                                                      details_model_filler, theme_manager, config_ui, config, settings)
        editor_button_js: EditorButtonJs = EditorButtonJs(editor_button_formatter)
        editor_button_creator: EditorButtonCreator = EditorButtonCreator(editor_button_formatter, details_dialog)
        editor_button_hooks: EditorButtonHooks = EditorButtonHooks(
            editor_button_creator, editor_button_js, settings, config)
        editor_button_hooks.setup_hooks()
        deck_browser_js: DeckBrowserJs = DeckBrowserJs(config, config_ui)
        deck_browser_updater: DeckBrowserUpdater = DeckBrowserUpdater(deck_browser, deck_browser_formatter, config)
        deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(deck_browser_updater, deck_browser_js)
        deck_browser_hooks.setup_hooks()
        cache_hooks: CacheHooks = CacheHooks(cache_manager, cache_initializer, updated_files_calculator)
        cache_hooks.setup_hooks()
        config_hooks: ConfigHooks = ConfigHooks(config_ui, desktop_services, url_manager)
        config_hooks.setup_hooks()
        browser_button_manager: BrowserButtonManager = BrowserButtonManager(
            item_id_cache, size_str_cache, details_dialog, progress_manager, config)
        browser_hooks: BrowserHooks = BrowserHooks(browser_button_manager, config)
        browser_hooks.setup_hooks()
        theme_hooks: ThemeHooks = ThemeHooks(theme_manager, details_dialog, deck_browser_updater)
        theme_hooks.setup_hooks()

    def shutdown(self):
        self.__profiler.stop_profiling()
