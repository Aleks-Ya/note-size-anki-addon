import logging
from logging import Logger
from pathlib import Path

from aqt import colors, props
from aqt.qt import QTableWidget, Qt, QTableWidgetItem, QIcon, QHeaderView
from aqt.theme import ThemeManager

from .file_type_helper import FileTypeHelper
from .icon_table_widget_item import IconTableWidgetItem
from .size_table_widget_item import SizeTableWidgetItem
from ...calculator.size_formatter import SizeFormatter
from ...config.config import Config
from ...config.settings import Settings
from ...common.types import MediaFile, SizeStr, FileType, FileSize, SignificantDigits, ColorName

log: Logger = logging.getLogger(__name__)


class FilesTable(QTableWidget):
    __icon_column: int = 0
    __filename_column: int = 1
    __size_column: int = 2

    def __init__(self, file_type_helper: FileTypeHelper, size_formatter: SizeFormatter,
                 theme_manager: ThemeManager, config: Config, settings: Settings):
        super().__init__(parent=None)
        self.__theme_manager: ThemeManager = theme_manager
        self.__config: Config = config
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__size_formatter: SizeFormatter = size_formatter
        self.__items_dict: dict[int, dict[int, QTableWidgetItem]] = {}
        icons_dir: Path = settings.module_dir / "ui" / "details_dialog" / "icon"
        self.__icons: dict[FileType, QIcon] = {
            FileType.OTHER: QIcon(str(icons_dir / "other.png")),
            FileType.IMAGE: QIcon(str(icons_dir / "image.png")),
            FileType.AUDIO: QIcon(str(icons_dir / "audio.png")),
            FileType.VIDEO: QIcon(str(icons_dir / "video.png")),
        }

        self.setColumnCount(3)
        # noinspection PyUnresolvedReferences
        self.setHorizontalHeaderLabels(["", "File", "Size"])
        self.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.setWordWrap(False)
        self.setSortingEnabled(True)
        self.__horizontal_header: QHeaderView = self.horizontalHeader()
        self.__horizontal_header.setMinimumSectionSize(0)
        self.__horizontal_header.setSectionResizeMode(self.__icon_column, QHeaderView.ResizeMode.ResizeToContents)
        self.__horizontal_header.setSectionResizeMode(self.__filename_column, QHeaderView.ResizeMode.Stretch)
        self.__horizontal_header.setSectionResizeMode(self.__size_column, QHeaderView.ResizeMode.ResizeToContents)
        self.__vertical_header: QHeaderView = self.verticalHeader()
        self.__vertical_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.on_theme_changed()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def prepare_items(self, file_sizes: dict[MediaFile, FileSize]) -> None:
        files_number: int = len(file_sizes)
        log.debug(f"Prepare for showing files: {files_number}")
        self.__items_dict: dict[int, dict[int, QTableWidgetItem]] = {}
        sorted_file_sizes: dict[MediaFile, FileSize] = dict(
            sorted(file_sizes.items(), key=lambda item: item[1].size, reverse=True))
        for row_index, (media_file, file_size) in enumerate(sorted_file_sizes.items()):
            icon_item: IconTableWidgetItem = self.__create_icon_item(media_file)

            filename_item: QTableWidgetItem = QTableWidgetItem(media_file)
            filename_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            significant_digits: SignificantDigits = self.__config.get_browser_significant_digits()
            size_str: SizeStr = self.__size_formatter.bytes_to_str(file_size.size, significant_digits)
            size_item: SizeTableWidgetItem = SizeTableWidgetItem(media_file, file_size, size_str)

            self.__items_dict[row_index] = {}
            self.__items_dict[row_index][self.__icon_column] = icon_item
            self.__items_dict[row_index][self.__filename_column] = filename_item
            self.__items_dict[row_index][self.__size_column] = size_item

    def show_files(self) -> None:
        files_number: int = len(self.__items_dict)
        log.debug(f"Prepare for showing files: {files_number}")
        # noinspection PyUnresolvedReferences
        self.setUpdatesEnabled(False)
        self.blockSignals(True)
        self.setSortingEnabled(False)
        # noinspection PyUnresolvedReferences
        self.setRowCount(files_number)
        for row_index, row in enumerate(self.__items_dict.values()):
            # noinspection PyUnresolvedReferences
            self.setItem(row_index, self.__icon_column, row[self.__icon_column])
            # noinspection PyUnresolvedReferences
            self.setItem(row_index, self.__filename_column, row[self.__filename_column])
            # noinspection PyUnresolvedReferences
            self.setItem(row_index, self.__size_column, row[self.__size_column])
        # noinspection PyUnresolvedReferences
        self.sortItems(self.__size_column, Qt.SortOrder.DescendingOrder)
        # noinspection PyUnresolvedReferences
        self.setUpdatesEnabled(True)
        self.blockSignals(False)
        self.setSortingEnabled(True)
        if self.rowCount() > 0:
            # noinspection PyUnresolvedReferences
            self.show()
            log.debug("Shown files")
        else:
            self.hide()
            log.debug("Table is hidden (no files to show)")

    def recalculate_window_sizes(self) -> None:
        if self.rowCount() > 0:
            # noinspection PyUnresolvedReferences
            self.setUpdatesEnabled(False)
            self.blockSignals(True)

            hint: int = self.sizeHintForRow(0)
            for row in range(self.rowCount()):
                self.setRowHeight(row, hint)

            # noinspection PyUnresolvedReferences
            self.setUpdatesEnabled(True)
            self.blockSignals(False)

        self.resizeColumnsToContents()
        self.adjustSize()

    def clear_rows(self) -> None:
        # noinspection PyUnresolvedReferences
        self.setRowCount(0)
        self.clearContents()

    def on_theme_changed(self) -> None:
        log.debug("On theme changed")
        border_color: ColorName = ColorName(self.__theme_manager.var(colors.BORDER_SUBTLE))
        # noinspection PyUnresolvedReferences
        self.setStyleSheet(f"""
        QTableCornerButton::section {{
            border-top: 1px solid {border_color};
            border-right: 1px solid {border_color};
            border-bottom: 1px solid {border_color};
            background: {self.__theme_manager.var(colors.BUTTON_BG)};
            border-top-left-radius: {self.__theme_manager.var(props.BORDER_RADIUS)};
        }}
        """)
        # noinspection PyUnresolvedReferences
        self.__horizontal_header.setStyleSheet("""
        QHeaderView::section:first {
            padding-right: -4px;
            border-top-left-radius: 0px;
        }
        """)
        # noinspection PyUnresolvedReferences
        self.__vertical_header.setStyleSheet("""
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

    def __create_icon_item(self, media_file: MediaFile) -> IconTableWidgetItem:
        file_type: FileType = self.__file_type_helper.get_file_type(media_file)
        icon: QIcon = self.__icons[file_type]
        icon_item: IconTableWidgetItem = IconTableWidgetItem(icon, file_type)
        return icon_item

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
