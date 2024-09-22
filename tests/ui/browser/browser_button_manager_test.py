from aqt.browser import Browser

from note_size.ui.browser.browser_button import BrowserButton
from note_size.ui.browser.browser_button_manager import BrowserButtonManager


def test_create_browser_button(browser_button_manager: BrowserButtonManager, browser: Browser):
    button: BrowserButton = browser_button_manager.create_browser_button(browser)
    assert button.text() == ""


def test_get_current_button(browser_button_manager: BrowserButtonManager, browser: Browser):
    button1: BrowserButton = browser_button_manager.create_browser_button(browser)
    button2: BrowserButton = browser_button_manager.get_current_button()
    button3: BrowserButton = browser_button_manager.create_browser_button(browser)
    assert button1 == button2
    assert button2 != button3
