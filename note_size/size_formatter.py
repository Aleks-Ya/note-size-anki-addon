from typing import NewType

from .size_calculator import SizeBytes, MediaFile

SizeStr = NewType("SizeStr", str)


class SizeFormatter:

    @staticmethod
    def bytes_to_human_str(bytes_size: SizeBytes) -> SizeStr:
        divisor: int = 1024
        units: tuple[str, str, str] = 'B', 'KB', 'MB'
        final_unit: str = 'GB'
        num: float = float(bytes_size)
        for unit in units:
            if abs(num) < divisor:
                if unit == 'B':
                    return SizeStr(f'{num:0.0f}{unit}')
                else:
                    return SizeStr(f'{num:0.1f}{unit}')
            num /= divisor
        return SizeStr(f'{num:0.1f}{final_unit}')

    @staticmethod
    def file_size_to_human_string(file: MediaFile, size: SizeBytes, max_length: int) -> tuple[str, SizeStr]:
        size_text: SizeStr = SizeFormatter.bytes_to_human_str(size)
        file_text: str = SizeFormatter._prune_string(file, size_text, max_length)
        return file_text, size_text

    @staticmethod
    def _prune_string(file: MediaFile, size: SizeStr, max_length: int) -> str:
        file_max_length: int = max_length - len(size) - 2
        if len(file) > file_max_length:
            part_length: int = (file_max_length - 3) // 2
            file = file[:part_length] + "..." + file[-part_length:]
        return file
