import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from anki.collection import Collection
from bs4 import BeautifulSoup, Tag

from .js_actions import JsActions
from .trash import Trash
from ..cache.item_id_cache import ItemIdCache
from ..config.settings import Settings
from ..types import SizeBytes, FilesNumber
from ..cache.media_cache import MediaCache
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class CollectionSizeFormatter:
    __code_style: str = "font-family:Consolas,monospace;display: inline-block;"
    __sand_clock: str = "⏳"

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, media_cache: MediaCache, trash: Trash,
                 settings: Settings):
        self.__col: Collection = col
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__media_cache: MediaCache = media_cache
        self.__trash: Trash = trash
        self.__collection_file_path: Path = Path(col.path)
        self.__media_folder_path: Path = Path(col.media.dir())
        self.__module_name: str = settings.module_name
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format_collection_size_html(self) -> str:
        log.debug("Formatting collection size started")
        if self.__item_id_cache.is_initialized():
            collection_size: SizeBytes = SizeBytes(self.__collection_file_path.stat().st_size)
            used_files_size, used_files_number = self.__item_id_cache.get_used_files_size(use_cache=True)
            unused_files_size, unused_files_number = self.__media_cache.get_unused_files_size(use_cache=True)
            trash_dir_size: SizeBytes = self.__trash.get_trash_dir_size()
            trash_files_number: FilesNumber = self.__trash.get_trash_files_number()
            note_count: int = self.__col.note_count()
            note_number_str: str = self.__format_number(note_count)
            used_files_number_str: str = self.__format_number(used_files_number)
            unused_files_size_str: str = self.__format_number(unused_files_number)
            trash_files_number_str: str = self.__format_number(trash_files_number)
            total_size: SizeBytes = SizeBytes(collection_size + used_files_size + unused_files_size + trash_dir_size)
        else:
            collection_size: Optional[SizeBytes] = None
            used_files_size: Optional[SizeBytes] = None
            unused_files_size: Optional[SizeBytes] = None
            trash_dir_size: Optional[SizeBytes] = None
            total_size: Optional[SizeBytes] = None
            note_number_str: str = self.__sand_clock
            used_files_number_str: str = self.__sand_clock
            unused_files_size_str: str = self.__sand_clock
            trash_files_number_str: str = self.__sand_clock
        trash_dir_path: Path = self.__trash.get_trash_dir_path()
        soup: BeautifulSoup = BeautifulSoup()
        div: Tag = soup.new_tag('div')
        collection_title: str = f'Size of {note_number_str} notes\nFile "{self.__collection_file_path}"'
        media_title: str = f'Size of {used_files_number_str} ' \
                           f'media files used in notes (not include Unused and Trash)\n' \
                           f'Folder "{self.__media_folder_path}"'
        unused_title: str = f'Size of {unused_files_size_str} ' \
                            f'media files not used in any notes (can be moved to Trash)'
        trash_title: str = f'Size of {trash_files_number_str} media files in the Trash (can be emptied)\n' \
                           f'Folder "{trash_dir_path}"'
        total_title: str = f'Total size of collection, media files, unused files and trash files'
        div.append(self.__span(soup, "Collection", collection_size, collection_title))
        div.append(self.__span(soup, "Media", used_files_size, media_title))
        div.append(self.__span(soup, "Unused", unused_files_size, unused_title, self.__details_icon(soup)))
        div.append(self.__span(soup, "Trash", trash_dir_size, trash_title, self.__details_icon(soup)))
        div.append(self.__span(soup, "Total", total_size, total_title))
        config_icon: Tag = soup.new_tag('img', attrs={
            "title": 'Open Configuration',
            "src": f"/_addons/{self.__module_name}/web/setting.png",
            "height": "12",
            "onclick": f"pycmd('{JsActions.open_config_action}')"
        })
        div.append(config_icon)

        soup.append(div)
        html = str(soup)
        log.debug("Formatting collection size finished")
        return html

    def __details_icon(self, soup: BeautifulSoup):
        details_icon: Tag = soup.new_tag('img', attrs={
            "title": 'Click to show details',
            "src": f"/_addons/{self.__module_name}/web/info.png",
            "height": "12",
            "onclick": f"pycmd('{JsActions.open_check_media_action}')",
            "style": "margin-right: 0.2em;"
        })
        return details_icon

    def __span(self, soup: BeautifulSoup, name: str, size: Optional[SizeBytes], title: str, icon: Tag = None) -> Tag:
        log.debug(f"Create span for: name={name}, size={size}")
        outer_span: Tag = soup.new_tag('span', attrs={"title": f'{title}', "style": "margin-right: 0.5em;"})
        outer_span.string = f"{name}: "
        if size is not None:
            separator: str = " "
            size_split: list[str] = SizeFormatter.bytes_to_str(size, precision=0, unit_separator=separator).split(
                separator)
            number: str = size_split[0]
            unit: str = size_split[1]
            number_span: Tag = soup.new_tag('span', attrs={"style": CollectionSizeFormatter.__code_style})
            outer_span.append(number_span)
            number_span.string = number
            unit_span: Tag = soup.new_tag('span', attrs={"style": CollectionSizeFormatter.__code_style})
            unit_span.string = unit
            outer_span.append(" ")
            outer_span.append(unit_span)
            if icon:
                outer_span.append(icon)
        else:
            number_span: Tag = soup.new_tag('span', attrs={"style": "font-size: 80%"})
            outer_span.append(number_span)
            number_span.string = self.__sand_clock
        return outer_span

    @staticmethod
    def __format_number(num: int) -> str:
        return f"{num:,}".replace(',', ' ')
