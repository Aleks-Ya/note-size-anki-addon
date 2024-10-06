import logging
from enum import Enum
from logging import Logger
from typing import NewType
from urllib.parse import urljoin

from ..config.settings import Settings

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
    }

    def __init__(self, settings: Settings) -> None:
        self.__settings: Settings = settings
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_url(self, url_type: UrlType) -> URL:
        return URL(urljoin(self.__settings.docs_base_url, self.__links[url_type]))

    def get_all_urls(self) -> dict[UrlType, URL]:
        return {url_type: self.get_url(url_type) for url_type in UrlType}
