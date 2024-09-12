import logging
from logging import Logger
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout, QWidget, Qt, QUrl, QPushButton, QDesktopServices

from ...config.settings import Settings
from ...ui.config.ui_model import UiModel
from ...ui.config.widgets import TitledComboBoxLayout
from ...log.logs import Logs

log: Logger = logging.getLogger(__name__)


class LoggingTab(QWidget):
    name: str = "Logging"

    def __init__(self, model: UiModel, logs: Logs, desktop_services: QDesktopServices, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        self.__logs: Logs = logs
        self.__desktop_services: QDesktopServices = desktop_services
        levels: list[str] = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.__combo_box_layout: TitledComboBoxLayout = TitledComboBoxLayout(
            'Log level:', desktop_services, settings,
            urljoin(settings.docs_base_url, "docs/configuration.md#logging-level"),
            levels)
        self.__combo_box_layout.add_current_text_changed_callback(self.__on_log_level_changed)
        open_log_file_button: QPushButton = QPushButton("Open log file")
        open_log_file_button.setFixedWidth(open_log_file_button.sizeHint().width())
        # noinspection PyUnresolvedReferences
        open_log_file_button.clicked.connect(self.__on_open_log_file_click)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__combo_box_layout)
        layout.addWidget(open_log_file_button)
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__combo_box_layout.set_current_text(self.__model.log_level)

    def __on_log_level_changed(self, log_level: str):
        self.__model.log_level = log_level

    def __on_open_log_file_click(self):
        log_file: str = str(self.__logs.get_log_file())
        url: QUrl = QUrl.fromLocalFile(log_file)
        self.__desktop_services.openUrl(url)