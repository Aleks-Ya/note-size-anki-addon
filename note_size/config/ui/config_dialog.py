import logging
from logging import Logger
from typing import Optional, Any

import aqt
from aqt.qt import QDialog, QVBoxLayout, QDialogButtonBox, QTabWidget, QPushButton

from .model_converter import ModelConverter
from ..config_loader import ConfigLoader
from ..settings import Settings
from ..ui.cache_tab import CacheTab
from ..ui.deck_browser_tab import DeckBrowserTab
from ..ui.logging_tab import LoggingTab
from ..ui.editor_tab import EditorTab
from ...config.ui.ui_model import UiModel
from ...config.config import Config
from ...log.logs import Logs

log: Logger = logging.getLogger(__name__)


class ConfigDialog(QDialog):
    def __init__(self, config: Config, config_loader: ConfigLoader, model: UiModel, logs: Logs, settings: Settings):
        super().__init__(parent=None)
        self.__config: Config = config
        self.__logs: Logs = logs
        self.__model: UiModel = model
        self.__config_loader: ConfigLoader = config_loader
        ModelConverter.apply_config_to_model(model, config)
        self.setWindowTitle('"Note Size" addon configuration')

        self.deck_browser_tab: DeckBrowserTab = DeckBrowserTab(self.__model, settings)
        self.editor_tab: EditorTab = EditorTab(self.__model, settings)
        self.logging_tab: LoggingTab = LoggingTab(self.__model, logs, settings)
        self.cache_tab: CacheTab = CacheTab(self.__model, settings)

        tab_widget: QTabWidget = QTabWidget(self)
        tab_widget.addTab(self.deck_browser_tab, DeckBrowserTab.name)
        tab_widget.addTab(self.editor_tab, EditorTab.name)
        tab_widget.addTab(self.logging_tab, LoggingTab.name)
        tab_widget.addTab(self.cache_tab, CacheTab.name)
        tab_widget.adjustSize()

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        button_box.accepted.connect(self.__accept)
        button_box.rejected.connect(self.__reject)
        restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        restore_defaults_button.setToolTip(
            'Reset settings in this dialog to defaults. You will need to click the "OK" button to apply it.')
        restore_defaults_button.clicked.connect(self.__restore_defaults)

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(tab_widget)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setMinimumWidth(500)
        self.adjustSize()

    def refresh_from_model(self):
        self.deck_browser_tab.refresh_from_model()
        self.editor_tab.refresh_from_model()
        self.logging_tab.refresh_from_model()
        self.cache_tab.refresh_from_model()

    def __accept(self):
        ModelConverter.apply_model_to_config(self.__model, self.__config)
        self.__config_loader.write_config(self.__config)
        if aqt.mw.deckBrowser:
            aqt.mw.deckBrowser.refresh()
        self.__logs.set_level(self.__config.get_log_level())
        self.accept()
        log.info("Config accepted")

    def __reject(self):
        log.info("Config rejected")
        self.reject()

    def __restore_defaults(self):
        log.info("Restore defaults")
        defaults: Optional[dict[str, Any]] = self.__config_loader.get_defaults()
        config: Config = Config(defaults)
        ModelConverter.apply_config_to_model(self.__model, config)
        self.refresh_from_model()
