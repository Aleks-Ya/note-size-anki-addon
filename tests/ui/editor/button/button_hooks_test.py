import pytest
from aqt import gui_hooks

from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.ui.details_dialog.details_dialog import DetailsDialog
from note_size.ui.editor.button.button_formatter import ButtonFormatter
from note_size.ui.editor.button.button_hooks import ButtonHooks


@pytest.fixture
def button_hooks(settings: Settings, config: Config, button_formatter: ButtonFormatter,
                 details_dialog: DetailsDialog) -> ButtonHooks:
    button_hooks = ButtonHooks(button_formatter, details_dialog, settings, config)
    yield button_hooks
    button_hooks.remove_hooks()


def test_setup_hooks_enabled(button_hooks: ButtonHooks):
    __assert_no_hooks()
    button_hooks.setup_hooks()
    assert gui_hooks.editor_did_init.count() == 1
    assert gui_hooks.editor_did_init_buttons.count() == 1
    assert gui_hooks.editor_did_load_note.count() == 3
    assert gui_hooks.editor_did_unfocus_field.count() == 1
    assert gui_hooks.editor_did_fire_typing_timer.count() == 1
    assert gui_hooks.webview_will_set_content.count() == 1
    assert gui_hooks.focus_did_change.count() == 1
    button_hooks.remove_hooks()
    __assert_no_hooks()


def __assert_no_hooks():
    assert gui_hooks.editor_did_init.count() == 0
    assert gui_hooks.editor_did_init_buttons.count() == 0
    assert gui_hooks.editor_did_load_note.count() == 2
    assert gui_hooks.editor_did_unfocus_field.count() == 0
    assert gui_hooks.editor_did_fire_typing_timer.count() == 0
    assert gui_hooks.webview_will_set_content.count() == 0
    assert gui_hooks.focus_did_change.count() == 0
