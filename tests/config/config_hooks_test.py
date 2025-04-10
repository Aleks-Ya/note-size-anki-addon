from aqt import gui_hooks

from note_size.config.config_hooks import ConfigHooks
from tests.conftest import assert_no_hooks


def test_setup_hooks(config_hooks: ConfigHooks):
    assert_no_hooks()
    config_hooks.setup_hooks()
    assert 1 == gui_hooks.main_window_did_init.count()
    assert 1 == gui_hooks.browser_will_show.count()
    config_hooks.remove_hooks()
    assert_no_hooks()
