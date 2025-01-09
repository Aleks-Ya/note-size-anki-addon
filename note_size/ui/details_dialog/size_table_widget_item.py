import logging
from logging import Logger

from aqt.qt import Qt, QTableWidgetItem

from ...types import SizeStr, FileSize

log: Logger = logging.getLogger(__name__)


class SizeTableWidgetItem(QTableWidgetItem):
    def __init__(self, file_size: FileSize, size_str: SizeStr):
        super().__init__(size_str)
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.file_size: FileSize = file_size

    def __lt__(self, other: object):
        if isinstance(other, SizeTableWidgetItem):
            return self.file_size.size < other.file_size.size
        return NotImplemented
