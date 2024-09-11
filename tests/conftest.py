import shutil
import tempfile
from pathlib import Path
from typing import Callable, Any

import aqt
import pytest
from anki.collection import Collection
from aqt import AnkiQt, ProfileManager, QApplication, QDesktopServices
from aqt.addons import AddonManager
from aqt.theme import ThemeManager
from mock.mock import MagicMock
from pytestqt.qtbot import QtBot

from note_size.cache.cache_initializer import CacheInitializer
from note_size.cache.cache_storage import CacheStorage
from note_size.cache.item_id_cache import ItemIdCache
from note_size.cache.media_cache import MediaCache
from note_size.calculator.size_calculator import SizeCalculator
from note_size.calculator.size_formatter import SizeFormatter
from note_size.config.config import Config
from note_size.config.config_loader import ConfigLoader
from note_size.config.settings import Settings
from note_size.ui.config.config_ui import ConfigUi
from note_size.ui.config.model_converter import ModelConverter
from note_size.ui.config.ui_model import UiModel
from note_size.ui.deck_browser.collection_size_formatter import CollectionSizeFormatter
from note_size.ui.deck_browser.trash import Trash
from note_size.ui.details_dialog.details_dialog import DetailsDialog
from note_size.ui.editor.button.button_formatter import ButtonFormatter
from note_size.ui.editor.column.item_id_sorter import ItemIdSorter
from note_size.log.logs import Logs
from tests.data import Data


@pytest.fixture
def module_name() -> str:
    return "1188705668"


@pytest.fixture
def profile_manager(base_dir: Path, profile_name: str) -> ProfileManager:
    anki_base_dir: Path = ProfileManager.get_created_base_folder(str(base_dir))
    pm: ProfileManager = ProfileManager(base=anki_base_dir)
    pm.setupMeta()
    pm.create(profile_name)
    pm.openProfile(profile_name)
    pm.save()
    return pm


@pytest.fixture
def profile_dir(profile_manager: ProfileManager) -> Path:
    return Path(profile_manager.profileFolder())


@pytest.fixture
def media_trash_dir(profile_dir: Path) -> Path:
    return profile_dir / "media.trash"


@pytest.fixture
def col(profile_manager: ProfileManager) -> Collection:
    collection_file: str = profile_manager.collectionPath()
    col: Collection = Collection(collection_file)
    yield col
    col.close()


@pytest.fixture
def td(col: Collection, module_dir: Path) -> Data:
    return Data(col, module_dir)


@pytest.fixture
def project_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def base_dir() -> Path:
    return Path(tempfile.mkdtemp(prefix="anki-base-dir"))


@pytest.fixture
def logs_dir(base_dir: Path, module_name: str) -> Path:
    return base_dir / "logs" / "addons" / module_name


@pytest.fixture
def profile_name() -> str:
    return "User1"


@pytest.fixture
def addons_dir(base_dir: Path) -> Path:
    return base_dir / "addons21"


@pytest.fixture
def module_dir(addons_dir: Path, module_name: str, project_dir: Path) -> Path:
    addon_project_dir: Path = project_dir.joinpath("note_size")
    module_dir: Path = addons_dir.joinpath(module_name)
    ignore_patterns: Callable[[Any, list[str]], set[str]] = shutil.ignore_patterns("__pycache__")
    shutil.copytree(addon_project_dir, module_dir, ignore=ignore_patterns)
    return module_dir


@pytest.fixture
def settings(module_dir: Path, module_name: str, logs_dir: Path) -> Settings:
    return Settings(module_dir, module_name, logs_dir)


@pytest.fixture
def config(col: Collection, td: Data) -> Config:
    return td.read_config()


@pytest.fixture
def media_cache(col: Collection, config: Config) -> MediaCache:
    return MediaCache(col, config)


@pytest.fixture
def size_calculator(col: Collection, media_cache: MediaCache) -> SizeCalculator:
    return SizeCalculator(col, media_cache)


@pytest.fixture
def item_id_cache(col: Collection, size_calculator: SizeCalculator, media_cache: MediaCache) -> ItemIdCache:
    return ItemIdCache(col, size_calculator, media_cache)


@pytest.fixture
def cache_storage(settings: Settings) -> CacheStorage:
    return CacheStorage(settings)


@pytest.fixture
def cache_initializer(mw: AnkiQt, media_cache: MediaCache, item_id_cache: ItemIdCache, size_calculator: SizeCalculator,
                      cache_storage: CacheStorage, config: Config) -> CacheInitializer:
    return CacheInitializer(mw, media_cache, item_id_cache, size_calculator, cache_storage, config)


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
def desktop_services() -> QDesktopServices:
    return QDesktopServices()


@pytest.fixture
def config_ui(config: Config, config_loader: ConfigLoader, logs: Logs, cache_initializer: CacheInitializer,
              desktop_services: QDesktopServices, settings: Settings) -> ConfigUi:
    return ConfigUi(config, config_loader, logs, cache_initializer, desktop_services, settings)


@pytest.fixture
def mw(profile_manager: ProfileManager, qapp: QApplication) -> AnkiQt:
    mw_mock: MagicMock = MagicMock()
    mw_mock.pm = profile_manager
    mw_mock.app = qapp
    aqt.mw = mw_mock
    return mw_mock


@pytest.fixture
def ui_model() -> UiModel:
    return UiModel()


@pytest.fixture
def details_dialog(qtbot: QtBot, size_calculator: SizeCalculator, config_ui: ConfigUi, config: Config,
                   settings: Settings, ui_model: UiModel, theme_manager: ThemeManager) -> DetailsDialog:
    ModelConverter.apply_config_to_model(ui_model, config)
    details_dialog: DetailsDialog = DetailsDialog(size_calculator, config_ui, config, settings)
    theme_manager.apply_style()
    qtbot.addWidget(details_dialog)
    return details_dialog


@pytest.fixture
def theme_manager() -> ThemeManager:
    return ThemeManager()
