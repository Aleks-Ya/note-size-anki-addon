import logging
import os.path
from logging import Logger
from pathlib import Path
from typing import Optional

from anki.collection import Collection
from bs4 import BeautifulSoup, Tag

from .js_actions import JsActions
from .trash import Trash
from ..common.number_formatter import NumberFormatter
from ...cache.item_id_cache import ItemIdCache
from ...cache.media_cache import MediaCache
from ...calculator.used_files_calculator import UsedFilesCalculator
from ...config.settings import Settings
from ...types import SizeBytes, FilesNumber
from ...calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class CollectionSizeFormatter:
    __code_style: str = "font-family:Consolas,monospace;display: inline-block;"
    __sand_clock: str = "⏳"

    def __init__(self, col: Collection, item_id_cache: ItemIdCache, media_cache: MediaCache, trash: Trash,
                 size_formatter: SizeFormatter, used_files_calculator: UsedFilesCalculator, settings: Settings):
        self.__col: Collection = col
        self.__item_id_cache: ItemIdCache = item_id_cache
        self.__media_cache: MediaCache = media_cache
        self.__trash: Trash = trash
        self.__size_formatter: SizeFormatter = size_formatter
        self.__used_files_calculator: UsedFilesCalculator = used_files_calculator
        self.__collection_file_path: Path = Path(col.path)
        self.__media_folder_path: Path = Path(col.media.dir())
        self.__web_dir: str = os.path.join("_addons", settings.module_name, "ui", "web")
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format_collection_size_html(self) -> str:
        log.debug("Preparing data for formatting collection size has started")
        if self.__item_id_cache.is_initialized():
            log.debug("Use actual collection sizes")
            collection_size: SizeBytes = SizeBytes(self.__collection_file_path.stat().st_size)
            used_files_size, used_files_number, missing_files_number, used_notes_numbers \
                = self.__used_files_calculator.get_used_files_size(use_cache=True)
            unused_files_size, unused_files_number = self.__media_cache.get_unused_files_size(use_cache=True)
            trash_dir_size: SizeBytes = self.__trash.get_trash_dir_size()
            trash_files_number: FilesNumber = self.__trash.get_trash_files_number()
            note_count: int = self.__col.note_count()
            note_number_str: str = NumberFormatter.with_thousands_separator(note_count)
            used_notes_numbers_str: str = NumberFormatter.with_thousands_separator(used_notes_numbers)
            used_files_number_str: str = NumberFormatter.with_thousands_separator(used_files_number)
            missing_files_number_str: str = NumberFormatter.with_thousands_separator(missing_files_number)
            unused_files_size_str: str = NumberFormatter.with_thousands_separator(unused_files_number)
            trash_files_number_str: str = NumberFormatter.with_thousands_separator(trash_files_number)
            total_size: SizeBytes = SizeBytes(collection_size + used_files_size + unused_files_size + trash_dir_size)
        else:
            log.debug("Use sand clocks instead of actual collection sizes")
            collection_size: Optional[SizeBytes] = None
            used_files_size: Optional[SizeBytes] = None
            unused_files_size: Optional[SizeBytes] = None
            trash_dir_size: Optional[SizeBytes] = None
            total_size: Optional[SizeBytes] = None
            note_number_str: str = self.__sand_clock
            used_notes_numbers_str: str = self.__sand_clock
            used_files_number_str: str = self.__sand_clock
            missing_files_number_str: str = self.__sand_clock
            unused_files_size_str: str = self.__sand_clock
            trash_files_number_str: str = self.__sand_clock
        log.debug("Preparing data for formatting collection size has finished")
        trash_dir_path: Path = self.__trash.get_trash_dir_path()
        soup: BeautifulSoup = BeautifulSoup()
        div: Tag = soup.new_tag('div')
        collection_title: str = f'Size of {note_number_str} notes in file "{self.__collection_file_path}"'
        media_title: str = f'Size of {used_files_number_str} media files (including {missing_files_number_str} ' \
                           f'missing files) used in {used_notes_numbers_str} notes (not include Unused and Trash)\n' \
                           f'Folder "{self.__media_folder_path}"'
        unused_title: str = f'Size of {unused_files_size_str} ' \
                            f'media files not used in any notes (can be moved to Trash)'
        trash_title: str = f'Size of {trash_files_number_str} media files in the Trash (can be emptied)\n' \
                           f'Folder "{trash_dir_path}"'
        total_title: str = 'Total size of collection, media files, unused files and trash files'
        div.append(self.__span(soup, "Collection", collection_size, collection_title))
        div.append(self.__span(soup, "Media", used_files_size, media_title))
        div.append(self.__span(soup, "Unused", unused_files_size, unused_title, self.__details_icon(soup)))
        div.append(self.__span(soup, "Trash", trash_dir_size, trash_title, self.__details_icon(soup)))
        div.append(self.__span(soup, "Total", total_size, total_title))
        config_icon: Tag = soup.new_tag('img', attrs={
            "title": 'Open Configuration',
            "src": os.path.join(self.__web_dir, "setting.png"),
            "height": "12",
            "onclick": f"pycmd('{JsActions.open_config_action}')"
        })
        div.append(config_icon)

        soup.append(div)
        html: str = str(soup)
        log.debug("Formatting collection size finished")
        return html

    def __details_icon(self, soup: BeautifulSoup) -> Tag:
        details_icon: Tag = soup.new_tag('img', attrs={
            "title": 'Click to show details',
            "src": os.path.join(self.__web_dir, "info.png"),
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
            size_split: list[str] = self.__size_formatter.bytes_to_str(size, precision=0,
                                                                       unit_separator=separator).split(separator)
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

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
