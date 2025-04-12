import json
import os
from pathlib import Path
from typing import Optional

from aqt.addons import AddonManager

from note_size.config.config import Config
from note_size.config.config_loader import ConfigLoader
from note_size.common.types import SignificantDigits
from note_size.config.level_parser import LevelDict, LevelParser
from tests.data import Colors


# When default "config.json" is missing, all properties should be deleted
def test_empty_addon_dir(config_loader: ConfigLoader, module_dir: Path) -> None:
    os.remove(module_dir.joinpath("config.json"))
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {}


# No actual values are set, take all values from default "config.json"
def test_default_values(config_loader: ConfigLoader, module_dir: Path):
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 2},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 2,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Dark Theme Color": "DarkGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Dark Theme Color": "SaddleBrown", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Dark Theme Color": "Maroon", "Max Size": None}]}}}


# Replace default values of all possible properties with actual values
def test_actual_values_all(config_loader: ConfigLoader, module_dir: Path):
    meta_json_config: dict[str, any] = {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 2},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 2,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Dark Theme Color": "DarkGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Dark Theme Color": "SaddleBrown", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Dark Theme Color": "Maroon", "Max Size": None}]}}}
    __write_meta_json_config(meta_json_config, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == meta_json_config


# Some default values are overwritten with actual values
def test_actual_values_partial(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({'Cache': {'Warmup Enabled': False}}, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 2},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 2,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Dark Theme Color": "DarkGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Dark Theme Color": "SaddleBrown", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Dark Theme Color": "Maroon", "Max Size": None}]}}}


# Remove any properties which are not present in "config.json"
def test_delete_unused_properties(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({
        'Logging': {'Logger Level': 'DEBUG', 'UNUSED LEVEL 2 STRING': 'Value 3'},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 1,
            "Color": {
                'UNUSED LEVEL 3 STRING': 'Value 4',
                "Enabled": True,
                "Levels v2": [
                    {"Light Theme Color": "PaleGreen", "Max Size": "100 KB", 'UNUSED LEVEL 4 LIST': 'Value 5'},
                    {"Light Theme Color": "Orange", "Max Size": "1 MB"},
                    {"Light Theme Color": "LightCoral", "Max Size": None}]}, },
        'UNUSED LEVEL 1 DICT': {'Property 1': 'Value 1'},
        'UNUSED LEVEL 1 STRING': 'Value 2'
    }, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 2},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 1,
            "Color": {
                "Enabled": True,
                "Levels v2": [
                    {"Light Theme Color": "PaleGreen", "Max Size": "100 KB", 'UNUSED LEVEL 4 LIST': 'Value 5'},
                    {"Light Theme Color": "Orange", "Max Size": "1 MB"},
                    {"Light Theme Color": "LightCoral", "Max Size": None}]}}}


def test_save_loaded_config(addon_manager: AddonManager, config_loader: ConfigLoader, module_name: str,
                            module_dir: Path):
    __write_meta_json_config({
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 0},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 1,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Max Size": None}]}},
        'Unused Top': {'Property 1': 'Value 1'}
    }, module_dir)
    config_origin: Optional[dict[str, any]] = addon_manager.getConfig(module_name)
    assert config_origin == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 0},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 1,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Max Size": None}]}},
        'Unused Top': {'Property 1': 'Value 1'}}
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 0},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 1,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Max Size": None}]}}}
    config_saved: Optional[dict[str, any]] = addon_manager.getConfig(module_name)
    assert config_saved == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 0},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 1,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Max Size": None}]}}}


def test_write_config(config_loader: ConfigLoader, module_dir: Path) -> None:
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 2},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True,
                         'Significant Digits': 2},
        'Logging': {'Logger Level': 'DEBUG'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': True,
            'Significant Digits': 2,
            "Color": {
                "Enabled": True,
                "Levels v2": [{"Light Theme Color": "PaleGreen", "Dark Theme Color": "DarkGreen", "Max Size": "100 KB"},
                              {"Light Theme Color": "Orange", "Dark Theme Color": "SaddleBrown", "Max Size": "1 MB"},
                              {"Light Theme Color": "LightCoral", "Dark Theme Color": "Maroon", "Max Size": None}]}}}
    config.set_cache_warmup_enabled(False)
    config.set_deck_browser_show_collection_size(False)
    config.set_deck_browser_significant_digits(SignificantDigits(2))
    config.set_browser_significant_digits(SignificantDigits(4))
    config.set_log_level('INFO')
    config.set_size_button_enabled(False)
    config.set_size_button_color_enabled(False)
    config.set_size_button_significant_digits(SignificantDigits(5))
    config.set_size_button_color_levels(
        [LevelDict({LevelParser.light_theme_color_key: Colors.green, "Max Size": "50 KB"}),
         LevelDict({LevelParser.light_theme_color_key: Colors.yellow, "Max Size": "2 MB"}),
         LevelDict({LevelParser.light_theme_color_key: Colors.red, "Max Size": "100 GB"})])
    config_loader.write_config(config)
    act_config: Config = config_loader.load_config()
    assert act_config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': True,
                    'Significant Digits': 4},
        'Cache': {'Store Cache In File Enabled': True,
                  'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': False,
                         'Significant Digits': 2},
        'Logging': {'Logger Level': 'INFO'},
        'Profiler': {'Enabled': False},
        'Size Button': {
            'Enabled': False,
            'Significant Digits': 5,
            "Color": {
                "Enabled": False,
                "Levels v2": [{"Light Theme Color": "Green", "Max Size": "50 KB"},
                              {"Light Theme Color": "Yellow", "Max Size": "2 MB"},
                              {"Light Theme Color": "Red", "Max Size": "100 GB"}]}}}


def __write_meta_json_config(meta_json_config, module_dir: Path) -> None:
    module_dir.mkdir(exist_ok=True)
    meta_json: Path = module_dir.joinpath("meta.json")
    meta_json_content: dict[str, dict[str, any]] = {
        "config": meta_json_config
    }
    with open(meta_json, 'w') as fp:
        # noinspection PyTypeChecker
        json.dump(meta_json_content, fp, indent=2)
