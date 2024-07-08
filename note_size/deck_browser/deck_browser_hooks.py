import logging
from logging import Logger
from pathlib import Path
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
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.append(self.__hook_deck_browser_will_render_content)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.deck_browser_will_render_content.remove(self.__hook_deck_browser_will_render_content)
        log.info(f"{self.__class__.__name__} are removed")

    # noinspection PyUnresolvedReferences
    def __on_action(self, _: 'aqt.deckbrowser.DeckBrowser',
                    content: 'aqt.deckbrowser.DeckBrowserContent') -> None:
        collection_size: SizeStr = SizeFormatter.bytes_to_str(self.__collection_size())
        media_size: SizeStr = SizeFormatter.bytes_to_str(self.__media_size())
        total_size: SizeStr = SizeFormatter.bytes_to_str(self.__total_size())
        collection_span: str = (
            f"<span id='{DeckBrowserHooks.__collection_size_id}' title='Size of note fields without media' "
            f"style='{DeckBrowserHooks.__code_style}'>{collection_size}</span>")
        media_span: str = (f"<span id='{DeckBrowserHooks.__media_size_id}' title='Size of media files without fields' "
                           f"style='{DeckBrowserHooks.__code_style}'>{media_size}</span>")
        total_span: str = (f"<span id='{DeckBrowserHooks.__total_size_id}' title='Size of note fields with media' "
                           f"style='{DeckBrowserHooks.__code_style}'>{total_size}</span>")
        content.stats += (f"<div>Collection:&nbsp;{collection_span}&nbsp;&nbsp;&nbsp;"
                          f"Media:&nbsp;{media_span}&nbsp;&nbsp;&nbsp;"
                          f"Total:&nbsp;{total_span}&nbsp;&nbsp;&nbsp;</div>")
        log.info(f"DeckBrowserContent stats (edited): {content.stats}\n\n")

    def __media_size(self) -> SizeBytes:
        return self.__media_cache.get_total_files_size()

    @staticmethod
    def __collection_size() -> SizeBytes:
        collection_file_path: Path = Path(mw.pm.profileFolder(), "collection.anki2")
        return SizeBytes(collection_file_path.stat().st_size)

    def __total_size(self) -> SizeBytes:
        return SizeBytes(self.__collection_size() + self.__media_size())
