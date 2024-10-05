import pytest
from aqt.qt import QDesktopServices
from pytestqt.qtbot import QtBot

from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.ui.config.browser_tab import BrowserTab
from note_size.ui.config.model_converter import ModelConverter
from note_size.ui.config.ui_model import UiModel
from note_size.ui.config.widgets import CheckboxWithInfo


@pytest.fixture
def browser_tab(qtbot: QtBot, config: Config, desktop_services: QDesktopServices, settings: Settings,
                ui_model: UiModel) -> BrowserTab:
    ModelConverter.apply_config_to_model(ui_model, config)
    browser_tab: BrowserTab = BrowserTab(ui_model, desktop_services, settings)
    browser_tab.refresh_from_model()
    browser_tab.show()
    qtbot.addWidget(browser_tab)
    return browser_tab


@pytest.fixture
def show_notes_size_checkbox(browser_tab: BrowserTab) -> CheckboxWithInfo:
    return browser_tab.findChildren(CheckboxWithInfo)[0]


def test_default_state(show_notes_size_checkbox: CheckboxWithInfo):
    assert show_notes_size_checkbox.is_checked()
