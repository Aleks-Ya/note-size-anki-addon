from pydantic import ByteSize


class SizeFormatter:

    @staticmethod
    def bytes_to_human_str(bytes_size: int) -> str:
        byte_size: ByteSize = ByteSize(bytes_size)
        return byte_size.human_readable(True)

    @staticmethod
    def file_sizes_to_human_strings(file_sizes: dict[str, int]) -> list[str]:
        return [f"{key}: {SizeFormatter.bytes_to_human_str(value)}" for key, value in file_sizes.items()]
