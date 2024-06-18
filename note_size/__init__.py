import logging
import os
from logging import Logger, FileHandler, Formatter
from pathlib import Path
from threading import Thread

from aqt import mw, gui_hooks

from .button.button_formatter import ButtonFormatter
from .button.details_formatter import DetailsFormatter
from .button.button_hooks import ButtonHooks
from .config import Config
from .media_cache import MediaCache
from .size_calculator import SizeCalculator
from .column.column_hooks import ColumnHooks
from .size_formatter import SizeFormatter
from .item_id_cache import ItemIdCache


def configure_logging(addon_folder: Path) -> Logger:
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


addon_dir: Path = Path(__file__).parent
log: Logger = configure_logging(addon_dir)
with open(Path(addon_dir, 'version.txt'), 'r') as file:
    version = file.read()
log.info(f"NoteSize addon version: {version}")


def initialize():
    c: Config = Config(mw.addonManager.getConfig(__name__))
    mc: MediaCache = MediaCache(mw.col)
    sc: SizeCalculator = SizeCalculator(mc)
    iic: ItemIdCache = ItemIdCache(mw.col, sc)
    ch: ColumnHooks = ColumnHooks(iic)
    ch.setup_hooks()
    dt: DetailsFormatter = DetailsFormatter(addon_dir, sc, c)
    bf: ButtonFormatter = ButtonFormatter(iic, sc)
    bh: ButtonHooks = ButtonHooks(dt, bf)
    bh.setup_hooks()
    thread = Thread(target=iic.warm_up_cache)
    thread.start()


gui_hooks.profile_did_open.append(initialize)
