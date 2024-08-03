import logging
from logging import Logger
from pathlib import Path

from anki.collection import Collection
from bs4 import BeautifulSoup, Tag

from .trash import Trash
from ..cache.item_id_cache import ItemIdCache
from ..config.settings import Settings
from ..types import SizeBytes, FilesNumber
from ..cache.media_cache import MediaCache
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class CollectionSizeFormatter:
    __code_style: str = "font-family:Consolas,monospace"
    __open_config_action: str = "open-config-action"

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, media_cache: MediaCache, trash: Trash,
                 settings: Settings):
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__media_cache: MediaCache = media_cache
        self.__trash: Trash = trash
        self.__collection_file_path: Path = Path(col.path)
        self.__media_folder_path: Path = Path(col.media.dir())
        self.__module_name: str = settings.module_name
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format_collection_size_html(self) -> str:
        media_file_number: int = len(list(self.__media_folder_path.glob('*')))
        media_file_number_str: str = f"{media_file_number:,}".replace(',', ' ')
        collection_size: SizeBytes = SizeBytes(self.__collection_file_path.stat().st_size)
        used_files_size, used_files_number = self.__item_id_cache.get_used_files_size(use_cache=True)
        unused_files_size, unused_files_number = self.__media_cache.get_unused_files_size(use_cache=True)
        trash_dir_size: SizeBytes = self.__trash.get_trash_dir_size()
        trash_files_number: FilesNumber = self.__trash.get_trash_files_number()
        total_size: SizeBytes = SizeBytes(collection_size + used_files_size + unused_files_size + trash_dir_size)
        soup: BeautifulSoup = BeautifulSoup()
        div: Tag = soup.new_tag('div')
        div.append(self.__span(soup, "Collection", collection_size,
                               f'Size of file "{self.__collection_file_path}"'))
        div.append(self.__span(soup, "Media", used_files_size,
                               f'Size of {media_file_number_str} '
                               f'media files used in notes (do not include "Unused" and "Trash")'))
        div.append(self.__span(soup, "Unused", unused_files_size,
                               f'Size of {unused_files_number} '
                               f'media files not used in any notes (can be moved to Trash)'))
        div.append(self.__span(soup, "Trash", trash_dir_size,
                               f'Size of {trash_files_number} media files in the Trash (can be emptied)'))
        div.append(self.__span(soup, "Total", total_size,
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
        inner_span.string = SizeFormatter.bytes_to_str(size, precision=0)
        outer_span: Tag = soup.new_tag('span', attrs={"title": f'{title}'})
        outer_span.string = f"{name}: "
        outer_span.append(inner_span)
        outer_span.append("   ")
        return outer_span
