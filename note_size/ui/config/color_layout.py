import logging
from logging import Logger
from typing import Optional
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout, QTableWidget, QPushButton, QColorDialog, Qt, \
    QHBoxLayout, QColor, QTableWidgetItem, QDesktopServices

from ...config.level_parser import Level, LevelParser
from ...config.settings import Settings
from ...ui.config.ui_model import UiModel
from ...ui.config.widgets import GroupVBox, CheckboxWithInfo, InfoButton

log: Logger = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
class ColorLayout(QVBoxLayout):
    __min_size_column: int = 0
    __max_size_column: int = 1
    __color_column: int = 2
    __color_key: str = 'Color'
    __min_size_key: str = 'Min Size'
    __max_size_key: str = 'Max Size'

    def __init__(self, model: UiModel, desktop_services: QDesktopServices, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        url: str = urljoin(settings.docs_base_url, "docs/configuration.md#color---enabled")
        self.__color_enabled_checkbox: CheckboxWithInfo = CheckboxWithInfo("Enable colors", url, desktop_services,
                                                                           settings)
        self.__color_enabled_checkbox.add_checkbox_listener(self.__on_color_enabled_checkbox_state_changed)
        headers: list[str] = ["Min Size", "Max Size", "Color"]
        # noinspection PyTypeChecker
        self.__table: QTableWidget = QTableWidget(0, len(headers))
        self.__table.setHorizontalHeaderLabels(headers)
        self.__table.verticalHeader().setVisible(False)
        self.__table.cellClicked.connect(self.__open_color_dialog)
        self.__table.cellChanged.connect(self.__on_cell_changed)

        add_remove_level_layout: QHBoxLayout = QHBoxLayout()
        add_remove_level_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__add_button: QPushButton = QPushButton("+")
        self.__add_button.setToolTip("Add a color level")
        self.__add_button.setFixedWidth(self.__add_button.sizeHint().width())
        self.__add_button.clicked.connect(self.__add_row)
        self.__remove_button: QPushButton = QPushButton("-")
        self.__remove_button.setToolTip("Remove selected color level")
        self.__remove_button.setFixedWidth(self.__remove_button.sizeHint().width())
        self.__remove_button.clicked.connect(self.__remove_row)
        button_url: str = urljoin(settings.docs_base_url, "docs/configuration.md#color---levels")
        info_button: InfoButton = InfoButton(button_url, desktop_services, settings)
        add_remove_level_layout.addWidget(self.__add_button)
        add_remove_level_layout.addWidget(self.__remove_button)
        add_remove_level_layout.addWidget(info_button)

        self.__group_box: GroupVBox = GroupVBox('Color levels')
        self.__group_box.set_alignment(Qt.AlignmentFlag.AlignTop)
        self.__group_box.add_layout(self.__color_enabled_checkbox)
        self.__group_box.add_widget(self.__table)
        self.__group_box.add_layout(add_remove_level_layout)
        self.addWidget(self.__group_box)

        self.__group_box.adjustSize()

    def refresh_from_model(self) -> None:
        self.__color_enabled_checkbox.set_checked(self.__model.size_button_color_enabled)
        self.__color_enabled_checkbox.setEnabled(self.__model.size_button_enabled)
        self.__table.cellChanged.disconnect()
        self.__set_color_levels(self.__model.size_button_color_levels)
        self.__disable_column(self.__min_size_column)
        self.__disable_column_in_last_row(self.__max_size_column)
        self.__table.cellChanged.connect(self.__on_cell_changed)
        table_enabled: bool = self.__model.size_button_enabled and self.__model.size_button_color_enabled
        self.__table.setEnabled(table_enabled)
        self.__group_box.setEnabled(self.__model.size_button_enabled)
        self.__add_button.setEnabled(table_enabled)
        self.__remove_button.setEnabled(table_enabled and len(self.__model.size_button_color_levels) > 1)
        self.__adjust_table_size()

    def __on_color_enabled_checkbox_state_changed(self, _: int) -> None:
        self.__model.size_button_color_enabled = self.__color_enabled_checkbox.is_checked()
        self.refresh_from_model()

    def __add_row(self) -> None:
        LevelParser.add_level(self.__model.size_button_color_levels)
        self.refresh_from_model()

    def __remove_row(self) -> None:
        current_row: int = self.__table.currentRow()
        LevelParser.remove_level(self.__model.size_button_color_levels, current_row)
        self.refresh_from_model()

    def __open_color_dialog(self, row, column) -> None:
        if column == self.__color_column:
            if not self.__table.item(row, column):
                self.__table.setItem(row, column, QTableWidgetItem(""))
            item: QTableWidgetItem = self.__table.item(row, column)
            init_color: QColor = item.background().color()
            # noinspection PyArgumentList
            color: Optional[QColor] = QColorDialog.getColor(init_color)
            if color.isValid():
                item.setBackground(color)

    def __on_cell_changed(self, _: int, __: int) -> None:
        color_levels: list[dict[str, str]] = self.__table_to_color_levels()
        self.__model.size_button_color_levels = color_levels
        self.refresh_from_model()

    def __table_to_color_levels(self) -> list[dict[str, str]]:
        color_levels: list[dict[str, str]] = []
        for row in range(self.__table.rowCount()):
            color_item: Optional[QTableWidgetItem] = self.__table.item(row, self.__color_column)
            min_size_item: Optional[QTableWidgetItem] = self.__table.item(row, self.__min_size_column)
            max_size_item: Optional[QTableWidgetItem] = self.__table.item(row, self.__max_size_column)
            level: dict[str, str] = {
                self.__color_key: color_item.background().color().name() if color_item else None,
                self.__min_size_key: min_size_item.text() if min_size_item else None,
                self.__max_size_key: max_size_item.text() if max_size_item and max_size_item.text() != "∞" else None}
            color_levels.append(level)
        return color_levels

    def __set_color_levels(self, levels: list[dict[str, str]]) -> None:
        self.__table.setRowCount(len(levels))
        levels_parsed: list[Level] = LevelParser.parse_levels(levels)
        for row, level in enumerate(levels_parsed):
            color: QColor = QColor(level.color)
            color_item: QTableWidgetItem = QTableWidgetItem("")
            color_item.setBackground(color)
            min_size_item: QTableWidgetItem = QTableWidgetItem(level.min_size_str)
            max_size_item: QTableWidgetItem = QTableWidgetItem(level.max_size_str)
            self.__table.setItem(row, self.__color_column, color_item)
            self.__table.setItem(row, self.__min_size_column, min_size_item)
            self.__table.setItem(row, self.__max_size_column, max_size_item)

    def __disable_column(self, column: int) -> None:
        for row in range(self.__table.rowCount()):
            item = self.__table.item(row, column)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def __disable_column_in_last_row(self, column: int) -> None:
        last_row: int = self.__table.rowCount() - 1
        last_item: QTableWidgetItem = self.__table.item(last_row, column)
        last_item.setFlags(last_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def __adjust_table_size(self) -> None:
        self.__table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__table.adjustSize()
        table_width: int = self.__table.verticalHeader().width() + self.__table.horizontalHeader().length() + 1
        table_height: int = self.__table.horizontalHeader().height() + self.__table.verticalHeader().length()
        self.__table.setFixedSize(table_width, table_height)
