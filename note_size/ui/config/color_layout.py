import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QPushButton, Qt, QHBoxLayout, QDesktopServices
from aqt.theme import ThemeManager

from .color_table import ColorTable
from ...config.level_parser import LevelParser
from ...config.settings import Settings
from ...config.url_manager import UrlType, UrlManager
from ...ui.config.ui_model import UiModel
from ...ui.config.widgets import GroupVBox, CheckboxWithInfo, InfoButton

log: Logger = logging.getLogger(__name__)


class ColorLayout(QVBoxLayout):

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
        # noinspection PyTypeChecker
        self.__color_table: ColorTable = ColorTable(model, level_parser, theme_manager)
        add_remove_level_layout: QHBoxLayout = QHBoxLayout()
        add_remove_level_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__add_button: QPushButton = QPushButton("+")
        # noinspection PyUnresolvedReferences
        self.__add_button.setToolTip("Add a color level")
        self.__add_button.setFixedWidth(self.__add_button.sizeHint().width())
        # noinspection PyUnresolvedReferences
        self.__add_button.clicked.connect(self.__color_table.add_row)
        self.__remove_button: QPushButton = QPushButton("-")
        # noinspection PyUnresolvedReferences
        self.__remove_button.setToolTip("Remove selected color level")
        self.__remove_button.setFixedWidth(self.__remove_button.sizeHint().width())
        # noinspection PyUnresolvedReferences
        self.__remove_button.clicked.connect(self.__color_table.remove_current_row)
        button_url: str = url_manager.get_url(UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_LEVELS)
        info_button: InfoButton = InfoButton(button_url, desktop_services, settings)
        add_remove_level_layout.addWidget(self.__add_button)
        add_remove_level_layout.addWidget(self.__remove_button)
        add_remove_level_layout.addWidget(info_button)

        self.__group_box: GroupVBox = GroupVBox('Color levels')
        self.__group_box.set_alignment(Qt.AlignmentFlag.AlignTop)
        self.__group_box.add_layout(self.__color_enabled_checkbox)
        self.__group_box.add_widget(self.__color_table)
        self.__group_box.add_layout(add_remove_level_layout)
        self.addWidget(self.__group_box)

        self.__group_box.adjustSize()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def refresh_from_model(self) -> None:
        self.__color_enabled_checkbox.set_checked(self.__model.size_button_color_enabled)
        self.__color_enabled_checkbox.setEnabled(self.__model.size_button_enabled)
        table_enabled: bool = self.__model.size_button_enabled and self.__model.size_button_color_enabled
        self.__color_table.setEnabled(table_enabled)
        self.__group_box.setEnabled(self.__model.size_button_enabled)
        self.__add_button.setEnabled(table_enabled)
        self.__remove_button.setEnabled(table_enabled and len(self.__model.size_button_color_levels) > 1)
        self.__color_table.refresh_from_model()

    def __on_color_enabled_checkbox_state_changed(self, _: int) -> None:
        self.__model.size_button_color_enabled = self.__color_enabled_checkbox.is_checked()
        self.refresh_from_model()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
