from ..types import SizeStr, SizeBytes


class SizeFormatter:

    @staticmethod
    def bytes_to_str(size: SizeBytes, precision: int = 1, unit_separator: str = " ") -> SizeStr:
        divisor: int = 1024
        units: tuple[str, str, str] = 'B', 'KB', 'MB'
        final_unit: str = 'GB'
        num: float = float(size)
        for unit in units:
            if abs(num) < divisor:
                if unit == 'B':
                    return SizeStr(f'{num:0.0f}{unit_separator}{unit}')
                else:
                    return SizeStr(f'{num:0.{precision}f}{unit_separator}{unit}')
            num /= divisor
        return SizeStr(f'{num:0.{precision}f}{unit_separator}{final_unit}')

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
