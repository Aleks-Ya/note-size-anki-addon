from note_size.config.config import Config
from note_size.config.config_listener import ConfigListener
from note_size.common.types import SignificantDigits
from note_size.config.level_parser import LevelDict, LevelParser
from tests.data import Data, Colors


class CountConfigListener(ConfigListener):
    def __init__(self):
        self.counter: int = 0

    def on_config_changed(self):
        self.counter += 1


def test_setters(td: Data):
    config: Config = td.read_config()
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
                "Levels": [{"Light Theme Color": "PaleGreen", "Dark Theme Color": "DarkGreen", "Max Size": "100 KB"},
                           {"Light Theme Color": "Orange", "Dark Theme Color": "SaddleBrown", "Max Size": "1 MB"},
                           {"Light Theme Color": "LightCoral", "Dark Theme Color": "Maroon", "Max Size": None}]}}}

    exp_color_levels: list[LevelDict] = [
        LevelDict({LevelParser.light_theme_color_key: Colors.green, "Max Size": "50 KB"}),
        LevelDict({LevelParser.light_theme_color_key: Colors.yellow, "Max Size": "2 MB"}),
        LevelDict({LevelParser.light_theme_color_key: Colors.red, "Max Size": "100 GB"})]
    config.set_cache_warmup_enabled(False)
    config.set_store_cache_in_file_enabled(False)
    config.set_deck_browser_show_collection_size(False)
    config.set_deck_browser_significant_digits(SignificantDigits(6))
    config.set_browser_show_found_notes_size(False)
    config.set_browser_significant_digits(SignificantDigits(4))
    config.set_log_level('INFO')
    config.set_size_button_enabled(False)
    config.set_size_button_significant_digits(SignificantDigits(5))
    config.set_size_button_color_enabled(False)
    config.set_profiler_enabled(True)
    config.set_size_button_color_levels(exp_color_levels)
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': False,
                    'Significant Digits': 4},
        'Cache': {'Store Cache In File Enabled': False,
                  'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': False,
                         'Significant Digits': 6},
        'Logging': {'Logger Level': 'INFO'},
        'Profiler': {'Enabled': True},
        'Size Button': {
            'Enabled': False,
            'Significant Digits': 5,
            "Color": {
                "Enabled": False,
                "Levels": exp_color_levels}}}

    assert config.get_cache_warmup_enabled() == False
    assert config.get_store_cache_in_file_enabled() == False
    assert config.get_deck_browser_show_collection_size() == False
    assert config.get_deck_browser_significant_digits() == SignificantDigits(6)
    assert config.get_browser_show_found_notes_size() == False
    assert config.get_browser_significant_digits() == SignificantDigits(4)
    assert config.get_log_level() == 'INFO'
    assert config.get_size_button_enabled() == False
    assert config.get_size_button_significant_digits() == SignificantDigits(5)
    assert config.get_size_button_color_enabled() == False
    assert config.get_profiler_enabled() == True
    assert config.get_size_button_color_levels() == exp_color_levels


def test_fire_config_changed(td: Data):
    config: Config = td.read_config()
    listener: CountConfigListener = CountConfigListener()
    config.add_listener(listener)
    assert listener.counter == 0
    config.fire_config_changed()
    assert listener.counter == 1
    config.fire_config_changed()
    assert listener.counter == 2
