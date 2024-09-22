from note_size.ui.browser.browser_button import BrowserButton
from note_size.ui.browser.browser_button_manager import BrowserButtonManager


def test_create_browser_button(browser_button_manager: BrowserButtonManager):
    button: BrowserButton = browser_button_manager.create_browser_button()
    assert button.text() == ""


def test_get_current_button(browser_button_manager: BrowserButtonManager):
    button1: BrowserButton = browser_button_manager.create_browser_button()
    button2: BrowserButton = browser_button_manager.get_current_button()
    button3: BrowserButton = browser_button_manager.create_browser_button()
    assert button1 == button2
    assert button2 != button3
