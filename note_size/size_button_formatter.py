import logging
from logging import Logger

from bs4 import BeautifulSoup, Tag

from .size_calculator import SizeCalculator
from .size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class SizeButtonFormatter:
    def __init__(self, size_calculator: SizeCalculator):
        self.size_calculator: SizeCalculator = size_calculator

    def format_note_detailed_text(self, note):
        soup: BeautifulSoup = BeautifulSoup()
        self._add_total_note_size(note, soup)
        self._add_total_texts_size(note, soup)
        self._add_total_file_size(note, soup)
        self._add_files(note, soup)
        return str(soup.prettify())

    def _add_total_note_size(self, note, soup):
        note_size: int = self.size_calculator.calculate_note_size(note, use_cache=False)
        total_size: str = SizeFormatter.bytes_to_human_str(note_size)
        h3: Tag = soup.new_tag('h3')
        h3.string = f"Total note size: "
        code: Tag = soup.new_tag('code')
        code.string = total_size
        h3.append(code)
        soup.append(h3)

    @staticmethod
    def _add_total_texts_size(note, soup):
        size: str = SizeFormatter.bytes_to_human_str(SizeCalculator.total_text_size(note))
        li: Tag = soup.new_tag('li')
        li.string = f"Texts size: "
        code: Tag = soup.new_tag('code')
        code.string = size
        li.append(code)
        soup.append(li)

    @staticmethod
    def _add_total_file_size(note, soup):
        size: str = SizeFormatter.bytes_to_human_str(SizeCalculator.total_file_size(note))
        li: Tag = soup.new_tag('li')
        li.string = f"Files size: "
        code: Tag = soup.new_tag('code')
        code.string = size
        li.append(code)
        soup.append(li)

    @staticmethod
    def _add_files(note, soup):
        file_sizes: dict[str, int] = SizeCalculator.sort_by_size_desc(SizeCalculator.file_sizes(note))
        is_empty_files: bool = len(file_sizes) == 0
        files_li: Tag = soup.new_tag('li')
        files_li.string = "Files (big to small):" if not is_empty_files else "Files: (no files)"
        soup.append(files_li)
        if not is_empty_files:
            ol: Tag = soup.new_tag('ol')
            for file, size in file_sizes.items():
                file_text, size_text = SizeFormatter.file_size_to_human_string(file, size, 100)
                li: Tag = soup.new_tag('li', attrs={"style": "white-space:nowrap"})
                li.string = f"{file_text}: "
                code: Tag = soup.new_tag('code')
                code.string = size_text
                li.append(code)
                ol.append(li)
            soup.append(ol)
