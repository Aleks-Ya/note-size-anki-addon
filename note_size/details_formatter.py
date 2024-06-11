import logging
from logging import Logger

from anki.notes import Note
from bs4 import BeautifulSoup, Tag

from .size_calculator import SizeCalculator, SizeBytes, MediaFile
from .item_id_cache import ItemIdCache

log: Logger = logging.getLogger(__name__)


class DetailsFormatter:

    @staticmethod
    def format_note_detailed_text(note: Note) -> str:
        soup: BeautifulSoup = BeautifulSoup()
        DetailsFormatter._add_total_note_size(note, soup)
        DetailsFormatter._add_total_texts_size(note, soup)
        DetailsFormatter._add_total_files_size(note, soup)
        DetailsFormatter._add_files(note, soup)
        return str(soup.prettify())

    @staticmethod
    def _add_total_note_size(note: Note, soup: BeautifulSoup) -> None:
        h3: Tag = soup.new_tag('h3')
        h3.string = f"Total note size: "
        code: Tag = soup.new_tag('code')
        code.string = ItemIdCache.get_note_size_str(note)
        h3.append(code)
        soup.append(h3)

    @staticmethod
    def _add_total_texts_size(note: Note, soup: BeautifulSoup) -> None:
        li: Tag = soup.new_tag('li')
        li.string = f"Texts size: "
        code: Tag = soup.new_tag('code')
        code.string = ItemIdCache.calculate_texts_size(note)
        li.append(code)
        soup.append(li)

    @staticmethod
    def _add_total_files_size(note: Note, soup: BeautifulSoup) -> None:
        li: Tag = soup.new_tag('li')
        li.string = f"Files size: "
        code: Tag = soup.new_tag('code')
        code.string = ItemIdCache.calculate_files_size(note)
        li.append(code)
        soup.append(li)

    @staticmethod
    def _add_files(note: Note, soup: BeautifulSoup) -> None:
        file_sizes: dict[MediaFile, SizeBytes] = SizeCalculator.sort_by_size_desc(SizeCalculator.file_sizes(note))
        is_empty_files: bool = len(file_sizes) == 0
        files_li: Tag = soup.new_tag('li')
        files_li.string = "Files (big to small):" if not is_empty_files else "Files: (no files)"
        soup.append(files_li)
        if not is_empty_files:
            ol: Tag = soup.new_tag('ol')
            for file, size in file_sizes.items():
                filename, size_text = ItemIdCache.file_size_to_str(file, size, 100)
                li: Tag = soup.new_tag('li', attrs={"style": "white-space:nowrap"})
                li.string = f"{filename}: "
                code: Tag = soup.new_tag('code')
                code.string = size_text
                li.append(code)
                ol.append(li)
            soup.append(ol)
