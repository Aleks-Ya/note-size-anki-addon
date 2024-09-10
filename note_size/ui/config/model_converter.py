import logging
from logging import Logger

from .ui_model import UiModel
from ...config.config import Config

log: Logger = logging.getLogger(__name__)


class ModelConverter:

    @staticmethod
    def apply_model_to_config(model: UiModel, config: Config):
        config.set_deck_browser_show_collection_size(model.deck_browser_show_collection_size)
        config.set_size_button_enabled(model.size_button_enabled)
        config.set_size_button_color_enabled(model.size_button_color_enabled)
        config.set_size_button_color_levels(model.size_button_color_levels)
        config.set_log_level(model.log_level)
        config.set_cache_warmup_enabled(model.cache_warmup_enabled)
        config.set_store_cache_in_file_enabled(model.store_cache_in_file_enabled)

    @staticmethod
    def apply_config_to_model(model: UiModel, config: Config):
        model.deck_browser_show_collection_size = config.get_deck_browser_show_collection_size()
        model.size_button_enabled = config.get_size_button_enabled()
        model.size_button_color_enabled = config.get_size_button_color_enabled()
        model.size_button_color_levels = config.get_size_button_color_levels()
        model.log_level = config.get_log_level()
        model.cache_warmup_enabled = config.get_cache_warmup_enabled()
        model.store_cache_in_file_enabled = config.get_store_cache_in_file_enabled()
