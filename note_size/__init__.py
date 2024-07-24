from logging import Logger
from pathlib import Path
from threading import Thread

from anki.collection import Collection
from aqt import mw, gui_hooks

from .cache.cache_hooks import CacheHooks
from .cache.media_cache import MediaCache
from .cache.item_id_cache import ItemIdCache
from .config.settings import Settings
from .deck_browser.collection_size_formatter import CollectionSizeFormatter
from .log.logs import Logs


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

    mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")
    addon_dir: Path = Path(__file__).parent
    module: str = addon_dir.stem
    settings: Settings = Settings(addon_dir, module,
                                  mw.addonManager.logs_folder(module),
                                  mw.addonManager.addonFromModule(__name__))
    logs: Logs = Logs(settings)
    log: Logger = logs.root_logger()
    log.info(f"NoteSize addon version: {settings.addon_dir().joinpath('version.txt').read_text()}")
    config_loader: ConfigLoader = ConfigLoader(mw.addonManager, settings)
    config: Config = config_loader.load_config()
    log_level: str = config.log_level()
    log.info(f"Set log level from Config: {log_level}")
    logs.set_level(log_level)
    media_cache: MediaCache = MediaCache(col, config)
    size_calculator: SizeCalculator = SizeCalculator(media_cache)
    item_id_cache: ItemIdCache = ItemIdCache(col, size_calculator, config)
    item_id_sorter: ItemIdSorter = ItemIdSorter(item_id_cache)
    column_hooks: ColumnHooks = ColumnHooks(item_id_cache, item_id_sorter)
    column_hooks.setup_hooks()
    details_formatter: DetailsFormatter = DetailsFormatter(size_calculator, settings, config)
    button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache, size_calculator, config)
    button_hooks: ButtonHooks = ButtonHooks(details_formatter, button_formatter, settings, config)
    button_hooks.setup_hooks()
    collection_size_formatter: CollectionSizeFormatter = CollectionSizeFormatter(col, media_cache)
    deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(collection_size_formatter, config)
    deck_browser_hooks.setup_hooks()
    cache_hooks: CacheHooks = CacheHooks(media_cache, item_id_cache, size_calculator)
    cache_hooks.setup_hooks()
    thread = Thread(target=__warm_up_caches, args=[media_cache, item_id_cache])
    thread.start()


gui_hooks.collection_did_load.append(__initialize)
