from typing import Generator

import pytest
from aqt import gui_hooks

from note_size.config.config import Config
from note_size.ui.config.config_ui import ConfigUi
from note_size.ui.deck_browser.collection_size_formatter import CollectionSizeFormatter
from note_size.ui.deck_browser.deck_browser_hooks import DeckBrowserHooks


@pytest.fixture
def deck_browser_hooks(config: Config, collection_size_formatter: CollectionSizeFormatter,
                       config_ui: ConfigUi) -> Generator[DeckBrowserHooks, None, None]:
    deck_browser_hooks: DeckBrowserHooks = DeckBrowserHooks(collection_size_formatter, config, config_ui)
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
