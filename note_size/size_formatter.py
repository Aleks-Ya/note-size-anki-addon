class SizeFormatter:

    @staticmethod
    def bytes_to_human_str(bytes_size: int) -> str:
        divisor = 1024
        units = 'B', 'KB', 'MB'
        final_unit = 'GB'
        num = float(bytes_size)
        for unit in units:
            if abs(num) < divisor:
                if unit == 'B':
                    return f'{num:0.0f}{unit}'
                else:
                    return f'{num:0.1f}{unit}'
            num /= divisor

        return f'{num:0.1f}{final_unit}'

    @staticmethod
    def file_sizes_to_human_strings(file_sizes: dict[str, int]) -> list[str]:
        return [f"{key}: {SizeFormatter.bytes_to_human_str(value)}" for key, value in file_sizes.items()]
