import logging
from logging import Logger
from urllib.parse import urljoin

from aqt.qt import QVBoxLayout

from ..settings import Settings
from ...config.ui.ui_model import UiModel
from ...config.ui.widgets import TitledSpinBoxLayout, GroupVBox

log: Logger = logging.getLogger(__name__)


class DetailsWindowLayout(QVBoxLayout):
    def __init__(self, model: UiModel, settings: Settings):
        super().__init__()
        self.__model: UiModel = model
        self.__max_filename_length: TitledSpinBoxLayout = TitledSpinBoxLayout(
            'Max filename length:', settings,
            urljoin(settings.docs_base_url, "docs/configuration.md#max-filename-length"),
            0, 1000)
        self.__max_filename_length.add_editing_finished_callback(self.__max_filename_length_editing_finished)
        self.__max_files_to_show: TitledSpinBoxLayout = TitledSpinBoxLayout(
            'Max files to show:', settings,
            urljoin(settings.docs_base_url, "docs/configuration.md#max-files-to-show"),
            0, 100)
        self.__max_files_to_show.add_editing_finished_callback(self.__max_files_to_show_editing_finished)
        self.__group_box: GroupVBox = GroupVBox('Details Window')
        self.__group_box.add_layout(self.__max_filename_length)
        self.__group_box.add_layout(self.__max_files_to_show)
        self.addWidget(self.__group_box)

    def refresh_from_model(self):
        self.__max_filename_length.set_value(self.__model.size_button_details_formatter_max_filename_length)
        self.__max_files_to_show.set_value(self.__model.size_button_details_formatter_max_files_to_show)
        self.__max_filename_length.set_enabled(self.__model.size_button_enabled)
        self.__max_files_to_show.set_enabled(self.__model.size_button_enabled)
        self.__group_box.setEnabled(self.__model.size_button_enabled)

    def __max_filename_length_editing_finished(self):
        self.__model.size_button_details_formatter_max_filename_length = self.__max_filename_length.get_value()

    def __max_files_to_show_editing_finished(self):
        self.__model.size_button_details_formatter_max_files_to_show = self.__max_files_to_show.get_value()
