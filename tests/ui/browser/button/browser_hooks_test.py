from aqt import gui_hooks

from note_size.ui.browser.button.browser_hooks import BrowserHooks


def test_setup_hooks(browser_hooks: BrowserHooks):
    assert gui_hooks.browser_will_show.count() == 0
    assert gui_hooks.browser_did_search.count() == 0
    browser_hooks.setup_hooks()
    assert gui_hooks.browser_will_show.count() == 1
    assert gui_hooks.browser_did_search.count() == 1
    browser_hooks.remove_hooks()
    assert gui_hooks.browser_will_show.count() == 0
    assert gui_hooks.browser_did_search.count() == 0
