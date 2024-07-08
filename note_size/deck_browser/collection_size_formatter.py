import logging
from logging import Logger
from pathlib import Path

from anki.collection import Collection
from aqt import mw

from ..types import SizeStr, SizeBytes
from ..cache.media_cache import MediaCache
from ..calculator.size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class CollectionSizeFormatter:

    def __init__(self, col: Collection, media_cache: MediaCache):
        self.__media_cache: MediaCache = media_cache
        self.__collection_file_path: Path = Path(col.path)
        self.__media_folder_path: Path = Path(col.media.dir())
        log.debug(f"{self.__class__.__name__} was instantiated")

    def format_collection_size_html(self) -> str:
        collection_size: SizeStr = SizeFormatter.bytes_to_str(self.__collection_size())
        media_size: SizeStr = SizeFormatter.bytes_to_str(self.__media_size())
        total_size: SizeStr = SizeFormatter.bytes_to_str(self.__total_size())
        collection_title: str = f'Size of file "{self.__collection_file_path}"'
        media_title: str = f'Size of folder "{self.__media_folder_path}"'
        total_title: str = f'Total size of collection file and media folder'
        code_style: str = "font-family:Consolas,monospace"
        collection_span: str = f"<span style='{code_style}'>{collection_size}</span>"
        media_span: str = f"<span style='{code_style}'>{media_size}</span>"
        total_span: str = f"<span style='{code_style}'>{total_size}</span>"
        return (f"<div>"
                f"<span title='{collection_title}'>Collection:&nbsp;{collection_span}&nbsp;&nbsp;&nbsp;</span>"
                f"<span title='{media_title}'>Media:&nbsp;{media_span}&nbsp;&nbsp;&nbsp;</span>"
                f"<span title='{total_title}'>Total:&nbsp;{total_span}</span>"
                f"</div>")

    def __media_size(self) -> SizeBytes:
        return self.__media_cache.get_total_files_size()

    def __collection_size(self) -> SizeBytes:
        return SizeBytes(self.__collection_file_path.stat().st_size)

    def __total_size(self) -> SizeBytes:
        return SizeBytes(self.__collection_size() + self.__media_size())
