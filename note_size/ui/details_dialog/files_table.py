import logging
from logging import Logger
from pathlib import Path

from aqt.qt import QTableWidget, Qt, QTableWidgetItem, QIcon, QHeaderView

from .file_type_helper import FileTypeHelper
from .icon_table_widget_item import IconTableWidgetItem
from .size_table_widget_item import SizeTableWidgetItem
from ...calculator.size_formatter import SizeFormatter
from ...config.config import Config
from ...config.settings import Settings
from ...types import MediaFile, SizeBytes, SizeStr, FileType

log: Logger = logging.getLogger(__name__)


class FilesTable(QTableWidget):
    __icon_column: int = 0
    __filename_column: int = 1
    __size_column: int = 2
    __default_general_mime_type: str = "other"

    def __init__(self, file_type_helper: FileTypeHelper, size_formatter: SizeFormatter, config: Config,
                 settings: Settings):
        super().__init__(parent=None)
        self.__config: Config = config
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__size_formatter: SizeFormatter = size_formatter
        icons_dir: Path = settings.module_dir / "ui" / "details_dialog" / "icon"
        self.__icons: dict[FileType, QIcon] = {
            FileType.OTHER: QIcon(str(icons_dir / "other.png")),
            FileType.IMAGE: QIcon(str(icons_dir / "image.png")),
            FileType.AUDIO: QIcon(str(icons_dir / "audio.png")),
            FileType.VIDEO: QIcon(str(icons_dir / "video.png")),
        }

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

    def show_files(self, file_sizes: dict[MediaFile, SizeBytes]) -> None:
        files_number: int = len(file_sizes)
        log.debug(f"Showing files: {files_number}")
        self.setRowCount(files_number)
        for i, (file, size) in enumerate(file_sizes.items()):
            icon_item: IconTableWidgetItem = self.__create_icon_item(file)

            filename_item: QTableWidgetItem = QTableWidgetItem(file)
            filename_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            size_str: SizeStr = self.__size_formatter.bytes_to_str(size)
            size_item: SizeTableWidgetItem = SizeTableWidgetItem(size, size_str)

            self.setItem(i, self.__icon_column, icon_item)
            self.setItem(i, self.__filename_column, filename_item)
            self.setItem(i, self.__size_column, size_item)
        self.sortItems(self.__size_column, Qt.SortOrder.DescendingOrder)
        if files_number > 0:
            self.show()
            log.debug("Shown files")
        else:
            self.hide()
            log.debug("Table is hidden (no files to show)")

    def __create_icon_item(self, file: MediaFile) -> IconTableWidgetItem:
        file_type: FileType = self.__file_type_helper.get_file_type(file)
        icon: QIcon = self.__icons[file_type]
        icon_item: IconTableWidgetItem = IconTableWidgetItem(icon, file_type)
        return icon_item

    def recalculate_window_sizes(self) -> None:
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.adjustSize()

    def clear_rows(self) -> None:
        self.setRowCount(0)
        self.clearContents()
