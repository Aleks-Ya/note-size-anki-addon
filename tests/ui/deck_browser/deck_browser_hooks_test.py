from typing import Generator

import pytest
from aqt import gui_hooks

from note_size.ui.deck_browser.deck_browser_hooks import DeckBrowserHooks
from note_size.ui.deck_browser.deck_browser_js import DeckBrowserJs
from note_size.ui.deck_browser.deck_browser_updater import DeckBrowserUpdater


@pytest.fixture
def deck_browser_hooks(deck_browser_updater: DeckBrowserUpdater,
                       deck_browser_js: DeckBrowserJs) -> Generator[DeckBrowserHooks, None, None]:
    deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(deck_browser_updater, deck_browser_js)
    yield deck_browser_hooks
    deck_browser_hooks.remove_hooks()


def test_setup_hooks(deck_browser_hooks: DeckBrowserHooks):
    assert gui_hooks.deck_browser_will_render_content.count() == 0
    assert gui_hooks.webview_did_receive_js_message.count() == 0
    deck_browser_hooks.setup_hooks()
    assert gui_hooks.deck_browser_will_render_content.count() == 1
    assert gui_hooks.webview_did_receive_js_message.count() == 1
    deck_browser_hooks.remove_hooks()
    assert gui_hooks.deck_browser_will_render_content.count() == 0
    assert gui_hooks.webview_did_receive_js_message.count() == 0
