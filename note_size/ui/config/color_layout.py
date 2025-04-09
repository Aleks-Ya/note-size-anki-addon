import logging
from logging import Logger
from typing import Optional

from aqt.qt import QVBoxLayout, QTableWidget, QPushButton, QColorDialog, Qt, \
    QHBoxLayout, QColor, QTableWidgetItem, QDesktopServices, QHeaderView
from aqt.theme import ThemeManager

from ...config.level_parser import Level, LevelParser, LevelDict
from ...config.settings import Settings
from ...config.url_manager import UrlType, UrlManager
from ...ui.config.ui_model import UiModel
from ...ui.config.widgets import GroupVBox, CheckboxWithInfo, InfoButton

log: Logger = logging.getLogger(__name__)


class ColorLayout(QVBoxLayout):
    __min_size_column: int = 0
    __max_size_column: int = 1
    __light_theme_color_column: int = 2
    __dark_theme_color_column: int = 3

    def __init__(self, model: UiModel, desktop_services: QDesktopServices, level_parser: LevelParser,
                 url_manager: UrlManager, theme_manager: ThemeManager, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        self.__level_parser: LevelParser = level_parser
        self.__theme_manager: ThemeManager = theme_manager
        url: str = url_manager.get_url(UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_ENABLED)
        self.__color_enabled_checkbox: CheckboxWithInfo = CheckboxWithInfo(
            "Enable colors", url, desktop_services, settings)
        self.__color_enabled_checkbox.add_checkbox_listener(self.__on_color_enabled_checkbox_state_changed)
        headers: list[str] = ["Min Size", "Max Size", "Color (light theme)", "Color (dark theme)"]
        # noinspection PyTypeChecker
        self.__table: QTableWidget = QTableWidget(0, len(headers))
        self.__table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        # noinspection PyUnresolvedReferences
        self.__table.setHorizontalHeaderLabels(headers)
        self.__table.horizontalHeader().setSectionResizeMode(self.__min_size_column, QHeaderView.ResizeMode.ResizeToContents)
        self.__table.horizontalHeader().setSectionResizeMode(self.__max_size_column, QHeaderView.ResizeMode.ResizeToContents)
        self.__table.horizontalHeader().setSectionResizeMode(self.__light_theme_color_column, QHeaderView.ResizeMode.ResizeToContents)
        self.__table.horizontalHeader().setSectionResizeMode(self.__dark_theme_color_column, QHeaderView.ResizeMode.Stretch)
        self.__table.verticalHeader().setVisible(False)
        # noinspection PyUnresolvedReferences
        self.__table.cellClicked.connect(self.__open_color_dialog)
        # noinspection PyUnresolvedReferences
        self.__table.cellChanged.connect(self.__on_cell_changed)

        add_remove_level_layout: QHBoxLayout = QHBoxLayout()
        add_remove_level_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__add_button: QPushButton = QPushButton("+")
        # noinspection PyUnresolvedReferences
        self.__add_button.setToolTip("Add a color level")
        self.__add_button.setFixedWidth(self.__add_button.sizeHint().width())
        # noinspection PyUnresolvedReferences
        self.__add_button.clicked.connect(self.__add_row)
        self.__remove_button: QPushButton = QPushButton("-")
        # noinspection PyUnresolvedReferences
        self.__remove_button.setToolTip("Remove selected color level")
        self.__remove_button.setFixedWidth(self.__remove_button.sizeHint().width())
        # noinspection PyUnresolvedReferences
        self.__remove_button.clicked.connect(self.__remove_row)
        button_url: str = url_manager.get_url(UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_LEVELS)
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
        log.debug(f"{self.__class__.__name__} was instantiated")

    def refresh_from_model(self) -> None:
        self.__color_enabled_checkbox.set_checked(self.__model.size_button_color_enabled)
        self.__color_enabled_checkbox.setEnabled(self.__model.size_button_enabled)
        # noinspection PyUnresolvedReferences
        self.__table.cellChanged.disconnect()
        self.__set_color_levels(self.__model.size_button_color_levels)
        self.__disable_column(self.__min_size_column)
        self.__disable_column_in_last_row(self.__max_size_column)
        # noinspection PyUnresolvedReferences
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
        self.__level_parser.add_level(self.__model.size_button_color_levels)
        self.refresh_from_model()

    def __remove_row(self) -> None:
        current_row: int = self.__table.currentRow()
        self.__level_parser.remove_level(self.__model.size_button_color_levels, current_row)
        self.refresh_from_model()

    def __open_color_dialog(self, row: int, column: int) -> None:
        if column == self.__light_theme_color_column or column == self.__dark_theme_color_column:
            if not self.__table.item(row, column):
                # noinspection PyUnresolvedReferences
                self.__table.setItem(row, column, QTableWidgetItem(""))
            item: QTableWidgetItem = self.__table.item(row, column)
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
        for row in range(self.__table.rowCount()):
            light_theme_color_item: Optional[QTableWidgetItem] = self.__table.item(row, self.__light_theme_color_column)
            dark_theme_color_item: Optional[QTableWidgetItem] = self.__table.item(row, self.__dark_theme_color_column)
            min_size_item: Optional[QTableWidgetItem] = self.__table.item(row, self.__min_size_column)
            max_size_item: Optional[QTableWidgetItem] = self.__table.item(row, self.__max_size_column)
            level: LevelDict = LevelDict({
                LevelParser.light_theme_color_key: light_theme_color_item.background().color().name() if light_theme_color_item else None,
                LevelParser.dark_theme_color_key: dark_theme_color_item.background().color().name() if dark_theme_color_item else None,
                LevelParser.min_size_key: min_size_item.text() if min_size_item else None,
                LevelParser.max_size_key: max_size_item.text() if max_size_item and max_size_item.text() != "∞" else None})
            color_levels.append(level)
        return color_levels

    def __set_color_levels(self, levels: list[LevelDict]) -> None:
        # noinspection PyUnresolvedReferences
        self.__table.setRowCount(len(levels))
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
            self.__table.setItem(row, self.__min_size_column, min_size_item)
            # noinspection PyUnresolvedReferences
            self.__table.setItem(row, self.__max_size_column, max_size_item)
            # noinspection PyUnresolvedReferences
            self.__table.setItem(row, self.__light_theme_color_column, light_theme_color_item)
            # noinspection PyUnresolvedReferences
            self.__table.setItem(row, self.__dark_theme_color_column, dark_theme_color_item)

    def __disable_column(self, column: int) -> None:
        for row in range(self.__table.rowCount()):
            item: QTableWidgetItem = self.__table.item(row, column)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def __disable_column_in_last_row(self, column: int) -> None:
        last_row: int = self.__table.rowCount() - 1
        last_item: QTableWidgetItem = self.__table.item(last_row, column)
        last_item.setFlags(last_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def __adjust_table_size(self) -> None:
        self.__table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__table.resizeColumnsToContents()
        table_width: int = self.__table.verticalHeader().width() + self.__table.horizontalHeader().length() + 1
        table_height: int = self.__table.horizontalHeader().height() + self.__table.verticalHeader().length()
        self.__table.setFixedSize(table_width, table_height)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
