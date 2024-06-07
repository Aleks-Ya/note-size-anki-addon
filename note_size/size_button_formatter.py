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
        note_size: int = self.size_calculator.calculate_note_size(note, use_cache=False)
        total_size: str = SizeFormatter.bytes_to_human_str(note_size)
        total_texts_size: str = SizeFormatter.bytes_to_human_str(SizeCalculator.total_text_size(note))
        total_files_size: str = SizeFormatter.bytes_to_human_str(SizeCalculator.total_file_size(note))
        file_sizes: dict[str, int] = SizeCalculator.sort_by_size_desc(SizeCalculator.file_sizes(note))
        files_sizes_str: list[str] = SizeFormatter.file_sizes_to_human_strings(file_sizes, 100)

        soup: BeautifulSoup = BeautifulSoup()

        total_note_size_h3: Tag = soup.new_tag('h3')
        total_note_size_h3.string = f"Total note size: {total_size}"
        soup.append(total_note_size_h3)

        text_size_li: Tag = soup.new_tag('li')
        text_size_li.string = f"Texts size: {total_texts_size}"
        soup.append(text_size_li)

        file_size_li: Tag = soup.new_tag('li')
        file_size_li.string = f"Files size: {total_files_size}"
        soup.append(file_size_li)

        is_empty_files: bool = len(files_sizes_str) == 0

        files_li: Tag = soup.new_tag('li')
        files_li.string = "Files (big to small):" if not is_empty_files else "Files: (no files)"
        soup.append(files_li)

        if not is_empty_files:
            files_ol: Tag = soup.new_tag('ol')
            for files_str in files_sizes_str:
                li: Tag = soup.new_tag('li', attrs={"style": "white-space:nowrap"})
                li.string = files_str
                files_ol.append(li)
            soup.append(files_ol)

        return str(soup.prettify())
