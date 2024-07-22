import tempfile
from pathlib import Path

import pytest
from anki.collection import Collection

from note_size.button.button_formatter import ButtonFormatter
from note_size.button.details_formatter import DetailsFormatter
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.column.item_id_sorter import ItemIdSorter
from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from tests.data import Data


@pytest.fixture
def module_name() -> str:
    return "note_size"


@pytest.fixture
def col() -> Collection:
    col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
    yield col
    col.close()


@pytest.fixture
def td(col: Collection) -> Data:
    return Data(col)


@pytest.fixture
def project_dir(col: Collection, td: Data) -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def addon_dir(project_dir: Path) -> Path:
    return project_dir.joinpath("note_size")


@pytest.fixture
def settings(col: Collection, addon_dir: Path, module_name: str) -> Settings:
    return Settings(addon_dir, module_name, Path(), "1188705668")


@pytest.fixture
def config(col: Collection, td: Data) -> Config:
    return Data.read_config()


@pytest.fixture
def media_cache(col: Collection, config: Config) -> MediaCache:
    return MediaCache(col, config)


@pytest.fixture
def size_calculator(col: Collection, media_cache: MediaCache) -> SizeCalculator:
    return SizeCalculator(media_cache)


@pytest.fixture
def item_id_cache(col: Collection, config: Config, size_calculator: SizeCalculator) -> ItemIdCache:
    return ItemIdCache(col, size_calculator, config)


@pytest.fixture
def item_id_sorter(item_id_cache: ItemIdCache) -> ItemIdSorter:
    return ItemIdSorter(item_id_cache)


@pytest.fixture
def button_formatter(config: Config, size_calculator: SizeCalculator, item_id_cache: ItemIdCache) -> ButtonFormatter:
    return ButtonFormatter(item_id_cache, size_calculator, config)


@pytest.fixture
def size_formatter() -> SizeFormatter:
    return SizeFormatter()


@pytest.fixture
def collection_size_formatter(col: Collection, media_cache: MediaCache) -> CollectionSizeFormatter:
    return CollectionSizeFormatter(col, media_cache)


@pytest.fixture
def details_formatter(config: Config, settings: Settings, size_calculator: SizeCalculator) -> DetailsFormatter:
    return DetailsFormatter(size_calculator, settings, config)
