import pytest
from aqt.qt import QDesktopServices
from pytestqt.qtbot import QtBot

from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.config.url_manager import UrlManager
from note_size.log.logs import Logs
from note_size.ui.config.logging_tab import LoggingTab
from note_size.ui.config.model_converter import ModelConverter
from note_size.ui.config.ui_model import UiModel
from note_size.ui.config.widgets import TitledComboBoxLayout


@pytest.fixture
def logging_tab(qtbot: QtBot, config: Config, desktop_services: QDesktopServices, settings: Settings,
                ui_model: UiModel, logs: Logs, url_manager: UrlManager) -> LoggingTab:
    ModelConverter.apply_config_to_model(ui_model, config)
    logging_tab: LoggingTab = LoggingTab(ui_model, logs, desktop_services, url_manager, settings)
    logging_tab.refresh_from_model()
    # noinspection PyUnresolvedReferences
    logging_tab.show()
    qtbot.addWidget(logging_tab)
    return logging_tab


@pytest.fixture
def log_level_combo_box(logging_tab: LoggingTab) -> TitledComboBoxLayout:
    return logging_tab.findChildren(TitledComboBoxLayout)[0]


def test_default_state(log_level_combo_box: TitledComboBoxLayout):
    assert log_level_combo_box
