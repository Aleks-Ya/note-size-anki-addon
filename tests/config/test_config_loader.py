import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Optional

from aqt.addons import AddonManager
from mock.mock import MagicMock

from note_size.config.config import Config
from note_size.config.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        self.module_name: str = "note_size"
        self.addons_dir: Path = Path(tempfile.mkdtemp())
        wm: MagicMock = MagicMock()
        wm.pm.addonFolder.return_value = self.addons_dir
        self.addon_manager: AddonManager = AddonManager(wm)
        self.config_loader: ConfigLoader = ConfigLoader(self.addon_manager, self.module_name)

    def test_empty_addon_dir(self):
        self.__write_meta_json_config({})
        config: Config = self.config_loader.load_config()
        self.assertDictEqual({}, config.config)

    def test_default_values(self):
        self.__copy_config_json_to_addons_dir()
        config: Config = self.config_loader.load_config()
        self.assertDictEqual({
            'Logging': {'Logger Level': 'INFO'},
            'Cache': {'Warmup Enabled': True},
            'Size Button': {
                'Details Window': {
                    'Max Filename Length': 100,
                    'Max Files To Show': 10}}}, config.config)

    def test_actual_values_all(self):
        self.__copy_config_json_to_addons_dir()
        meta_json_config: dict[str, Any] = {
            'Logging': {'Logger Level': 'DEBUG'},
            'Cache': {'Warmup Enabled': False},
            'Size Button': {
                'Details Window': {
                    'Max Filename Length': 200,
                    'Max Files To Show': 20}}}
        self.__write_meta_json_config(meta_json_config)
        config: Config = self.config_loader.load_config()
        self.assertDictEqual(meta_json_config, config.config)

    def test_actual_values_partial(self):
        self.__copy_config_json_to_addons_dir()
        self.__write_meta_json_config({'Size Button': {'Details Window': {'Max Filename Length': 200}}})
        config: Config = self.config_loader.load_config()
        self.assertDictEqual({
            'Logging': {'Logger Level': 'INFO'},
            'Cache': {'Warmup Enabled': True},
            'Size Button': {'Details Window': {
                'Max Filename Length': 200,
                'Max Files To Show': 10}}}, config.config)

    def test_delete_unused_properties(self):
        self.__copy_config_json_to_addons_dir()
        self.__write_meta_json_config({
            'Logging': {'Logger Level': 'INFO'},
            'Size Button': {
                'Details Window': {
                    'Max Filename Length': 200,
                    'Unused Nested': 'Nested 1'
                }},
            'Unused Top': {'Property 1': 'Value 1'}
        })
        config: Config = self.config_loader.load_config()
        self.assertDictEqual({
            'Logging': {'Logger Level': 'INFO'},
            'Cache': {'Warmup Enabled': True},
            'Size Button': {
                'Details Window': {
                    'Max Filename Length': 200,
                    'Max Files To Show': 10}}}, config.config)

    def test_save_loaded_config(self):
        self.__copy_config_json_to_addons_dir()
        self.__write_meta_json_config({
            'Logging': {'Logger Level': 'INFO'},
            'Size Button': {
                'Details Window': {
                    'Max Filename Length': 200,
                    'Unused Nested': 'Nested 1'
                }},
            'Unused Top': {'Property 1': 'Value 1'}
        })
        config_origin: Optional[dict[str, Any]] = self.addon_manager.getConfig(self.module_name)
        self.assertDictEqual({
            'Logging': {'Logger Level': 'INFO'},
            'Cache': {'Warmup Enabled': True},
            'Size Button': {
                'Details Window': {
                    'Max Filename Length': 200,
                    'Unused Nested': 'Nested 1'
                }},
            'Unused Top': {'Property 1': 'Value 1'}}, config_origin)
        config: Config = self.config_loader.load_config()
        self.assertDictEqual({
            'Logging': {'Logger Level': 'INFO'},
            'Cache': {'Warmup Enabled': True},
            'Size Button': {
                'Details Window': {
                    'Max Filename Length': 200,
                    'Max Files To Show': 10}}}, config.config)
        config_saved: Optional[dict[str, Any]] = self.addon_manager.getConfig(self.module_name)
        self.assertDictEqual({
            'Logging': {'Logger Level': 'INFO'},
            'Cache': {'Warmup Enabled': True},
            'Size Button': {'Details Window': {
                'Max Filename Length': 200,
                'Max Files To Show': 10}}}, config_saved)

    def __write_meta_json_config(self, meta_json_config) -> None:
        module_dir: Path = self.__get_module_dir()
        module_dir.mkdir(exist_ok=True)
        meta_json: Path = module_dir.joinpath("meta.json")
        meta_json_content: dict[str, dict[str, Any]] = {
            "config": meta_json_config
        }
        with open(meta_json, 'w') as fp:
            json.dump(meta_json_content, fp, indent=2)

    def __copy_config_json_to_addons_dir(self) -> None:
        project_dir: Path = Path(__file__).parent.parent.parent
        config_json: Path = project_dir.joinpath(self.module_name).joinpath("config.json")
        module_dir: Path = self.__get_module_dir()
        module_dir.mkdir(exist_ok=True)
        shutil.copy(config_json, module_dir)

    def __get_module_dir(self) -> Path:
        return Path(self.addons_dir).joinpath(self.module_name)


if __name__ == '__main__':
    unittest.main()
