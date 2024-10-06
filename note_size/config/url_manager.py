import logging
from enum import Enum
from logging import Logger
from typing import NewType
from urllib.parse import urljoin

log: Logger = logging.getLogger(__name__)

URL = NewType("URL", str)


class UrlType(Enum):
    CONFIGURATION_DECK_BROWSER_SHOW_COLLECTION_SIZE = 1
    CONFIGURATION_BROWSER_SHOW_FOUND_NOTES_SIZE = 2
    CONFIGURATION_EDITOR_SIZE_BUTTON_ENABLED = 3
    CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_ENABLED = 4
    CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_LEVELS = 5
    CONFIGURATION_LOGGING_LEVEL = 6
    CONFIGURATION_CACHE_WARM_UP_ENABLED = 7
    CONFIGURATION_CACHE_STORE_ON_DISK = 8
    INFO_USER_MANUAL = 9
    INFO_ADDON_PAGE = 10
    INFO_FORUM = 11
    INFO_CHANGE_LOG = 12
    INFO_BUG_TRACKER = 13
    INFO_GITHUB = 14


class UrlManager:
    __links: dict[UrlType, URL] = {
        UrlType.CONFIGURATION_BROWSER_SHOW_FOUND_NOTES_SIZE: "docs/configuration.md#show-size-of-notes-found-in-browser",
        UrlType.CONFIGURATION_CACHE_WARM_UP_ENABLED: "docs/configuration.md#enable-cache-warm-up",
        UrlType.CONFIGURATION_CACHE_STORE_ON_DISK: "docs/configuration.md#store-cache-in-file-on-exit",
        UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_ENABLED: "docs/configuration.md#color---enabled",
        UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_LEVELS: "docs/configuration.md#color---levels",
        UrlType.CONFIGURATION_DECK_BROWSER_SHOW_COLLECTION_SIZE: "docs/configuration.md#show-collection-size",
        UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_ENABLED: "docs/configuration.md#enabled",
        UrlType.CONFIGURATION_LOGGING_LEVEL: "docs/configuration.md#logging",
        UrlType.INFO_USER_MANUAL: "docs/user-manual.md",
        UrlType.INFO_ADDON_PAGE: "https://ankiweb.net/shared/info/1188705668",
        UrlType.INFO_FORUM: "https://forums.ankiweb.net/t/note-size-addon-support/46001",
        UrlType.INFO_CHANGE_LOG: "https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/CHANGELOG.md",
        UrlType.INFO_BUG_TRACKER: "https://github.com/Aleks-Ya/note-size-anki-addon/issues",
        UrlType.INFO_GITHUB: "https://github.com/Aleks-Ya/note-size-anki-addon",
    }

    def __init__(self) -> None:
        self.docs_base_url: str = "https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/"
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_url(self, url_type: UrlType) -> URL:
        link: URL = self.__links[url_type]
        if link.startswith("docs/"):
            link = URL(urljoin(self.docs_base_url, link))
        return link

    def get_all_urls(self) -> dict[UrlType, URL]:
        return {url_type: self.get_url(url_type) for url_type in UrlType}
