import json
import os
from pathlib import Path
from typing import Any, Optional

from aqt.addons import AddonManager

from note_size.config.config import Config
from note_size.config.config_loader import ConfigLoader


def test_empty_addon_dir(config_loader: ConfigLoader, module_dir: Path) -> None:
    os.remove(module_dir.joinpath("config.json"))
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {}


def test_default_values(config_loader: ConfigLoader, module_dir: Path):
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True}}


def test_actual_values_all(config_loader: ConfigLoader, module_dir: Path):
    meta_json_config: dict[str, Any] = {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True}}
    __write_meta_json_config(meta_json_config, module_dir)
    config: Config = config_loader.load_config()
    assert meta_json_config == config.get_as_dict()


def test_actual_values_partial(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({'Size Button': {'Cache': {'Warmup Enabled': False}}}, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True}}


def test_delete_unused_properties(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]}, },
        'Unused Top': {'Property 1': 'Value 1'}
    }, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True}}


def test_save_loaded_config(addon_manager: AddonManager, config_loader: ConfigLoader, module_name: str,
                            module_dir: Path):
    __write_meta_json_config({
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True},
        'Unused Top': {'Property 1': 'Value 1'}
    }, module_dir)
    config_origin: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_origin == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True},
        'Unused Top': {'Property 1': 'Value 1'}}
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True}}
    config_saved: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_saved == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True}}


def test_write_config(config_loader: ConfigLoader, module_dir: Path) -> None:
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Enabled': True}}
    config.set_cache_warmup_enabled(False)
    config.set_deck_browser_show_collection_size(False)
    config.set_log_level('INFO')
    config.set_size_button_enabled(False)
    config.set_size_button_color_enabled(False)
    config.set_size_button_color_levels([{"Color": "Green", "Max Size": "50 KB"},
                                         {"Color": "Yellow", "Max Size": "2 MB"},
                                         {"Color": "Red", "Max Size": "100 GB"}])
    config_loader.write_config(config)
    act_config: Config = config_loader.load_config()
    assert act_config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True},
        'Cache': {
            'Store Cache In File Enabled': True,
            'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': False},
        'Logging': {'Logger Level': 'INFO'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": False,
                "Levels": [{"Color": "Green", "Max Size": "50 KB"},
                           {"Color": "Yellow", "Max Size": "2 MB"},
                           {"Color": "Red", "Max Size": "100 GB"}]},
            'Enabled': False}}


def __write_meta_json_config(meta_json_config, module_dir: Path) -> None:
    module_dir.mkdir(exist_ok=True)
    meta_json: Path = module_dir.joinpath("meta.json")
    meta_json_content: dict[str, dict[str, Any]] = {
        "config": meta_json_config
    }
    with open(meta_json, 'w') as fp:
        json.dump(meta_json_content, fp, indent=2)
