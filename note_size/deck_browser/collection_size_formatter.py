import logging
from logging import Logger
from pathlib import Path

from anki.collection import Collection
from bs4 import BeautifulSoup, Tag

from ..config.settings import Settings
from ..types import SizeBytes
from ..cache.media_cache import MediaCache
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class CollectionSizeFormatter:
    __code_style: str = "font-family:Consolas,monospace"
    __open_config_action: str = "open-config-action"

    def __init__(self, col: Collection, media_cache: MediaCache, settings: Settings):
        self.__media_cache: MediaCache = media_cache
        self.__collection_file_path: Path = Path(col.path)
        self.__media_folder_path: Path = Path(col.media.dir())
        self.__module_name: str = settings.module_name
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format_collection_size_html(self) -> str:
        media_file_number: int = len(list(self.__media_folder_path.glob('*')))
        media_file_number_str: str = f"{media_file_number:,}".replace(',', ' ')
        soup: BeautifulSoup = BeautifulSoup()
        div: Tag = soup.new_tag('div')
        div.append(self.__span(soup, "Collection", self.__collection_size(),
                               f'Size of file "{self.__collection_file_path}"'))
        div.append(self.__span(soup, "Media", self.__media_size(),
                               f'Size of folder "{self.__media_folder_path}" ({media_file_number_str} files)'))
        div.append(self.__span(soup, "Total", self.__total_size(),
                               f'Total size of collection file and media folder'))
        config_icon: Tag = soup.new_tag('img', attrs={
            "title": 'Open Configuration',
            "src": f"/_addons/{self.__module_name}/web/setting.png",
            "height": "12",
            "onclick": f"pycmd('{self.__open_config_action}')"
        })
        div.append(config_icon)

        soup.append(div)
        return str(soup.prettify())

    @staticmethod
    def __span(soup: BeautifulSoup, name: str, size: SizeBytes, title: str) -> Tag:
        inner_span: Tag = soup.new_tag('span', attrs={"style": CollectionSizeFormatter.__code_style})
        inner_span.string = SizeFormatter.bytes_to_str(size)
        outer_span: Tag = soup.new_tag('span', attrs={"title": f'{title}'})
        outer_span.string = f"{name}: "
        outer_span.append(inner_span)
        outer_span.append("   ")
        return outer_span

    def __media_size(self) -> SizeBytes:
        return self.__media_cache.get_total_files_size()

    def __collection_size(self) -> SizeBytes:
        return SizeBytes(self.__collection_file_path.stat().st_size)

    def __total_size(self) -> SizeBytes:
        return SizeBytes(self.__collection_size() + self.__media_size())
