import pytest
from aqt.qt import QCheckBox
from aqt.qt import Qt, QDesktopServices
from pytestqt.qtbot import QtBot
from PyQtPath.path_chain_pyqt6 import path

from note_size.cache.cache_initializer import CacheInitializer
from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.config.url_manager import UrlManager
from note_size.ui.config.cache_tab import CacheTab
from note_size.ui.config.model_converter import ModelConverter
from note_size.ui.config.ui_model import UiModel
from note_size.ui.config.widgets import CheckboxWithInfo


@pytest.fixture
def cache_tab(qtbot: QtBot, config: Config, cache_initializer: CacheInitializer, desktop_services: QDesktopServices,
              settings: Settings, ui_model: UiModel, url_manager: UrlManager) -> CacheTab:
    ModelConverter.apply_config_to_model(ui_model, config)
    cache_tab: CacheTab = CacheTab(ui_model, cache_initializer, desktop_services, url_manager, settings)
    cache_tab.refresh_from_model()
    # noinspection PyUnresolvedReferences
    cache_tab.show()
    qtbot.addWidget(cache_tab)
    return cache_tab


@pytest.fixture
def enable_warmup_checkbox(cache_tab: CacheTab) -> CheckboxWithInfo:
    return cache_tab.findChildren(CheckboxWithInfo)[0]


@pytest.fixture
def store_cache_to_file_checkbox(cache_tab: CacheTab) -> CheckboxWithInfo:
    return cache_tab.findChildren(CheckboxWithInfo)[1]


def test_default_state(enable_warmup_checkbox: CheckboxWithInfo, store_cache_to_file_checkbox: CheckboxWithInfo):
    assert enable_warmup_checkbox.is_checked()
    assert store_cache_to_file_checkbox.is_checked()


def test_enable_warmup_checkbox(cache_tab: CacheTab, enable_warmup_checkbox: CheckboxWithInfo, qtbot: QtBot):
    assert enable_warmup_checkbox.is_checked()
    checkbox: QCheckBox = path(cache_tab).checkbox().get()
    qtbot.mouseClick(checkbox, Qt.MouseButton.LeftButton)
    assert not enable_warmup_checkbox.is_checked()
    qtbot.mouseClick(checkbox, Qt.MouseButton.LeftButton)
    assert enable_warmup_checkbox.is_checked()
