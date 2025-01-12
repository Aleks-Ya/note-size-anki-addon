import logging
from logging import Logger

from aqt.qt import Qt, QTableWidgetItem

from ...common.types import SizeStr, FileSize, MediaFile

log: Logger = logging.getLogger(__name__)


class SizeTableWidgetItem(QTableWidgetItem):
    def __init__(self, media_file: MediaFile, file_size: FileSize, size_str: SizeStr):
        super().__init__(size_str if file_size.exists else "❌")
        self.setToolTip(None if file_size.exists else "File is referenced in notes, but missing in media folder")
        self.setTextAlignment(Qt.AlignmentFlag.AlignLeft if file_size.exists else Qt.AlignmentFlag.AlignCenter)
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.media_file: MediaFile = media_file
        self.file_size: FileSize = file_size

    def __lt__(self, other: object) -> bool:
        if isinstance(other, SizeTableWidgetItem):
            if self.file_size.exists and other.file_size.exists:
                return self.file_size.size < other.file_size.size
            elif not self.file_size.exists and not other.file_size.exists:
                return self.media_file > other.media_file
            else:
                return other.file_size.exists
        return NotImplemented
