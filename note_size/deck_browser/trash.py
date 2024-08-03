import logging
from logging import Logger
from pathlib import Path

from anki.collection import Collection

from ..types import FilesNumber, SizeBytes

log: Logger = logging.getLogger(__name__)


class Trash:

    def __init__(self, col: Collection):
        self.__trash_dir: Path = Path(col.media.dir()).joinpath("..").joinpath("media.trash")
        log.info(f"Trash dir: {self.__trash_dir}")
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_trash_files_number(self) -> FilesNumber:
        return FilesNumber(len(list(self.__trash_dir.iterdir())))

    def get_trash_dir_size(self) -> SizeBytes:
        return SizeBytes(sum(f.stat().st_size for f in self.__trash_dir.rglob('*') if f.is_file()))
