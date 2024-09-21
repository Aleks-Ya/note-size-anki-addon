import logging
from logging import Logger
from typing import Callable, Sequence

from anki.cards import CardId
from anki.notes import NoteId
from aqt import gui_hooks
from aqt.browser import Browser, SearchContext, ItemId

from .browser_button import BrowserButton
from ..common.browser_helper import BrowserHelper

log: Logger = logging.getLogger(__name__)


class BrowserHooks:

    def __init__(self, button: BrowserButton) -> None:
        self.__button: BrowserButton = button
        self.__hook_browser_will_show: Callable[[Browser], None] = self.__add_size_button
        self.__hook_browser_did_search: Callable[[SearchContext], None] = self.__update_button
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.browser_will_show.append(self.__hook_browser_will_show)
        gui_hooks.browser_did_search.append(self.__hook_browser_did_search)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.browser_will_show.remove(self.__hook_browser_will_show)
        gui_hooks.browser_did_search.remove(self.__hook_browser_did_search)
        log.info(f"{self.__class__.__name__} are removed")

    def __add_size_button(self, browser: Browser) -> None:
        browser.form.gridLayout.addWidget(self.__button, 0, 2)

    def __update_button(self, context: SearchContext) -> None:
        item_ids: Sequence[ItemId] = context.ids
        if BrowserHelper.is_notes_mode(context):
            note_ids: Sequence[NoteId] = item_ids
            self.__button.show_notes_size(note_ids)
        else:
            card_ids: Sequence[CardId] = item_ids
            self.__button.show_cards_size(card_ids)
