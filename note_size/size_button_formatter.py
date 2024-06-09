import logging
from logging import Logger

from anki.notes import NoteId
from bs4 import BeautifulSoup, Tag

from .size_calculator import SizeCalculator, SizeBytes
from .item_id_cache import ItemIdCache
from .size_formatter import SizeStr

log: Logger = logging.getLogger(__name__)


class SizeButtonFormatter:
    def __init__(self, size_item_id_cache: ItemIdCache):
        self.size_item_id_cache: ItemIdCache = size_item_id_cache

    def get_note_human_str(self, note_id: NoteId) -> SizeStr:
        return self.size_item_id_cache.get_note_human_str(note_id, use_cache=False)

    def format_note_detailed_text(self, note):
        soup: BeautifulSoup = BeautifulSoup()
        self._add_total_note_size(note, soup)
        self._add_total_texts_size(note, soup)
        self._add_total_file_size(note, soup)
        self._add_files(note, soup)
        return str(soup.prettify())

    def _add_total_note_size(self, note, soup):
        h3: Tag = soup.new_tag('h3')
        h3.string = f"Total note size: "
        code: Tag = soup.new_tag('code')
        code.string = self.size_item_id_cache.get_note_human_str(note.id, use_cache=False)
        h3.append(code)
        soup.append(h3)

    def _add_total_texts_size(self, note, soup):
        li: Tag = soup.new_tag('li')
        li.string = f"Texts size: "
        code: Tag = soup.new_tag('code')
        code.string = self.size_item_id_cache.total_text_size_str(note)
        li.append(code)
        soup.append(li)

    def _add_total_file_size(self, note, soup):
        li: Tag = soup.new_tag('li')
        li.string = f"Files size: "
        code: Tag = soup.new_tag('code')
        code.string = self.size_item_id_cache.total_file_size_str(note)
        li.append(code)
        soup.append(li)

    def _add_files(self, note, soup):
        file_sizes: dict[str, SizeBytes] = SizeCalculator.sort_by_size_desc(SizeCalculator.file_sizes(note))
        is_empty_files: bool = len(file_sizes) == 0
        files_li: Tag = soup.new_tag('li')
        files_li.string = "Files (big to small):" if not is_empty_files else "Files: (no files)"
        soup.append(files_li)
        if not is_empty_files:
            ol: Tag = soup.new_tag('ol')
            for file, size in file_sizes.items():
                file_text, size_text = self.size_item_id_cache.file_size_to_human_string(file, size, 100)
                li: Tag = soup.new_tag('li', attrs={"style": "white-space:nowrap"})
                li.string = f"{file_text}: "
                code: Tag = soup.new_tag('code')
                code.string = size_text
                li.append(code)
                ol.append(li)
            soup.append(ol)
