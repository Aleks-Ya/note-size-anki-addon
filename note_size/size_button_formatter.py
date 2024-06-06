import logging
from logging import Logger

from .size_calculator import SizeCalculator
from .size_formatter import SizeFormatter

log: Logger = logging.getLogger(__name__)


class SizeButtonFormatter:

    @staticmethod
    def format_note_detailed_text(note):
        total_size: str = SizeFormatter.bytes_to_human_str(SizeCalculator.calculate_note_size(note))
        total_texts_size: str = SizeFormatter.bytes_to_human_str(SizeCalculator.total_text_size(note))
        total_files_size: str = SizeFormatter.bytes_to_human_str(SizeCalculator.total_file_size(note))
        file_sizes: dict[str, int] = SizeCalculator.sort_by_size_desc(SizeCalculator.file_sizes(note))
        files_sizes_str: list[str] = SizeFormatter.file_sizes_to_human_strings(file_sizes)
        files_str: str = '</li><li style="white-space:nowrap">'.join(files_sizes_str) \
            if len(files_sizes_str) > 0 else "<no-files>"
        detailed: str = f"""
                            <h3>Total note size: {total_size}</h3>
                            <ul>
                                <li>Texts size: {total_texts_size}</li>
                                <li>Files size: {total_files_size}</li>
                                <li>Files (big to small):</li>
                                    <ol>
                                        <li style="white-space:nowrap">{files_str}</li>
                                    </ol>
                            </ul>
                            """
        return detailed
