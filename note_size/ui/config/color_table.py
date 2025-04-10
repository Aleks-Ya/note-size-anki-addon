import logging
from logging import Logger
from typing import Optional

from aqt.qt import QTableWidget, QColorDialog, Qt, \
    QColor, QTableWidgetItem, QHeaderView
from aqt.theme import ThemeManager

from ...config.level_parser import Level, LevelParser, LevelDict
from ...ui.config.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class ColorTable(QTableWidget):
    __min_size_column: int = 0
    __max_size_column: int = 1
    __light_theme_color_column: int = 2
    __dark_theme_color_column: int = 3

    def __init__(self, model: UiModel, level_parser: LevelParser, theme_manager: ThemeManager):
        super().__init__(parent=None)
        self.__model: UiModel = model
        self.__level_parser: LevelParser = level_parser
        self.__theme_manager: ThemeManager = theme_manager
        headers: list[str] = ["Min Size", "Max Size", "Color (light theme)", "Color (dark theme)"]
        self.setColumnCount(len(headers))
        # noinspection PyTypeChecker
        self.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        # noinspection PyUnresolvedReferences
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(self.__min_size_column, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(self.__max_size_column, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(self.__light_theme_color_column,
                                                     QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(self.__dark_theme_color_column, QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        # noinspection PyUnresolvedReferences
        self.cellClicked.connect(self.__open_color_dialog)
        # noinspection PyUnresolvedReferences
        self.cellChanged.connect(self.__on_cell_changed)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def refresh_from_model(self) -> None:
        # noinspection PyUnresolvedReferences
        self.cellChanged.disconnect()
        self.__set_color_levels(self.__model.size_button_color_levels)
        self.__disable_column(self.__min_size_column)
        self.__disable_column_in_last_row(self.__max_size_column)
        # noinspection PyUnresolvedReferences
        self.cellChanged.connect(self.__on_cell_changed)
        table_enabled: bool = self.__model.size_button_enabled and self.__model.size_button_color_enabled
        self.setEnabled(table_enabled)
        self.__adjust_table_size()

    def add_row(self) -> None:
        self.__level_parser.add_level(self.__model.size_button_color_levels)
        self.refresh_from_model()

    def remove_current_row(self) -> None:
        current_row: int = self.currentRow()
        self.__level_parser.remove_level(self.__model.size_button_color_levels, current_row)
        self.refresh_from_model()

    def __open_color_dialog(self, row: int, column: int) -> None:
        if column == self.__light_theme_color_column or column == self.__dark_theme_color_column:
            if not self.item(row, column):
                # noinspection PyUnresolvedReferences
                self.setItem(row, column, QTableWidgetItem(""))
            item: QTableWidgetItem = self.item(row, column)
            init_color: QColor = item.background().color()
            # noinspection PyArgumentList
            color: Optional[QColor] = QColorDialog.getColor(init_color)
            if color.isValid():
                item.setBackground(color)

    def __on_cell_changed(self, _: int, __: int) -> None:
        color_levels: list[LevelDict] = self.__table_to_color_levels()
        self.__model.size_button_color_levels = color_levels
        self.refresh_from_model()

    def __table_to_color_levels(self) -> list[LevelDict]:
        color_levels: list[LevelDict] = []
        for row in range(self.rowCount()):
            light_theme_color_item: Optional[QTableWidgetItem] = self.item(row, self.__light_theme_color_column)
            dark_theme_color_item: Optional[QTableWidgetItem] = self.item(row, self.__dark_theme_color_column)
            min_size_item: Optional[QTableWidgetItem] = self.item(row, self.__min_size_column)
            max_size_item: Optional[QTableWidgetItem] = self.item(row, self.__max_size_column)
            level: LevelDict = LevelDict({
                LevelParser.light_theme_color_key: light_theme_color_item.background().color().name() if light_theme_color_item else None,
                LevelParser.dark_theme_color_key: dark_theme_color_item.background().color().name() if dark_theme_color_item else None,
                LevelParser.min_size_key: min_size_item.text() if min_size_item else None,
                LevelParser.max_size_key: max_size_item.text() if max_size_item and max_size_item.text() != "∞" else None})
            color_levels.append(level)
        return color_levels

    def __set_color_levels(self, levels: list[LevelDict]) -> None:
        # noinspection PyUnresolvedReferences
        self.setRowCount(len(levels))
        levels_parsed: list[Level] = self.__level_parser.parse_levels(levels)
        for row, level in enumerate(levels_parsed):
            min_size_item: QTableWidgetItem = QTableWidgetItem(level.min_size_str)
            max_size_item: QTableWidgetItem = QTableWidgetItem(level.max_size_str)
            light_theme_color: QColor = QColor(level.light_theme_color)
            light_theme_color_item: QTableWidgetItem = QTableWidgetItem("")
            light_theme_color_item.setBackground(light_theme_color)
            dark_theme_color: QColor = QColor(level.dark_theme_color)
            dark_theme_color_item: QTableWidgetItem = QTableWidgetItem("")
            dark_theme_color_item.setBackground(dark_theme_color)
            # noinspection PyUnresolvedReferences
            self.setItem(row, self.__min_size_column, min_size_item)
            # noinspection PyUnresolvedReferences
            self.setItem(row, self.__max_size_column, max_size_item)
            # noinspection PyUnresolvedReferences
            self.setItem(row, self.__light_theme_color_column, light_theme_color_item)
            # noinspection PyUnresolvedReferences
            self.setItem(row, self.__dark_theme_color_column, dark_theme_color_item)

    def __disable_column(self, column: int) -> None:
        for row in range(self.rowCount()):
            item: QTableWidgetItem = self.item(row, column)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def __disable_column_in_last_row(self, column: int) -> None:
        last_row: int = self.rowCount() - 1
        last_item: QTableWidgetItem = self.item(last_row, column)
        last_item.setFlags(last_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def __adjust_table_size(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.resizeColumnsToContents()
        table_width: int = self.verticalHeader().width() + self.horizontalHeader().length() + 1
        table_height: int = self.horizontalHeader().height() + self.verticalHeader().length()
        self.setFixedSize(table_width, table_height)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
