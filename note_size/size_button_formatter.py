import logging
from logging import Logger

from anki.notes import NoteId, Note
from bs4 import BeautifulSoup, Tag

from .size_calculator import SizeCalculator, SizeBytes, MediaFile
from .item_id_cache import ItemIdCache
from .size_formatter import SizeStr, SizeFormatter

log: Logger = logging.getLogger(__name__)


class SizeButtonFormatter:
    def __init__(self, size_item_id_cache: ItemIdCache):
        self.size_item_id_cache: ItemIdCache = size_item_id_cache

    def get_note_human_str(self, note_id: NoteId) -> SizeStr:
        return self.size_item_id_cache.get_note_human_str(note_id, use_cache=False)

    @staticmethod
    def get_note_size(note: Note) -> SizeStr:
        return ItemIdCache.get_note_size_str(note)

    @staticmethod
    def format_note_detailed_text(note: Note) -> str:
        soup: BeautifulSoup = BeautifulSoup()
        SizeButtonFormatter._add_total_note_size(note, soup)
        SizeButtonFormatter._add_total_texts_size(note, soup)
        SizeButtonFormatter._add_total_file_size(note, soup)
        SizeButtonFormatter._add_files(note, soup)
        return str(soup.prettify())

    @staticmethod
    def get_zero_size() -> SizeStr:
        return SizeFormatter.bytes_to_human_str(SizeBytes(0))

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
        code.string = ItemIdCache.get_total_text_size(note)
        li.append(code)
        soup.append(li)

    @staticmethod
    def _add_total_file_size(note: Note, soup: BeautifulSoup) -> None:
        li: Tag = soup.new_tag('li')
        li.string = f"Files size: "
        code: Tag = soup.new_tag('code')
        code.string = ItemIdCache.get_total_file_size(note)
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
