import logging
from logging import Logger
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout, QWidget, Qt

from .widgets import CheckboxWithInfo
from ..settings import Settings
from ...config.ui.ui_model import UiModel

log: Logger = logging.getLogger(__name__)


class CacheTab(QWidget):
    name: str = "Cache"

    def __init__(self, model: UiModel, settings: Settings) -> None:
        super().__init__()
        self.__model: UiModel = model
        warmup_enabled_url: str = urljoin(settings.docs_base_url, "description/configuration.md#warmup-enabled")
        self.__enable_warmup_checkbox: CheckboxWithInfo = CheckboxWithInfo(
            "Enable cache warm-up", warmup_enabled_url, settings)
        self.__enable_warmup_checkbox.add_checkbox_listener(self.__on_warmup_checkbox_state_changed)
        store_cache_to_file_enabled_url: str = urljoin(settings.docs_base_url,
                                                       "description/configuration.md#store-cache-on-disk")
        self.__store_cache_to_file_checkbox: CheckboxWithInfo = CheckboxWithInfo(
            "Store cache in file on exit", store_cache_to_file_enabled_url, settings)
        self.__store_cache_to_file_checkbox.add_checkbox_listener(self.__on_store_to_file_checkbox_state_changed)
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.__enable_warmup_checkbox)
        layout.addLayout(self.__store_cache_to_file_checkbox)
        self.setLayout(layout)

    def refresh_from_model(self):
        self.__enable_warmup_checkbox.set_checked(self.__model.cache_warmup_enabled)
        self.__store_cache_to_file_checkbox.set_checked(self.__model.store_cache_in_file_enabled)

    def __on_warmup_checkbox_state_changed(self, cache_warm_up_enabled: bool):
        self.__model.cache_warmup_enabled = cache_warm_up_enabled

    def __on_store_to_file_checkbox_state_changed(self, store_cache_in_file_enabled: bool):
        self.__model.store_cache_in_file_enabled = store_cache_in_file_enabled
