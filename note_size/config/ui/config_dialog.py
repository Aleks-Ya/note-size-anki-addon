import logging
from logging import Logger
from typing import Optional, Any

import aqt
from aqt.qt import QDialog, QVBoxLayout, QDialogButtonBox, QTabWidget, QPushButton

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
        self.__update_model_from_config(model, config)
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
        self.__config.set_deck_browser_show_collection_size(self.__model.deck_browser_show_collection_size)
        self.__config.set_size_button_enabled(self.__model.size_button_enabled)
        self.__config.set_size_button_details_formatter_max_filename_length(
            self.__model.size_button_details_formatter_max_filename_length)
        self.__config.set_size_button_details_formatter_max_files_to_show(
            self.__model.size_button_details_formatter_max_files_to_show)
        self.__config.set_size_button_color_enabled(self.__model.size_button_color_enabled)
        self.__config.set_size_button_color_levels(self.__model.size_button_color_levels)
        self.__config.set_log_level(self.__model.log_level)
        self.__config.set_cache_warmup_enabled(self.__model.cache_warmup_enabled)
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
        self.__update_model_from_config(self.__model, config)
        self.refresh_from_model()

    @staticmethod
    def __update_model_from_config(model: UiModel, config: Config):
        model.deck_browser_show_collection_size = config.get_deck_browser_show_collection_size()
        model.size_button_enabled = config.get_size_button_enabled()
        model.size_button_details_formatter_max_filename_length \
            = config.get_size_button_details_formatter_max_filename_length()
        model.size_button_details_formatter_max_files_to_show \
            = config.get_size_button_details_formatter_max_files_to_show()
        model.size_button_color_enabled = config.get_size_button_color_enabled()
        model.size_button_color_levels = config.get_size_button_color_levels()
        model.log_level = config.get_log_level()
        model.cache_warmup_enabled = config.get_cache_warmup_enabled()
