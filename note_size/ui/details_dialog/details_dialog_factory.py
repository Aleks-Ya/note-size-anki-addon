import logging
from logging import Logger
from typing import Optional

from aqt.theme import ThemeManager
from aqt import QWidget

from .details_dialog import DetailsDialog
from .details_model_filler import DetailsModelFiller
from ...core.cache.bytes_size_cache import BytesSizeCache
from ...core.config.config import Config
from ..config.config_ui import ConfigUi
from ...core.config.settings import Settings
from ...core.cache.file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class DetailsDialogFactory:

    def __init__(self, bytes_size_cache: BytesSizeCache, file_type_helper: FileTypeHelper,
                 details_model_filler: DetailsModelFiller, theme_manager: ThemeManager,
                 config_ui: ConfigUi, config: Config, settings: Settings):
        self.__bytes_size_cache: BytesSizeCache = bytes_size_cache
        self.__file_type_helper: FileTypeHelper = file_type_helper
        self.__details_model_filler: DetailsModelFiller = details_model_filler
        self.__theme_manager: ThemeManager = theme_manager
        self.__config_ui: ConfigUi = config_ui
        self.__config: Config = config
        self.__settings: Settings = settings
        self.__add_cards_editor_button_details_dialog: Optional[DetailsDialog] = None
        self.__browser_editor_button_details_dialog: Optional[DetailsDialog] = None
        self.__browser_button_details_dialog: Optional[DetailsDialog] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_add_cards_browser_editor_button_details_dialog(self, parent: Optional[QWidget]) -> DetailsDialog:
        if not self.__add_cards_editor_button_details_dialog:
            self.__add_cards_editor_button_details_dialog = DetailsDialog(
                parent, self.__bytes_size_cache, self.__file_type_helper, self.__details_model_filler,
                self.__theme_manager, self.__config_ui, self.__config, self.__settings)
        return self.__add_cards_editor_button_details_dialog

    def get_browser_editor_button_details_dialog(self, parent: Optional[QWidget]) -> DetailsDialog:
        if not self.__browser_editor_button_details_dialog:
            self.__browser_editor_button_details_dialog = DetailsDialog(
                parent, self.__bytes_size_cache, self.__file_type_helper, self.__details_model_filler,
                self.__theme_manager, self.__config_ui, self.__config, self.__settings)
        return self.__browser_editor_button_details_dialog

    def get_browser_button_details_dialog(self, parent: Optional[QWidget]) -> DetailsDialog:
        if not self.__browser_button_details_dialog:
            self.__browser_button_details_dialog = DetailsDialog(
                parent, self.__bytes_size_cache, self.__file_type_helper, self.__details_model_filler,
                self.__theme_manager, self.__config_ui, self.__config, self.__settings)
        return self.__browser_button_details_dialog

    def get_all_details_dialogs(self) -> list[DetailsDialog]:
        all_dialogs: list[Optional[DetailsDialog]] = [self.__add_cards_editor_button_details_dialog,
                                                      self.__browser_editor_button_details_dialog,
                                                      self.__browser_button_details_dialog]
        all_present_dialogs: list[DetailsDialog] = [dialog for dialog in all_dialogs if dialog is not None]
        return all_present_dialogs

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
