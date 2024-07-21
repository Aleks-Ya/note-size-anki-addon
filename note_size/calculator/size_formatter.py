from ..types import SizeStr, ShortFilename, SizeBytes, MediaFile


class SizeFormatter:

    @staticmethod
    def bytes_to_str(size: SizeBytes, precision: int = 1) -> SizeStr:
        divisor: int = 1024
        units: tuple[str, str, str] = 'B', 'KB', 'MB'
        final_unit: str = 'GB'
        num: float = float(size)
        for unit in units:
            if abs(num) < divisor:
                if unit == 'B':
                    return SizeStr(f'{num:0.0f} {unit}')
                else:
                    return SizeStr(f'{num:0.{precision}f} {unit}')
            num /= divisor
        return SizeStr(f'{num:0.{precision}f} {final_unit}')

    @staticmethod
    def str_to_bytes(size_str: SizeStr) -> SizeBytes:
        size_str = size_str.strip()
        units = {'B': 0, 'KB': 1, 'MB': 2, 'GB': 3}
        if size_str[-2:].upper() in units:
            size = float(size_str[:-2])
            unit = units[size_str[-2:].upper()]
        elif size_str[-1].upper() in units:
            size = float(size_str[:-1])
            unit = units[size_str[-1].upper()]
        else:
            raise ValueError(f"Invalid size string: '{size_str}'")
        size_in_bytes = int(size * (1024 ** unit))
        return SizeBytes(size_in_bytes)

    @staticmethod
    def file_size_to_str(file: MediaFile, size: SizeBytes, max_length: int) \
            -> tuple[ShortFilename, SizeStr]:
        size_str: SizeStr = SizeFormatter.bytes_to_str(size)
        filename: ShortFilename = SizeFormatter.__prune_string(file, size_str, max_length)
        return filename, size_str

    @staticmethod
    def __prune_string(file: MediaFile, size: SizeStr, max_length: int) -> ShortFilename:
        file_max_length: int = max_length - len(size) - 2
        if len(file) > file_max_length:
            part_length: int = (file_max_length - 3) // 2
            filename: str = file[:part_length] + "..." + file[-part_length:]
        else:
            filename: str = file
        return ShortFilename(filename)
