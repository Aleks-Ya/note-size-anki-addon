from note_size.config.config import Config
from tests.data import Data


def test_setters():
    config: Config = Data.read_config()
    assert config.get_as_dict() == {
        'Cache': {'Warmup Enabled': True},
        'Deck Browser': {'Show Collection Size': True},
        'Logging': {'Logger Level': 'INFO'},
        'Size Button': {
            "Color": {
                "Enabled": True,
                "Levels": [{"Color": "PaleGreen", "Max Size": "100 KB"},
                           {"Color": "Orange", "Max Size": "1 MB"},
                           {"Color": "LightCoral", "Max Size": None}]},
            'Details Window': {
                'Max Filename Length': 100,
                'Max Files To Show': 10},
            'Enabled': True}}
    config.set_cache_warmup_enabled(False)
    config.set_deck_browser_show_collection_size(False)
    config.set_log_level('DEBUG')
    config.set_size_button_enabled(False)
    config.set_size_button_details_formatter_max_filename_length(50)
    config.set_size_button_details_formatter_max_files_to_show(5)
    config.set_size_button_color_enabled(False)
    config.set_size_button_color_levels([{"Color": "Green", "Max Size": "50 KB"},
                                         {"Color": "Yellow", "Max Size": "2 MB"},
                                         {"Color": "Red", "Max Size": "100 GB"}])
    assert config.get_as_dict() == {
        'Cache': {'Warmup Enabled': False},
        'Deck Browser': {'Show Collection Size': False},
        'Logging': {'Logger Level': 'DEBUG'},
        'Size Button': {
            "Color": {
                "Enabled": False,
                "Levels": [{"Color": "Green", "Max Size": "50 KB"},
                           {"Color": "Yellow", "Max Size": "2 MB"},
                           {"Color": "Red", "Max Size": "100 GB"}]},
            'Details Window': {
                'Max Filename Length': 50,
                'Max Files To Show': 5},
            'Enabled': False}}
