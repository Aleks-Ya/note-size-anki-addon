import logging
import mimetypes
from logging import Logger
from pathlib import Path

from aqt.qt import QTableWidget, Qt, QTableWidgetItem, QIcon, QHeaderView

from ...calculator.size_formatter import SizeFormatter
from ...config.config import Config
from ...config.settings import Settings
from ...types import MediaFile, SizeBytes, SizeStr

log: Logger = logging.getLogger(__name__)


class _IconTableWidgetItem(QTableWidgetItem):
    def __init__(self, icon_path: Path):
        super().__init__()
        self.icon_path: Path = icon_path
        icon: QIcon = QIcon(str(icon_path))
        self.setIcon(icon)
        self.setData(Qt.ItemDataRole.DisplayRole, None)
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable)

    def __lt__(self, other: object):
        if isinstance(other, _IconTableWidgetItem):
            return self.icon_path < other.icon_path
        return NotImplemented


class _SizeTableWidgetItem(QTableWidgetItem):
    def __init__(self, size_bytes: SizeBytes, size_str: SizeStr):
        super().__init__(size_str)
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.size_bytes: SizeBytes = size_bytes

    def __lt__(self, other: object):
        if isinstance(other, _SizeTableWidgetItem):
            return self.size_bytes < other.size_bytes
        return NotImplemented


# noinspection PyUnresolvedReferences
class FilesTable(QTableWidget):
    __icon_column: int = 0
    __filename_column: int = 1
    __size_column: int = 2

    def __init__(self, config: Config, settings: Settings):
        super().__init__(parent=None)
        self.__config: Config = config
        self.__icons_dir: Path = settings.module_dir / "ui" / "details_dialog" / "icon"
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["", "File", "Size"])
        self.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        horizontal_header: QHeaderView = self.horizontalHeader()
        horizontal_header.setMinimumSectionSize(0)
        self.setWordWrap(False)
        self.setSortingEnabled(True)
        self.setStyleSheet("""
        QTableCornerButton::section {
            border-top: 1px solid #e4e4e4;
            border-right: 1px solid #e4e4e4;
            border-bottom: 1px solid #e4e4e4;
            background: #fcfcfc;
            border-top-left-radius: 5px;
        }
        """)
        horizontal_header.setStyleSheet("""
        QHeaderView::section:first {
            padding-right: -4px;
            border-top-left-radius: 0px;
        }
        """)
        vertical_header: QHeaderView = self.verticalHeader()
        vertical_header.setStyleSheet("""
        QHeaderView::section {
            padding-right: 0px;
            border-top: 0px;
        }
        QHeaderView::section {
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
        }
        QHeaderView::section:first {
            border-top: 0px
        }
        """)
        vertical_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        horizontal_header.setSectionResizeMode(self.__icon_column, QHeaderView.ResizeMode.ResizeToContents)
        horizontal_header.setSectionResizeMode(self.__filename_column, QHeaderView.ResizeMode.Stretch)
        horizontal_header.setSectionResizeMode(self.__size_column, QHeaderView.ResizeMode.ResizeToContents)

    def show_files(self, file_sizes: dict[MediaFile, SizeBytes]):
        files_number: int = len(file_sizes)
        self.setRowCount(files_number)
        for i, (file, size) in enumerate(file_sizes.items()):
            size_str: SizeStr = SizeFormatter.bytes_to_str(size)
            icon_path: Path = self.__get_file_icon(file)
            icon_item: _IconTableWidgetItem = _IconTableWidgetItem(icon_path)

            filename_item: QTableWidgetItem = QTableWidgetItem(file)
            filename_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            size_item: _SizeTableWidgetItem = _SizeTableWidgetItem(size, size_str)

            self.setItem(i, self.__icon_column, icon_item)
            self.setItem(i, self.__filename_column, filename_item)
            self.setItem(i, self.__size_column, size_item)
        self.sortItems(self.__size_column, Qt.SortOrder.DescendingOrder)
        if files_number > 0:
            self.show()
        else:
            self.hide()

    def recalculate_window_sizes(self):
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.adjustSize()

    def __get_file_icon(self, filename: str) -> Path:
        icon_path: Path = self.__icons_dir.joinpath("other.png")
        full_mime_type: str = mimetypes.guess_type(filename)[0]
        if not full_mime_type:
            return icon_path
        general_mime_type: str = full_mime_type.split("/")[0]
        png_icon_path: Path = self.__icons_dir.joinpath(general_mime_type + ".png")
        if png_icon_path.exists():
            return png_icon_path
        return icon_path
