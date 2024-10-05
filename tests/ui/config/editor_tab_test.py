import pytest
from aqt.qt import QDesktopServices
from pytestqt.qtbot import QtBot

from note_size.config.config import Config
from note_size.config.level_parser import LevelParser
from note_size.config.settings import Settings
from note_size.ui.config.editor_tab import EditorTab
from note_size.ui.config.model_converter import ModelConverter
from note_size.ui.config.ui_model import UiModel
from note_size.ui.config.widgets import CheckboxWithInfo


@pytest.fixture
def editor_tab(qtbot: QtBot, config: Config, desktop_services: QDesktopServices, settings: Settings,
               ui_model: UiModel, level_parser: LevelParser) -> EditorTab:
    ModelConverter.apply_config_to_model(ui_model, config)
    editor_tab: EditorTab = EditorTab(ui_model, desktop_services, level_parser, settings)
    editor_tab.refresh_from_model()
    editor_tab.show()
    qtbot.addWidget(editor_tab)
    return editor_tab


@pytest.fixture
def show_note_size_checkbox(editor_tab: EditorTab) -> CheckboxWithInfo:
    return editor_tab.findChildren(CheckboxWithInfo)[0]


def test_default_state(show_note_size_checkbox: CheckboxWithInfo):
    assert show_note_size_checkbox.is_checked()
