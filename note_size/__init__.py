import logging
import os
from logging import Logger, FileHandler
from pathlib import Path

from .note_size_hooks import NoteSizeHooks


def configure_logging():
    init_py_file: Path = Path(__file__)
    addon_dir: Path = init_py_file.parent
    addon_name: str = addon_dir.name
    log_file: str = os.path.join(addon_dir, f"{addon_name}.log")
    root: Logger = logging.getLogger()
    handler: FileHandler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s'))
    root.addHandler(handler)
    log: Logger = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log.info(f"\n\n{'#' * 100}\nLogger was configured: file={log_file}")


configure_logging()
note_size_hooks: NoteSizeHooks = NoteSizeHooks()
note_size_hooks.setup_hooks()
