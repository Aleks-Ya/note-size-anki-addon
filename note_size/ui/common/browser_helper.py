from aqt.browser import SearchContext


class BrowserHelper:
    @staticmethod
    def is_notes_mode(context: SearchContext) -> bool:
        # Method "aqt.browser.table.table.Table.is_notes_mode" doesn't show correct state after toggling the switch
        # noinspection PyProtectedMember
        return context.browser._switch.isChecked()
