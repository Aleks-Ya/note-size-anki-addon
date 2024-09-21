import logging
from logging import Logger

from aqt.qt import Qt, QTableWidgetItem

from ...types import SizeBytes, SizeStr

log: Logger = logging.getLogger(__name__)


class SizeTableWidgetItem(QTableWidgetItem):
    def __init__(self, size_bytes: SizeBytes, size_str: SizeStr):
        super().__init__(size_str)
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.size_bytes: SizeBytes = size_bytes

    def __lt__(self, other: object):
        if isinstance(other, SizeTableWidgetItem):
            return self.size_bytes < other.size_bytes
        return NotImplemented
