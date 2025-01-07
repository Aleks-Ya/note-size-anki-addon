from aqt.browser import Browser


class BrowserHelper:
    @staticmethod
    def is_notes_mode(browser: Browser) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return browser._switch.isChecked()
