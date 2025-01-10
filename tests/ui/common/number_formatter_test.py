from note_size.ui.common.number_formatter import NumberFormatter


def test_with_thousand_separator():
    assert NumberFormatter.with_thousands_separator(0) == "0"
    assert NumberFormatter.with_thousands_separator(100) == "100"
    assert NumberFormatter.with_thousands_separator(1000) == "1 000"
    assert NumberFormatter.with_thousands_separator(1000000) == "1 000 000"
    assert NumberFormatter.with_thousands_separator(1000.456) == "1 000.456"
