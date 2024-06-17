import logging
import mimetypes
from logging import Logger
from pathlib import Path

from anki.notes import Note
from bs4 import BeautifulSoup, Tag

from .size_formatter import SizeFormatter
from .size_calculator import SizeCalculator
from .types import SizeBytes, MediaFile

log: Logger = logging.getLogger(__name__)


class DetailsFormatter:
    code_style: str = "font-family:Consolas,monospace"

    def __init__(self, addon_dir: Path):
        self.icons_dir: Path = addon_dir.joinpath("icon")

    def format_note_detailed_text(self, note: Note) -> str:
        soup: BeautifulSoup = BeautifulSoup()
        DetailsFormatter._add_total_note_size(note, soup)
        DetailsFormatter._add_total_texts_size(note, soup)
        DetailsFormatter._add_total_files_size(note, soup)
        self._add_files(note, soup)
        return str(soup.prettify())

    @staticmethod
    def _add_total_note_size(note: Note, soup: BeautifulSoup) -> None:
        h3: Tag = soup.new_tag('h3')
        h3.string = f"Total note size: "
        code: Tag = soup.new_tag('code', attrs={"style": DetailsFormatter.code_style})
        code.string = SizeFormatter.bytes_to_str(SizeCalculator.calculate_note_size(note))
        h3.append(code)
        soup.append(h3)

    @staticmethod
    def _add_total_texts_size(note: Note, soup: BeautifulSoup) -> None:
        li: Tag = soup.new_tag('li')
        li.string = f"Texts size: "
        code: Tag = soup.new_tag('code', attrs={"style": DetailsFormatter.code_style})
        code.string = SizeFormatter.bytes_to_str(SizeCalculator.calculate_texts_size(note))
        li.append(code)
        soup.append(li)

    @staticmethod
    def _add_total_files_size(note: Note, soup: BeautifulSoup) -> None:
        li: Tag = soup.new_tag('li')
        li.string = f"Files size: "
        code: Tag = soup.new_tag('code', attrs={"style": DetailsFormatter.code_style})
        code.string = SizeFormatter.bytes_to_str(SizeCalculator.calculate_files_size(note))
        li.append(code)
        soup.append(li)

    def _add_files(self, note: Note, soup: BeautifulSoup) -> None:
        file_sizes: dict[MediaFile, SizeBytes] = SizeCalculator.sort_by_size_desc(SizeCalculator.file_sizes(note))
        is_empty_files: bool = len(file_sizes) == 0
        files_li: Tag = soup.new_tag('li')
        files_li.string = "Files (big to small):" if not is_empty_files else "Files: (no files)"
        soup.append(files_li)
        if not is_empty_files:
            ol: Tag = soup.new_tag('ol')
            for file, size in file_sizes.items():
                filename, size_text = SizeFormatter.file_size_to_str(file, size, 100)
                icon_path: Path = self._get_file_icon(filename)
                img: Tag = soup.new_tag("img",
                                        attrs={"src": icon_path, "height": "15", "style": "vertical-align: middle;"})
                log.info(f"IMG: {img.prettify()}")
                li: Tag = soup.new_tag('li', attrs={"style": "white-space:nowrap"})
                li.append(img)
                li.append(f"{filename}: ")
                code: Tag = soup.new_tag('code', attrs={"style": DetailsFormatter.code_style})
                code.string = size_text
                li.append(code)
                ol.append(li)
            soup.append(ol)

    def _get_file_icon(self, filename: str) -> Path:
        full_mime_type: str = mimetypes.guess_type(filename)[0]
        general_mime_type: str = full_mime_type.split("/")[0]
        icon_path: Path = self.icons_dir.joinpath(general_mime_type + ".png")
        if not icon_path.exists():
            icon_path: Path = self.icons_dir.joinpath("other.png")
        return icon_path
