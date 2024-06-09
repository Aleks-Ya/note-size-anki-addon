import logging
import os
from logging import Logger, FileHandler
from pathlib import Path
from threading import Thread

from aqt import mw, gui_hooks

from .size_button_formatter import SizeButtonFormatter
from .size_button_hooks import SizeButtonHooks
from .size_calculator import SizeCalculator
from .size_column_hooks import SizeColumnHooks
from .size_formatter import SizeFormatter
from .item_id_cache import ItemIdCache


def configure_logging(addon_folder: Path) -> Logger:
    log_file: str = os.path.join(addon_folder, "note_size.log")
    root: Logger = logging.getLogger()
    handler: FileHandler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(funcName)s %(threadName)s %(levelname)s %(message)s'))
    root.addHandler(handler)
    logger: Logger = logging.getLogger(__name__)
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
    column_hooks: SizeColumnHooks = SizeColumnHooks(item_id_cache)
    column_hooks.setup_hooks()
    button_formatter: SizeButtonFormatter = SizeButtonFormatter(item_id_cache)
    button_hooks: SizeButtonHooks = SizeButtonHooks(button_formatter)
    button_hooks.setup_hooks()
    thread = Thread(target=item_id_cache.warm_up_cache)
    thread.start()


gui_hooks.profile_did_open.append(initialize)
