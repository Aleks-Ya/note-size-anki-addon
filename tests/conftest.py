import shutil
import tempfile
from pathlib import Path
from typing import Callable, Any

import pytest
from anki.collection import Collection
from aqt import AnkiQt
from aqt.addons import AddonManager
from mock.mock import MagicMock

from note_size.button.button_formatter import ButtonFormatter
from note_size.button.details_formatter import DetailsFormatter
from note_size.cache.cache_initializer import CacheInitializer
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.column.item_id_sorter import ItemIdSorter
from note_size.config.config import Config
from note_size.config.config_loader import ConfigLoader
from note_size.config.config_ui import ConfigUi
from note_size.config.settings import Settings
from note_size.config.ui.ui_model import UiModel
from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from note_size.deck_browser.trash import Trash
from note_size.log.logs import Logs
from tests.data import Data


@pytest.fixture
def module_name() -> str:
    return "1188705668"


@pytest.fixture
def profile_dir() -> Path:
    return Path(tempfile.mkdtemp(prefix="profile-"))


@pytest.fixture
def col(profile_dir: Path) -> Collection:
    collection_file: Path = profile_dir.joinpath("collection.anki2")
    col: Collection = Collection(str(collection_file))
    yield col
    col.close()


@pytest.fixture
def td(col: Collection, module_dir: Path) -> Data:
    return Data(col, module_dir)


@pytest.fixture
def project_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def addons_dir() -> Path:
    return Path(tempfile.mkdtemp())


@pytest.fixture
def module_dir(addons_dir: Path, module_name: str, project_dir: Path) -> Path:
    addon_project_dir: Path = project_dir.joinpath("note_size")
    module_dir: Path = addons_dir.joinpath(module_name)
    ignore_patterns: Callable[[Any, list[str]], set[str]] = shutil.ignore_patterns("__pycache__")
    shutil.copytree(addon_project_dir, module_dir, ignore=ignore_patterns)
    return module_dir


@pytest.fixture
def settings(col: Collection, module_dir: Path, module_name: str) -> Settings:
    return Settings(module_dir, module_name, Path())


@pytest.fixture
def config(col: Collection, td: Data) -> Config:
    return td.read_config()


@pytest.fixture
def media_cache(col: Collection, config: Config) -> MediaCache:
    return MediaCache(col, config)


@pytest.fixture
def size_calculator(col: Collection, media_cache: MediaCache) -> SizeCalculator:
    return SizeCalculator(media_cache)


@pytest.fixture
def item_id_cache(col: Collection, config: Config, size_calculator: SizeCalculator, settings: Settings,
                  media_cache: MediaCache) -> ItemIdCache:
    return ItemIdCache(col, size_calculator, media_cache, config, settings)


@pytest.fixture
def cache_initializer(mw: AnkiQt, media_cache: MediaCache, item_id_cache: ItemIdCache,
                      config: Config) -> CacheInitializer:
    return CacheInitializer(mw, media_cache, item_id_cache, config)


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
def trash(col: Collection) -> Trash:
    return Trash(col)


@pytest.fixture
def collection_size_formatter(col: Collection, item_id_cache: ItemIdCache, media_cache: MediaCache,
                              trash: Trash, settings: Settings) -> CollectionSizeFormatter:
    return CollectionSizeFormatter(col, item_id_cache, media_cache, trash, settings)


@pytest.fixture
def details_formatter(config: Config, settings: Settings, size_calculator: SizeCalculator) -> DetailsFormatter:
    return DetailsFormatter(size_calculator, settings, config)


@pytest.fixture
def addon_manager(addons_dir: Path) -> AddonManager:
    mw: MagicMock = MagicMock()
    mw.pm.addonFolder.return_value = addons_dir
    return AddonManager(mw)


@pytest.fixture
def config_loader(addon_manager: AddonManager, settings: Settings) -> ConfigLoader:
    return ConfigLoader(addon_manager, settings)


@pytest.fixture
def logs(settings: Settings) -> Logs:
    return Logs(settings)


@pytest.fixture
def config_ui() -> ConfigUi:
    return MagicMock()


@pytest.fixture
def mw() -> AnkiQt:
    return MagicMock()


@pytest.fixture
def ui_model() -> UiModel:
    return UiModel()
