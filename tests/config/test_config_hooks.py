import pytest
from aqt import gui_hooks, QDesktopServices

from note_size.config.config_hooks import ConfigHooks
from note_size.config.config_ui import ConfigUi


@pytest.fixture
def config_hooks(config_ui: ConfigUi, desktop_services: QDesktopServices) -> ConfigHooks:
    config_hooks = ConfigHooks(config_ui, desktop_services)
    yield config_hooks
    config_hooks.remove_hooks()


def test_setup_hooks(config_hooks: ConfigHooks):
    assert 0 == gui_hooks.main_window_did_init.count()
    assert 0 == gui_hooks.browser_will_show.count()

    config_hooks.setup_hooks()
    assert 1 == gui_hooks.main_window_did_init.count()
    assert 1 == gui_hooks.browser_will_show.count()

    config_hooks.remove_hooks()
    assert 0 == gui_hooks.main_window_did_init.count()
    assert 0 == gui_hooks.browser_will_show.count()
