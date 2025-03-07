import logging
from logging import Logger
from pathlib import Path

from ...common.collection_holder import CollectionHolder
from ...common.types import FilesNumber, SizeBytes

log: Logger = logging.getLogger(__name__)


class Trash:

    def __init__(self, collection_holder: CollectionHolder):
        self.__collection_holder: CollectionHolder = collection_holder
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_trash_files_number(self) -> FilesNumber:
        files_number: FilesNumber = FilesNumber(len(list(self.get_trash_dir_path().iterdir())))
        log.debug(f"Trash files number: {files_number}")
        return files_number

    def get_trash_dir_size(self) -> SizeBytes:
        size: SizeBytes = SizeBytes(sum(f.stat().st_size for f in self.get_trash_dir_path().rglob('*') if f.is_file()))
        log.debug(f"Trash dir size: {size}")
        return size

    def get_trash_dir_path(self) -> Path:
        trash_dir: Path = Path(self.__collection_holder.media_dir()).parent.joinpath("media.trash")
        log.info(f"Trash dir: {trash_dir}")
        return trash_dir

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
