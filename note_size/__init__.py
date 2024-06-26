import logging
from logging import Logger, FileHandler, Formatter
from pathlib import Path
from threading import Thread

from anki.collection import Collection
from aqt import mw, gui_hooks
from aqt.addons import AddonManager

from .button.button_formatter import ButtonFormatter
from .button.details_formatter import DetailsFormatter
from .button.button_hooks import ButtonHooks
from .column.item_id_sorter import ItemIdSorter
from .config.config import Config
from .cache.media_cache import MediaCache
from .cache.item_id_cache import ItemIdCache
from .calculator.size_calculator import SizeCalculator
from .calculator.size_formatter import SizeFormatter
from .column.column_hooks import ColumnHooks
from .config.config_loader import ConfigLoader


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
    addon_dir: Path = Path(__file__).parent
    module: str = addon_dir.stem
    log: Logger = __configure_logging(mw.addonManager, module)
    log.info(f"NoteSize addon version: {addon_dir.joinpath('version.txt').open().read()}")
    cl: ConfigLoader = ConfigLoader(mw.addonManager, module)
    c: Config = cl.load_config()
    log_level: str = c.get_log_level()
    log.info(f"Set log level from Config: {log_level}")
    log.setLevel(log_level)
    mc: MediaCache = MediaCache(col, c)
    sc: SizeCalculator = SizeCalculator(mc)
    iic: ItemIdCache = ItemIdCache(col, sc, c)
    iis: ItemIdSorter = ItemIdSorter(iic)
    ch: ColumnHooks = ColumnHooks(iic, iis)
    ch.setup_hooks()
    dt: DetailsFormatter = DetailsFormatter(addon_dir, sc, c)
    bf: ButtonFormatter = ButtonFormatter(iic, sc)
    bh: ButtonHooks = ButtonHooks(dt, bf)
    bh.setup_hooks()
    thread = Thread(target=__warm_up_caches, args=[mc, iic])
    thread.start()


gui_hooks.collection_did_load.append(__initialize)
