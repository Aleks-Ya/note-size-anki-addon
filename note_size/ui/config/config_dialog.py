import logging
from logging import Logger
from typing import Optional, Any

from aqt.deckbrowser import DeckBrowser
from aqt.qt import QDialog, QVBoxLayout, QDialogButtonBox, QTabWidget, QPushButton, QDesktopServices
from aqt.theme import ThemeManager

from .browser_tab import BrowserTab
from .model_converter import ModelConverter
from ...cache.cache_initializer import CacheInitializer
from ...config.config import Config
from ...config.level_parser import LevelParser
from ...config.url_manager import UrlManager
from ...log.logs import Logs
from ...config.config_loader import ConfigLoader
from .ui_model import UiModel
from ...config.settings import Settings
from .deck_browser_tab import DeckBrowserTab
from .editor_tab import EditorTab
from .logging_tab import LoggingTab
from .cache_tab import CacheTab

log: Logger = logging.getLogger(__name__)


class ConfigDialog(QDialog):
    def __init__(self, config: Config, config_loader: ConfigLoader, model: UiModel, logs: Logs,
                 cache_initializer: CacheInitializer, desktop_services: QDesktopServices, level_parser: LevelParser,
                 url_manager: UrlManager, deck_browser: DeckBrowser, theme_manager: ThemeManager,
                 settings: Settings):
        super().__init__(parent=None)
        self.__config: Config = config
        self.__model: UiModel = model
        self.__logs: Logs = logs
        self.__config_loader: ConfigLoader = config_loader
        self.__deck_browser: DeckBrowser = deck_browser
        ModelConverter.apply_config_to_model(model, config)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('"Note Size" addon configuration')

        self.__deck_browser_tab: DeckBrowserTab = DeckBrowserTab(self.__model, desktop_services, url_manager, settings)
        self.__browser_tab: BrowserTab = BrowserTab(self.__model, desktop_services, url_manager, settings)
        self.__editor_tab: EditorTab = EditorTab(self.__model, desktop_services, level_parser, url_manager,
                                                 theme_manager, settings)
        self.__logging_tab: LoggingTab = LoggingTab(self.__model, logs, desktop_services, url_manager, settings)
        self.__cache_tab: CacheTab = CacheTab(self.__model, cache_initializer, desktop_services, url_manager, settings)

        tab_widget: QTabWidget = QTabWidget(self)
        tab_widget.addTab(self.__deck_browser_tab, DeckBrowserTab.name)
        tab_widget.addTab(self.__browser_tab, BrowserTab.name)
        tab_widget.addTab(self.__editor_tab, EditorTab.name)
        tab_widget.addTab(self.__logging_tab, LoggingTab.name)
        tab_widget.addTab(self.__cache_tab, CacheTab.name)
        tab_widget.adjustSize()

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        # noinspection PyUnresolvedReferences
        button_box.accepted.connect(self.__accept)
        # noinspection PyUnresolvedReferences
        button_box.rejected.connect(self.__reject)
        restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        # noinspection PyUnresolvedReferences
        restore_defaults_button.setToolTip(
            'Reset settings in this dialog to defaults. You will need to click the "OK" button to apply it.')
        # noinspection PyUnresolvedReferences
        restore_defaults_button.clicked.connect(self.__restore_defaults)

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(tab_widget)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setMinimumWidth(600)
        self.adjustSize()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def refresh_from_model(self) -> None:
        self.__deck_browser_tab.refresh_from_model()
        self.__browser_tab.refresh_from_model()
        self.__editor_tab.refresh_from_model()
        self.__logging_tab.refresh_from_model()
        self.__cache_tab.refresh_from_model()

    def __accept(self) -> None:
        ModelConverter.apply_model_to_config(self.__model, self.__config)
        self.__config_loader.write_config(self.__config)
        self.__deck_browser.refresh()
        self.__logs.set_level(self.__config.get_log_level())
        self.accept()
        log.info("Config accepted")
        self.__config.fire_config_changed()

    def __reject(self) -> None:
        log.info("Config rejected")
        self.reject()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
        defaults: Optional[dict[str, Any]] = self.__config_loader.get_defaults()
        config: Config = Config(defaults)
        ModelConverter.apply_config_to_model(self.__model, config)
        self.refresh_from_model()
        self.__config.fire_config_changed()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
