from .types import SizeStr, SizeBytes, SignificantDigits


class SizeFormatter:

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
    def bytes_to_str(size: SizeBytes, significant_digits: SignificantDigits, unit_separator: str = " ") -> SizeStr:
        divisor: int = 1024
        byte_unit: str = 'B'
        units: list[str] = [byte_unit, 'KB', 'MB', 'GB']
        num: float = size
        unit_index: int = 0
        while num >= divisor and unit_index < len(units) - 1:
            num /= divisor
            unit_index += 1
        unit: str = units[unit_index]
        precision: int = max(0, significant_digits - len(str(int(num)))) if unit != byte_unit else 0
        return SizeStr(f"{num:.{precision}f}{unit_separator}{unit}")
