from anki.cards import CardId, Card
from anki.collection import Collection
from anki.notes import Note
from aqt.browser import Browser

from note_size.ui.browser.browser_button import BrowserButton
from note_size.ui.browser.browser_button_manager import BrowserButtonManager
from tests.data import Data


def test_show_notes_size(browser_button_manager: BrowserButtonManager, td: Data, browser: Browser):
    button: BrowserButton = browser_button_manager.create_browser_button(browser)
    note1: Note = td.create_note_with_files()
    note2: Note = td.create_note_without_files()
    button.show_notes_size([note1.id, note2.id])
    assert button.text() == "213 B"


def test_show_cards_size(col: Collection, browser_button_manager: BrowserButtonManager, td: Data, browser: Browser):
    button: BrowserButton = browser_button_manager.create_browser_button(browser)
    card1: Card = td.create_card_with_files()
    card2: Card = td.create_card_without_files()
    card_ids: list[CardId] = [card1.id, card2.id]
    button.show_cards_size(card_ids)
    assert button.text() == "213 B"
