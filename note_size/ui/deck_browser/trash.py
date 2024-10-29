import logging
from logging import Logger
from pathlib import Path

from anki.collection import Collection

from ...types import FilesNumber, SizeBytes

log: Logger = logging.getLogger(__name__)


class Trash:

    def __init__(self, col: Collection):
        self.__trash_dir: Path = Path(col.media.dir()).parent.joinpath("media.trash")
        log.info(f"Trash dir: {self.__trash_dir}")
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_trash_files_number(self) -> FilesNumber:
        files_number: FilesNumber = FilesNumber(len(list(self.__trash_dir.iterdir())))
        log.debug(f"Trash files number: {files_number}")
        return files_number

    def get_trash_dir_size(self) -> SizeBytes:
        size: SizeBytes = SizeBytes(sum(f.stat().st_size for f in self.__trash_dir.rglob('*') if f.is_file()))
        log.debug(f"Trash dir size: {size}")
        return size

    def get_trash_dir_path(self) -> Path:
        return self.__trash_dir

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
