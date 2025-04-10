from aqt import gui_hooks

from note_size.ui.deck_browser.deck_browser_hooks import DeckBrowserHooks
from tests.conftest import assert_no_hooks


def test_setup_hooks(deck_browser_hooks: DeckBrowserHooks):
    assert_no_hooks()
    deck_browser_hooks.setup_hooks()
    assert gui_hooks.deck_browser_will_render_content.count() == 1
    assert gui_hooks.webview_did_receive_js_message.count() == 1
    deck_browser_hooks.remove_hooks()
    assert_no_hooks()
