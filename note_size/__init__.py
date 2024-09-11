from logging import Logger
from pathlib import Path

from anki.collection import Collection
from aqt import mw, gui_hooks, QDesktopServices


def __initialize(col: Collection):
    from .config.config import Config
    from .config.config_loader import ConfigLoader
    from .config.config_hooks import ConfigHooks
    from .config.settings import Settings
    from .calculator.size_calculator import SizeCalculator
    from .cache.cache_hooks import CacheHooks
    from .cache.cache_initializer import CacheInitializer
    from .cache.item_id_cache import ItemIdCache
    from .cache.media_cache import MediaCache
    from .cache.cache_storage import CacheStorage
    from .log.logs import Logs
    from .ui.config.config_ui import ConfigUi
    from .ui.deck_browser.collection_size_formatter import CollectionSizeFormatter
    from .ui.deck_browser.deck_browser_hooks import DeckBrowserHooks
    from .ui.deck_browser.trash import Trash
    from .ui.details_dialog.details_dialog import DetailsDialog
    from .ui.editor.button.button_formatter import ButtonFormatter
    from .ui.editor.button.button_hooks import ButtonHooks
    from .ui.editor.column.column_hooks import ColumnHooks
    from .ui.editor.column.item_id_sorter import ItemIdSorter

    module_dir: Path = Path(__file__).parent
    module_name: str = module_dir.stem
    mw.addonManager.setWebExports(module_name, r"ui/web/.*(css|js|png)")
    settings: Settings = Settings(module_dir, module_name, mw.addonManager.logs_folder(module_name))
    logs: Logs = Logs(settings)
    log: Logger = logs.root_logger()
    log.info(f"NoteSize addon version: {settings.module_dir.joinpath('version.txt').read_text()}")
    config_loader: ConfigLoader = ConfigLoader(mw.addonManager, settings)
    config: Config = config_loader.load_config()
    log_level: str = config.get_log_level()
    log.info(f"Set log level from Config: {log_level}")
    logs.set_level(log_level)
    media_cache: MediaCache = MediaCache(col, config)
    size_calculator: SizeCalculator = SizeCalculator(col, media_cache)
    item_id_cache: ItemIdCache = ItemIdCache(col, size_calculator, media_cache)
    item_id_sorter: ItemIdSorter = ItemIdSorter(item_id_cache)
    column_hooks: ColumnHooks = ColumnHooks(item_id_cache, item_id_sorter)
    column_hooks.setup_hooks()
    button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, size_calculator, config)
    trash: Trash = Trash(col)
    cache_storage: CacheStorage = CacheStorage(settings)
    cache_initializer: CacheInitializer = CacheInitializer(mw, media_cache, item_id_cache, size_calculator,
                                                           cache_storage, config)
    collection_size_formatter: CollectionSizeFormatter = CollectionSizeFormatter(
        col, item_id_cache, media_cache, trash, settings)
    desktop_services: QDesktopServices = QDesktopServices()
    config_ui: ConfigUi = ConfigUi(config, config_loader, logs, cache_initializer, desktop_services, settings)
    details_dialog: DetailsDialog = DetailsDialog(size_calculator, config_ui, config, settings)
    button_hooks: ButtonHooks = ButtonHooks(button_formatter, details_dialog, settings, config)
    button_hooks.setup_hooks()
    deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(collection_size_formatter, config, config_ui)
    deck_browser_hooks.setup_hooks()
    cache_hooks: CacheHooks = CacheHooks(media_cache, item_id_cache, size_calculator, cache_initializer)
    cache_hooks.setup_hooks()
    config_hooks: ConfigHooks = ConfigHooks(config_ui, desktop_services)
    config_hooks.setup_hooks()


gui_hooks.collection_did_load.append(__initialize)
