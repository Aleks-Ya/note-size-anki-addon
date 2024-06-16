import logging
import os
from logging import Logger, FileHandler, Formatter
from pathlib import Path
from threading import Thread

from aqt import mw, gui_hooks

from .button_formatter import ButtonFormatter
from .details_formatter import DetailsFormatter
from .button_hooks import ButtonHooks
from .size_calculator import SizeCalculator
from .column_hooks import ColumnHooks
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
    item_id_cache: ItemIdCache = ItemIdCache(mw.col)
    column_hooks: ColumnHooks = ColumnHooks(item_id_cache)
    column_hooks.setup_hooks()
    details_formatter: DetailsFormatter = DetailsFormatter()
    button_formatter: ButtonFormatter = ButtonFormatter(item_id_cache)
    button_hooks: ButtonHooks = ButtonHooks(details_formatter, button_formatter)
    button_hooks.setup_hooks()
    thread = Thread(target=item_id_cache.warm_up_cache)
    thread.start()


gui_hooks.profile_did_open.append(initialize)
