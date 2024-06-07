import logging
import os
from logging import Logger, FileHandler
from pathlib import Path

from .size_button_formatter import SizeButtonFormatter
from .size_button_hooks import SizeButtonHooks
from .size_calculator import SizeCalculator
from .size_column_hooks import SizeColumnHooks


def configure_logging(addon_folder: Path) -> Logger:
    addon_name: str = addon_folder.name
    log_file: str = os.path.join(addon_folder, f"{addon_name}.log")
    root: Logger = logging.getLogger()
    handler: FileHandler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s'))
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
size_calculator: SizeCalculator = SizeCalculator()
size_column_hooks: SizeColumnHooks = SizeColumnHooks(size_calculator)
size_column_hooks.setup_hooks()
size_button_formatter: SizeButtonFormatter = SizeButtonFormatter(size_calculator)
size_button_hooks: SizeButtonHooks = SizeButtonHooks(size_calculator, size_button_formatter)
size_button_hooks.setup_hooks()
