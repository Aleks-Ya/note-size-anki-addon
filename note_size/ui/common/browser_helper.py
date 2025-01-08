import logging
from logging import Logger

from aqt.browser import Browser

log: Logger = logging.getLogger(__name__)


class BrowserHelper:
    @staticmethod
    def is_notes_mode(browser: Browser) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        result: bool = browser._switch.isChecked()
        log.debug(f"Is browser in notes mode: {result}")
        return result
