import logging
import os
from logging import Logger, FileHandler, Formatter
from pathlib import Path
from threading import Thread

from anki.collection import Collection
from aqt import mw, gui_hooks

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


def __configure_logging(addon_folder: Path) -> Logger:
    log_file: str = os.path.join(addon_folder, "note_size.log")
    logger: Logger = logging.getLogger(__name__)
    handler: FileHandler = FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    formatter: Formatter = Formatter('%(asctime)s %(name)s %(funcName)s %(threadName)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info(f"\n\n{'#' * 100}\nLogger was configured: file={log_file}")
    return logger


__addon_dir: Path = Path(__file__).parent
__module: str = __addon_dir.stem
log: Logger = __configure_logging(__addon_dir)
with open(Path(__addon_dir, 'version.txt'), 'r') as file:
    version = file.read()
log.info(f"NoteSize addon version: {version}")


def __warm_up_caches(media_cache: MediaCache, item_id_cache: ItemIdCache):
    media_cache.warm_up_cache()
    item_id_cache.warm_up_cache()


def __initialize(col: Collection):
    cl: ConfigLoader = ConfigLoader(mw.addonManager, __module)
    c: Config = cl.load_config()
    mc: MediaCache = MediaCache(col, c)
    sc: SizeCalculator = SizeCalculator(mc)
    iic: ItemIdCache = ItemIdCache(col, sc, c)
    iis: ItemIdSorter = ItemIdSorter(iic)
    ch: ColumnHooks = ColumnHooks(iic, iis)
    ch.setup_hooks()
    dt: DetailsFormatter = DetailsFormatter(__addon_dir, sc, c)
    bf: ButtonFormatter = ButtonFormatter(iic, sc)
    bh: ButtonHooks = ButtonHooks(dt, bf)
    bh.setup_hooks()
    thread = Thread(target=__warm_up_caches, args=[mc, iic])
    thread.start()


gui_hooks.collection_did_load.append(__initialize)
