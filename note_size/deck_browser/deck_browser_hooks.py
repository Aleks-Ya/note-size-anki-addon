import datetime
import logging
from logging import Logger
from typing import Callable, Any

from aqt import gui_hooks, mw

from ..types import SizeStr, SizeBytes
from ..cache.item_id_cache import ItemIdCache
from ..cache.media_cache import MediaCache
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class DeckBrowserHooks:
    __my_python_action: str = "refresh-collection-size"
    __collection_size_id: str = "collection_size"
    __media_size_id: str = "media_size"
    __total_size_id: str = "total_size"
    __button_id: str = "refresh_button"
    __code_style: str = "font-family:Consolas,monospace"

    def __init__(self, media_cache: MediaCache, item_id_cache: ItemIdCache):
        self.__media_cache: MediaCache = media_cache
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__hook_deck_browser_will_render_content: Callable[[Any, Any], None] = self.__on_action
        self.__hook_webview_did_receive_js_message = self.__on_event
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.append(self.__hook_deck_browser_will_render_content)
        gui_hooks.webview_did_receive_js_message.append(self.__hook_webview_did_receive_js_message)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.remove(self.__hook_deck_browser_will_render_content)
        gui_hooks.webview_did_receive_js_message.remove(self.__hook_webview_did_receive_js_message)
        log.info(f"{self.__class__.__name__} are removed")

    # noinspection PyUnresolvedReferences
    def __on_action(self, _: 'aqt.deckbrowser.DeckBrowser',
                    content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        on_click_js: str = f"pycmd('{DeckBrowserHooks.__my_python_action}')"
        button_title: str = "Update"
        if self.__item_id_cache.is_initialized():
            collection_size: SizeStr = self.__collection_size()
            collection_title: str = "Size of note fields without media"
            media_size: SizeStr = self.__media_size()
            media_title: str = "Size of media files without fields"
            total_size: SizeStr = self.__total_size()
            total_title: str = "Size of note fields with media"
        else:
            collection_size: str = "⏳"
            collection_title: str = "Calculating..."
            media_size: str = collection_size
            media_title: str = collection_title
            total_size: str = collection_size
            total_title: str = collection_title
        collection_span: str = (f"<span id='{DeckBrowserHooks.__collection_size_id}' title='{collection_title}' "
                                f"style='{DeckBrowserHooks.__code_style}'>{collection_size}</span>")
        media_span: str = (f"<span id='{DeckBrowserHooks.__media_size_id}' title='{media_title}' "
                           f"style='{DeckBrowserHooks.__code_style}'>{media_size}</span>")
        total_span: str = (f"<span id='{DeckBrowserHooks.__total_size_id}' title='{total_title}' "
                           f"style='{DeckBrowserHooks.__code_style}'>{total_size}</span>")
        button: str = (f"<button id='{DeckBrowserHooks.__button_id}' title='{button_title}' "
                       f"""style="padding: 2px 5px;" onclick="{on_click_js}">⟳</button>""")
        content.stats += (f"<div style='align-items: center; display: flex; justify-content: center;'>"
                          f"Collection:&nbsp;{collection_span}&nbsp;&nbsp;&nbsp;"
                          f"Media:&nbsp;{media_span}&nbsp;&nbsp;&nbsp;"
                          f"Total:&nbsp;{total_span}&nbsp;&nbsp;&nbsp;"
                          f"{button}</div>")
        log.info(f"DeckBrowserContent stats (edited): {content.stats}\n\n")

    def __media_size(self) -> SizeStr:
        return SizeFormatter.bytes_to_str(self.__media_cache.get_total_files_size())

    def __collection_size(self) -> SizeStr:
        return SizeFormatter.bytes_to_str(self.__item_id_cache.get_total_texts_size())

    def __total_size(self) -> SizeStr:
        total_size: SizeBytes = SizeBytes(self.__item_id_cache.get_total_texts_size() +
                                          self.__media_cache.get_total_files_size())
        return SizeFormatter.bytes_to_str(total_size)

    def __on_event(self, handled: tuple[bool, Any], message: str, _: Any) -> tuple[bool, Any]:
        if message == DeckBrowserHooks.__my_python_action:
            collection_size: SizeStr = self.__collection_size()
            media_size: SizeStr = self.__media_size()
            total_size: SizeStr = self.__total_size()
            button_title: str = f"Updated {datetime.datetime.now().time().replace(microsecond=0)}"
            on_click_js: str = (
                f"document.getElementById('{DeckBrowserHooks.__collection_size_id}').textContent='{collection_size}';"
                f"document.getElementById('{DeckBrowserHooks.__media_size_id}').textContent='{media_size}';"
                f"document.getElementById('{DeckBrowserHooks.__total_size_id}').textContent='{total_size}';"
                f"document.getElementById('{DeckBrowserHooks.__button_id}').title='{button_title}';")
            mw.web.eval(on_click_js)
            return True, None
        return handled
