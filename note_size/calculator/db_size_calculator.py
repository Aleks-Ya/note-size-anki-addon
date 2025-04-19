import logging
from logging import Logger

from ..common.collection_holder import CollectionHolder
from ..common.types import SizeBytes

log: Logger = logging.getLogger(__name__)


class DbSizeCalculator:

    def __init__(self, collection_holder: CollectionHolder):
        super().__init__()
        self.__collection_holder: CollectionHolder = collection_holder
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_revision_log_size(self) -> SizeBytes:
        size: int = self.__collection_holder.col().db.scalar("SELECT SUM(pgsize) FROM dbstat WHERE name = 'revlog'")
        return SizeBytes(size)

    def get_revision_log_count(self) -> int:
        return self.__collection_holder.col().db.scalar("SELECT count(id) FROM revlog")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
