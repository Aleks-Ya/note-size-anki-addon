class NumberFormatter:
    @staticmethod
    def with_thousands_separator(number: int) -> str:
        return f"{number:,}".replace(',', ' ')
