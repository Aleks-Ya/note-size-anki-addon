import logging
from logging import Logger, FileHandler, Formatter
from pathlib import Path
from threading import Thread

from anki.collection import Collection
from aqt import mw, gui_hooks
from aqt.addons import AddonManager

from .cache.cache_hooks import CacheHooks
from .cache.media_cache import MediaCache
from .cache.item_id_cache import ItemIdCache
from .deck_browser.collection_size_formatter import CollectionSizeFormatter


def __configure_logging(addon_manager: AddonManager, module: str) -> Logger:
    log_dir: Path = addon_manager.logs_folder(module)
    log_dir.mkdir(exist_ok=True, parents=True)
    log_file: Path = log_dir.joinpath("note_size.log")
    logger: Logger = logging.getLogger(__name__)
    handler: FileHandler = FileHandler(log_file)
    level: int = logging.DEBUG
    handler.setLevel(level)
    formatter: Formatter = Formatter('%(asctime)s %(levelname)s %(name)s %(funcName)s %(threadName)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.info(f"\n\n{'#' * 100}\nLogger was configured: level={logging.getLevelName(level)}, file={log_file}")
    return logger


def __warm_up_caches(media_cache: MediaCache, item_id_cache: ItemIdCache):
    media_cache.warm_up_cache()
    item_id_cache.warm_up_cache()


def __initialize(col: Collection):
    from .button.button_formatter import ButtonFormatter
    from .button.details_formatter import DetailsFormatter
    from .button.button_hooks import ButtonHooks
    from .column.item_id_sorter import ItemIdSorter
    from .config.config import Config
    from .calculator.size_calculator import SizeCalculator
    from .column.column_hooks import ColumnHooks
    from .config.config_loader import ConfigLoader
    from .deck_browser.deck_browser_hooks import DeckBrowserHooks

    addon_dir: Path = Path(__file__).parent
    module: str = addon_dir.stem
    log: Logger = __configure_logging(mw.addonManager, module)
    log.info(f"NoteSize addon version: {addon_dir.joinpath('version.txt').open().read()}")
    config_loader: ConfigLoader = ConfigLoader(mw.addonManager, module)
    config: Config = config_loader.load_config()
    log_level: str = config.get_log_level()
    log.info(f"Set log level from Config: {log_level}")
    log.setLevel(log_level)
    media_cache: MediaCache = MediaCache(col, config)
    size_calculator: SizeCalculator = SizeCalculator(media_cache)
    item_id_cache: ItemIdCache = ItemIdCache(col, size_calculator, config)
    item_id_sorter: ItemIdSorter = ItemIdSorter(item_id_cache)
    column_hooks: ColumnHooks = ColumnHooks(item_id_cache, item_id_sorter)
    column_hooks.setup_hooks()
    details_formatter: DetailsFormatter = DetailsFormatter(addon_dir, size_calculator, config)
    button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, size_calculator)
    button_hooks: ButtonHooks = ButtonHooks(details_formatter, button_formatter)
    button_hooks.setup_hooks()
    collection_size_formatter: CollectionSizeFormatter = CollectionSizeFormatter(col, media_cache)
    deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(collection_size_formatter)
    deck_browser_hooks.setup_hooks()
    cache_hooks: CacheHooks = CacheHooks(media_cache, item_id_cache, size_calculator)
    cache_hooks.setup_hooks()
    thread = Thread(target=__warm_up_caches, args=[media_cache, item_id_cache])
    thread.start()


gui_hooks.collection_did_load.append(__initialize)
