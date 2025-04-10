from aqt import gui_hooks

from note_size.ui.theme.theme_hooks import ThemeHooks
from tests.conftest import assert_no_hooks


def test_setup_hooks_enabled(theme_hooks: ThemeHooks):
    assert_no_hooks()
    original_count: int = gui_hooks.theme_did_change.count()  # Fixtures "editor_add_mode" and "editor_edit_mode" add their own hooks
    theme_hooks.setup_hooks()
    assert gui_hooks.theme_did_change.count() == original_count + 1
    theme_hooks.remove_hooks()
    assert_no_hooks()
    assert gui_hooks.theme_did_change.count() == original_count
