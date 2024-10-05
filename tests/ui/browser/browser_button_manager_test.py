from aqt.browser import Browser

from note_size.config.config import Config
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


def test_on_config_changed(browser_button_manager: BrowserButtonManager, browser: Browser, config: Config):
    config.add_listener(browser_button_manager)
    button: BrowserButton = browser_button_manager.create_browser_button(browser)
    assert button.isHidden()

    assert config.get_browser_show_found_notes_size()
    config.fire_config_changed()
    assert not button.isHidden()

    config.set_browser_show_found_notes_size(False)
    config.fire_config_changed()
    assert button.isHidden()


def test_on_config_changed_no_button(browser_button_manager: BrowserButtonManager, browser: Browser, config: Config):
    config.add_listener(browser_button_manager)
    assert not browser_button_manager.get_current_button()
    config.fire_config_changed()
