from aqt import gui_hooks

from note_size.ui.editor.button.editor_button_hooks import EditorButtonHooks
from tests.conftest import assert_no_hooks


def test_setup_hooks_enabled(editor_button_hooks: EditorButtonHooks):
    assert_no_hooks()
    editor_button_hooks.setup_hooks()
    assert gui_hooks.editor_did_init.count() == 1
    assert gui_hooks.editor_did_init_buttons.count() == 1
    assert gui_hooks.editor_did_load_note.count() == 3
    assert gui_hooks.editor_did_unfocus_field.count() == 1
    assert gui_hooks.editor_did_fire_typing_timer.count() == 1
    assert gui_hooks.webview_will_set_content.count() == 1
    assert gui_hooks.focus_did_change.count() == 1
    editor_button_hooks.remove_hooks()
    assert_no_hooks()
