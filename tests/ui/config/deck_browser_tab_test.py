import pytest
from aqt.qt import QDesktopServices
from pytestqt.qtbot import QtBot

from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.ui.config.deck_browser_tab import DeckBrowserTab
from note_size.ui.config.model_converter import ModelConverter
from note_size.ui.config.ui_model import UiModel
from note_size.ui.config.widgets import CheckboxWithInfo


@pytest.fixture
def deck_browser_tab(qtbot: QtBot, config: Config, desktop_services: QDesktopServices, settings: Settings,
                     ui_model: UiModel) -> DeckBrowserTab:
    ModelConverter.apply_config_to_model(ui_model, config)
    deck_browser_tab: DeckBrowserTab = DeckBrowserTab(ui_model, desktop_services, settings)
    deck_browser_tab.refresh_from_model()
    deck_browser_tab.show()
    qtbot.addWidget(deck_browser_tab)
    return deck_browser_tab


@pytest.fixture
def show_collection_size_checkbox(deck_browser_tab: DeckBrowserTab) -> CheckboxWithInfo:
    return deck_browser_tab.findChildren(CheckboxWithInfo)[0]


def test_default_state(show_collection_size_checkbox: CheckboxWithInfo):
    assert show_collection_size_checkbox.is_checked()
