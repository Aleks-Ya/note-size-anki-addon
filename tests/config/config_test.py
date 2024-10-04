from note_size.config.config import Config
from tests.data import Data


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
        'Profiler': {'Enabled': False},
        'Size Button': {
            "Color": {
                "Enabled": False,
                "Levels": [{"Color": "Green", "Max Size": "50 KB"},
                           {"Color": "Yellow", "Max Size": "2 MB"},
                           {"Color": "Red", "Max Size": "100 GB"}]},
            'Enabled': False}}
