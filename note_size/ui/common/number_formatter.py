class NumberFormatter:
    @staticmethod
    def with_thousands_separator(number: float) -> str:
        return f"{number:,}".replace(',', ' ')
