import logging
from logging import Logger
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout, QWidget, Qt, QPushButton

from .widgets import CheckboxWithInfo
from ..settings import Settings
from ...cache.cache_updater import CacheUpdater
from ...config.ui.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class CacheTab(QWidget):
    name: str = "Cache"

    def __init__(self, model: UiModel, cache_updater: CacheUpdater, settings: Settings) -> None:
        super().__init__()
        self.__model: UiModel = model
        self.__cache_updater: CacheUpdater = cache_updater
        warmup_enabled_url: str = urljoin(settings.docs_base_url, "description/configuration.md#warmup-enabled")
        self.__enable_warmup_checkbox: CheckboxWithInfo = CheckboxWithInfo(
            "Enable cache warm-up", warmup_enabled_url, settings)
        self.__enable_warmup_checkbox.add_checkbox_listener(self.__on_warmup_checkbox_state_changed)
        store_cache_to_file_enabled_url: str = urljoin(settings.docs_base_url,
                                                       "description/configuration.md#store-cache-on-disk")
        self.__store_cache_to_file_checkbox: CheckboxWithInfo = CheckboxWithInfo(
            "Store cache in file on exit", store_cache_to_file_enabled_url, settings)
        self.__store_cache_to_file_checkbox.add_checkbox_listener(self.__on_store_to_file_checkbox_state_changed)
        refresh_cache_button: QPushButton = QPushButton("Refresh cache")
        refresh_cache_button.setFixedWidth(refresh_cache_button.sizeHint().width())
        refresh_cache_button.clicked.connect(self.__refresh_caches)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__enable_warmup_checkbox)
        layout.addLayout(self.__store_cache_to_file_checkbox)
        layout.addWidget(refresh_cache_button)
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__enable_warmup_checkbox.set_checked(self.__model.cache_warmup_enabled)
        self.__store_cache_to_file_checkbox.set_checked(self.__model.store_cache_in_file_enabled)

    def __on_warmup_checkbox_state_changed(self, _: int):
        self.__model.cache_warmup_enabled = self.__enable_warmup_checkbox.is_checked()

    def __on_store_to_file_checkbox_state_changed(self, _: int):
        self.__model.store_cache_in_file_enabled = self.__store_cache_to_file_checkbox.is_checked()

    def __refresh_caches(self):
        self.__cache_updater.refresh_caches(parent=self)
