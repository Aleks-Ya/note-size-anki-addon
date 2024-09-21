import logging
from logging import Logger

from aqt.qt import Qt, QTableWidgetItem, QIcon

from ...types import FileType

log: Logger = logging.getLogger(__name__)


class IconTableWidgetItem(QTableWidgetItem):
    def __init__(self, icon: QIcon, file_type: FileType):
        super().__init__()
        self.__file_type: FileType = file_type
        self.setIcon(icon)
        self.setData(Qt.ItemDataRole.DisplayRole, None)
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable)

    def __lt__(self, other: object):
        if isinstance(other, IconTableWidgetItem):
            return self.__file_type.value < other.__file_type.value
        return NotImplemented
