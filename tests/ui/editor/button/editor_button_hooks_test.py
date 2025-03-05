from typing import Generator

import pytest
from aqt import gui_hooks

from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.ui.editor.button.editor_button_creator import EditorButtonCreator
from note_size.ui.editor.button.editor_button_hooks import EditorButtonHooks
from note_size.ui.editor.button.editor_button_js import EditorButtonJs


@pytest.fixture
def editor_button_hooks(editor_button_creator: EditorButtonCreator, editor_button_js: EditorButtonJs,
                        settings: Settings, config: Config) -> Generator[EditorButtonHooks, None, None]:
    editor_button_hooks: EditorButtonHooks = EditorButtonHooks(
        editor_button_creator, editor_button_js, settings, config)
    yield editor_button_hooks
    editor_button_hooks.remove_hooks()


def test_setup_hooks_enabled(editor_button_hooks: EditorButtonHooks):
    __assert_no_hooks()
    editor_button_hooks.setup_hooks()
    assert gui_hooks.editor_did_init.count() == 1
    assert gui_hooks.editor_did_init_buttons.count() == 1
    assert gui_hooks.editor_did_load_note.count() == 3
    assert gui_hooks.editor_did_unfocus_field.count() == 1
    assert gui_hooks.editor_did_fire_typing_timer.count() == 1
    assert gui_hooks.webview_will_set_content.count() == 1
    assert gui_hooks.focus_did_change.count() == 1
    editor_button_hooks.remove_hooks()
    __assert_no_hooks()


def __assert_no_hooks():
    assert gui_hooks.editor_did_init.count() == 0
    assert gui_hooks.editor_did_init_buttons.count() == 0
    assert gui_hooks.editor_did_load_note.count() == 2
    assert gui_hooks.editor_did_unfocus_field.count() == 0
    assert gui_hooks.editor_did_fire_typing_timer.count() == 0
    assert gui_hooks.webview_will_set_content.count() == 0
    assert gui_hooks.focus_did_change.count() == 0
