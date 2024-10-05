from note_size.config.config import Config
from note_size.config.config_listener import ConfigListener
from tests.data import Data


class CountConfigListener(ConfigListener):
    def __init__(self):
        self.counter: int = 0

    def on_config_changed(self):
        self.counter += 1


def test_setters(td: Data):
    config: Config = td.read_config()
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
    config.set_store_cache_in_file_enabled(False)
    config.set_deck_browser_show_collection_size(False)
    config.set_browser_show_found_notes_size(False)
    config.set_log_level('INFO')
    config.set_size_button_enabled(False)
    config.set_size_button_color_enabled(False)
    config.set_profiler_enabled(True)
    config.set_size_button_color_levels([{"Color": "Green", "Max Size": "50 KB"},
                                         {"Color": "Yellow", "Max Size": "2 MB"},
                                         {"Color": "Red", "Max Size": "100 GB"}])
    assert config.get_as_dict() == {
        'Browser': {'Show Found Notes Size': False},
        'Cache': {
            'Store Cache In File Enabled': False,
            'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': False},
        'Logging': {'Logger Level': 'INFO'},
        'Profiler': {'Enabled': True},
        'Size Button': {
            "Color": {
                "Enabled": False,
                "Levels": [{"Color": "Green", "Max Size": "50 KB"},
                           {"Color": "Yellow", "Max Size": "2 MB"},
                           {"Color": "Red", "Max Size": "100 GB"}]},
            'Enabled': False}}


def test_fire_config_changed(td: Data):
    config: Config = td.read_config()
    listener: CountConfigListener = CountConfigListener()
    config.add_listener(listener)
    assert listener.counter == 0
    config.fire_config_changed()
    assert listener.counter == 1
    config.fire_config_changed()
    assert listener.counter == 2
