import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Optional

import pytest
from aqt.addons import AddonManager
from mock.mock import MagicMock

from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.config.config_loader import ConfigLoader


@pytest.fixture
def addons_dir() -> Path:
    return Path(tempfile.mkdtemp())


@pytest.fixture
def module_dir(addons_dir: Path, module_name: str) -> Path:
    return addons_dir.joinpath(module_name)


@pytest.fixture
def addon_manager(addons_dir: Path) -> AddonManager:
    wm: MagicMock = MagicMock()
    wm.pm.addonFolder.return_value = addons_dir
    return AddonManager(wm)


@pytest.fixture
def config_loader(addon_manager: AddonManager, settings: Settings) -> ConfigLoader:
    return ConfigLoader(addon_manager, settings)


def test_empty_addon_dir(config_loader: ConfigLoader, module_dir: Path) -> None:
    __write_meta_json_config({}, module_dir)
    config: Config = config_loader.load_config()
    assert config.as_dict() == {}


def test_default_values(config_loader: ConfigLoader, module_name: str, module_dir: Path):
    __copy_config_json_to_addons_dir(module_name, module_dir)
    config: Config = config_loader.load_config()
    assert config.as_dict() == {
        'Cache': {'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 100,
                'Max Files To Show': 10},
            'Enabled': True}}


def test_actual_values_all(config_loader: ConfigLoader, module_name: str, module_dir: Path):
    __copy_config_json_to_addons_dir(module_name, module_dir)
    meta_json_config: dict[str, Any] = {
        'Cache': {'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Max Files To Show': 20},
            'Enabled': True}}
    __write_meta_json_config(meta_json_config, module_dir)
    config: Config = config_loader.load_config()
    assert meta_json_config == config.as_dict()


def test_actual_values_partial(module_name: str, module_dir: Path, config_loader: ConfigLoader):
    __copy_config_json_to_addons_dir(module_name, module_dir)
    __write_meta_json_config({'Size Button': {'Details Window': {'Max Filename Length': 200}}}, module_dir)
    config: Config = config_loader.load_config()
    assert config.as_dict() == {
        'Cache': {'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Max Files To Show': 10},
            'Enabled': True}}


def test_delete_unused_properties(module_name: str, module_dir: Path, config_loader: ConfigLoader):
    __copy_config_json_to_addons_dir(module_name, module_dir)
    __write_meta_json_config({
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Unused Nested': 'Nested 1'}},
        'Unused Top': {'Property 1': 'Value 1'}
    }, module_dir)
    config: Config = config_loader.load_config()
    assert config.as_dict() == {
        'Cache': {'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Max Files To Show': 10},
            'Enabled': True}}


def test_save_loaded_config(addon_manager: AddonManager, config_loader: ConfigLoader, module_name: str,
                            module_dir: Path):
    __copy_config_json_to_addons_dir(module_name, module_dir)
    __write_meta_json_config({
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Unused Nested': 'Nested 1'},
            'Enabled': True},
        'Unused Top': {'Property 1': 'Value 1'}
    }, module_dir)
    config_origin: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_origin == {
        'Cache': {'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Unused Nested': 'Nested 1'},
            'Enabled': True},
        'Unused Top': {'Property 1': 'Value 1'}}
    config: Config = config_loader.load_config()
    assert config.as_dict() == {
        'Cache': {'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Max Files To Show': 10},
            'Enabled': True}}
    config_saved: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_saved == {
        'Cache': {'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB", "Min Size": None},
                           {"Color": "Orange", "Max Size": "1 MB", "Min Size": "100 KB"},
                           {"Color": "LightCoral", "Max Size": None, "Min Size": "1 MB"}]},
            'Details Window': {
                'Max Filename Length': 200,
                'Max Files To Show': 10},
            'Enabled': True}}


def __write_meta_json_config(meta_json_config, module_dir: Path) -> None:
    module_dir.mkdir(exist_ok=True)
    meta_json: Path = module_dir.joinpath("meta.json")
    meta_json_content: dict[str, dict[str, Any]] = {
        "config": meta_json_config
    }
    with open(meta_json, 'w') as fp:
        json.dump(meta_json_content, fp, indent=2)


def __copy_config_json_to_addons_dir(module_name: str, module_dir: Path) -> None:
    project_dir: Path = Path(__file__).parent.parent.parent
    config_json: Path = project_dir.joinpath(module_name).joinpath("config.json")
    module_dir.mkdir(exist_ok=True)
    shutil.copy(config_json, module_dir)
