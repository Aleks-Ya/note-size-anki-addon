from note_size.calculator.size_calculator import SizeCalculator
from tests.conftest import size_calculator


def test_cache_id(size_calculator: SizeCalculator):
    assert size_calculator.cache_id() == "SizeCalculator"
