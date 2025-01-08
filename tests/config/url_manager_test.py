from urllib.parse import urlparse, ParseResult

import pytest
import requests
from bs4 import BeautifulSoup
from requests import Response

from note_size.config.url_manager import UrlManager, UrlType, URL


def test_get_all_urls(url_manager: UrlManager):
    urls: dict[UrlType, URL] = url_manager.get_all_urls()
    assert urls == {
        UrlType.CONFIGURATION_BROWSER_SHOW_FOUND_NOTES_SIZE: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#show-size-of-notes-found-in-browser',
        UrlType.CONFIGURATION_CACHE_WARM_UP_ENABLED: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#enable-cache-warm-up',
        UrlType.CONFIGURATION_CACHE_STORE_ON_DISK: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#store-cache-in-file-on-exit',
        UrlType.CONFIGURATION_LOGGING_LEVEL: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#logging',
        UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_ENABLED: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#enabled',
        UrlType.CONFIGURATION_DECK_BROWSER_SHOW_COLLECTION_SIZE: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#show-collection-size',
        UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_LEVELS: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#color---levels',
        UrlType.CONFIGURATION_EDITOR_SIZE_BUTTON_COLOR_ENABLED: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/configuration.md#color---enabled',
        UrlType.INFO_USER_MANUAL: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/docs/user-manual.md',
        UrlType.INFO_ADDON_PAGE: 'https://ankiweb.net/shared/info/1188705668',
        UrlType.INFO_FORUM: 'https://forums.ankiweb.net/t/note-size-addon-support/46001',
        UrlType.INFO_CHANGE_LOG: 'https://github.com/Aleks-Ya/note-size-anki-addon/blob/main/CHANGELOG.md',
        UrlType.INFO_BUG_TRACKER: 'https://github.com/Aleks-Ya/note-size-anki-addon/issues',
        UrlType.INFO_GITHUB: 'https://github.com/Aleks-Ya/note-size-anki-addon',
    }


@pytest.mark.integration
def test_ping_all_urls(url_manager: UrlManager):
    urls: dict[UrlType, URL] = url_manager.get_all_urls()
    failed_urls: dict[UrlType, URL] = {}
    for url_type, url in urls.items():
        response: Response = requests.get(url, timeout=60)
        if response.status_code >= 300:
            failed_urls[url_type] = url
            print(f"Unavailable URL {url_type} -> {url}: status code {response.status_code}")
        has_anchor: bool = "#" in url
        if has_anchor:
            soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
            parsed_url: ParseResult = urlparse(url)
            anchor_id: str = f"user-content-{parsed_url.fragment}"
            if anchor_id != '':
                anchor = soup.find(id=anchor_id)
                if not anchor:
                    failed_urls[url_type] = url
                    print(f"Unavailable anchor {url_type} -> {url}: '{anchor_id}'")
    if len(failed_urls) > 0:
        raise AssertionError(f"Unavailable URLS: {len(failed_urls)}")
