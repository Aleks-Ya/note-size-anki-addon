import datetime
import logging
from logging import Logger

from aqt import gui_hooks

from ..types import SizeStr
from ..cache.item_id_cache import ItemIdCache
from ..cache.media_cache import MediaCache
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class DeckBrowserHooks:
    __my_python_action: str = "refresh-collection-size"

    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache):
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.append(self.__on_action)
        # gui_hooks.webview_did_receive_js_message.append(self.__on_event)
        log.info(f"{self.__class__.__name__} are set")

    # noinspection PyUnresolvedReferences
    def __on_action(self, _: 'aqt.deckbrowser.DeckBrowser', content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        on_click_js: str = "document.getElementById('updated').textContent=new Date().toLocaleString()"
        button: str = f"""<button onclick="{on_click_js}">Refresh</button>"""
        collection_size: SizeStr = SizeStr(SizeFormatter.bytes_to_str(self.__item_id_cache.get_total_texts_size()))
        media_size: SizeStr = SizeStr(SizeFormatter.bytes_to_str(self.__media_cache.get_total_files_size()))
        content.stats += ("\n<div>Custom text in statistics. "
                          f"Updated: <span id='updated'>{datetime.datetime.now().replace(microsecond=0)}</span>"
                          f"{button}</div>"
                          f"<div>Collection: {collection_size}</div>"
                          f"<div>Media: {media_size}</div>"
                          )

        log.info(f"DeckBrowserContent stats (edited): {content.stats}\n\n")

    # def __on_event(self, handled: tuple[bool, Any], message: str, _: Any) -> tuple[bool, Any]:
    #     showInfo(f"did_receive_js_message: message={message}")
    #     if message == self.__my_python_action:
    #         showInfo(f"Received my event: message={message}")
    #         return True, None
    #     return handled
    #
    #
    # def __menu_item_action(self) -> None:
    #     showInfo('You clicked "Send pycmd event"')
    #     mw.web.eval(f"pycmd('{__my_python_action}')")
