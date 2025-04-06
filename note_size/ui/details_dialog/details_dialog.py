import logging
from datetime import datetime
from logging import Logger
from typing import Sequence, Optional

from anki.notes import Note, NoteId
from aqt.qt import QDialog, QLabel, QGridLayout, QFont, QDialogButtonBox, Qt, QWidget
from aqt.theme import ThemeManager

from .configuration_button import ConfigurationButton
from .details_model import DetailsModel
from .details_model_filler import DetailsModelFiller
from .files_table import FilesTable
from ..theme.theme_listener import ThemeListener
from ...calculator.size_calculator import SizeCalculator
from ...calculator.size_formatter import SizeFormatter
from ...config.config import Config
from ..config.config_ui import ConfigUi
from ...config.settings import Settings
from .file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class DetailsDialog(QDialog, ThemeListener):
    __total_size_row: int = 0
    __texts_size_row: int = 1
    __files_size_row: int = 2
    __files_table_row: int = 3
    __button_box_row: int = 4

    def __init__(self, size_calculator: SizeCalculator, size_formatter: SizeFormatter, file_type_helper: FileTypeHelper,
                 details_model_filler: DetailsModelFiller, theme_manager: ThemeManager, config_ui: ConfigUi,
                 config: Config, settings: Settings):
        super().__init__(parent=None)
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__model: DetailsModel = DetailsModel()
        self.__details_model_filler: DetailsModelFiller = details_model_filler
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('"Note Size" addon')
        self.__configuration_button: ConfigurationButton = ConfigurationButton(theme_manager, config_ui, settings)
        self.__total_size_label: QLabel = self.__total_size_label()
        self.__texts_size_label: QLabel = QLabel()
        self.__files_size_label: QLabel = QLabel()
        self.__files_table: FilesTable = FilesTable(file_type_helper, size_formatter, theme_manager, config, settings)

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        # noinspection PyUnresolvedReferences
        button_box.rejected.connect(self.__close)

        layout: QGridLayout = QGridLayout(self)

        layout.addWidget(self.__total_size_label, self.__total_size_row, 0)
        # noinspection PyArgumentList
        layout.addWidget(self.__configuration_button, self.__total_size_row, 1, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.__texts_size_label, self.__texts_size_row, 0)
        layout.addWidget(self.__files_size_label, self.__files_size_row, 0)
        layout.addWidget(self.__files_table, self.__files_table_row, 0, 1, 2)
        layout.addWidget(button_box, self.__button_box_row, 1)

        layout.setRowStretch(self.__total_size_row, 0)
        layout.setRowStretch(self.__texts_size_row, 0)
        layout.setRowStretch(self.__files_size_row, 0)
        layout.setRowStretch(self.__files_table_row, 1)
        layout.setRowStretch(self.__button_box_row, 0)

        self.setLayout(layout)
        self.setMinimumSize(300, 200)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_note(self, note: Note, parent: Optional[QWidget] = None) -> None:
        self.__model = self.__details_model_filler.prepare_note_model(note)
        self.__files_table.prepare_items(self.__model.file_sizes)
        self.__show_model(parent)

    def prepare_show_notes(self, note_ids: Sequence[NoteId]) -> None:
        log.debug(f"Start showing notes: {len(note_ids)}")
        start_time: datetime = datetime.now()
        self.__model: DetailsModel = self.__details_model_filler.prepare_notes_model(note_ids)
        self.__files_table.prepare_items(self.__model.file_sizes)
        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Data preparation for showing notes finished: duration_sec={duration_sec}")

    def show_notes(self, parent: Optional[QWidget] = None) -> None:
        log.debug("Start showing notes")
        start_time: datetime = datetime.now()
        self.__show_model(parent)
        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Showing notes finished: duration_sec={duration_sec}")

    def on_theme_changed(self, theme_manager: ThemeManager):
        log.debug("Theme did changed")
        self.__configuration_button.on_theme_changed(theme_manager)
        self.__files_table.on_theme_changed(theme_manager)

    def __close(self):
        self.__files_table.clear_rows()
        self.close()

    @staticmethod
    def __total_size_label() -> QLabel:
        font: QFont = QFont()
        font.setPointSize(16)
        font.setWeight(QFont.Weight.Bold)
        label: QLabel = QLabel()
        label.setFont(font)
        return label

    def __show_model(self, parent: Optional[QWidget]) -> None:
        log.debug(f"Set details dialog parent: {parent}")
        self.setParent(parent)
        start_time: datetime = datetime.now()
        self.__total_size_label.setText(self.__model.total_note_size_text)
        self.__texts_size_label.setText(self.__model.texts_note_size_text)
        self.__files_size_label.setText(self.__model.files_note_size_text)
        self.__files_table.show_files()
        # noinspection PyUnresolvedReferences
        self.show()
        self.__files_table.recalculate_window_sizes()
        self.adjustSize()
        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Displaying details dialog duration sec: {duration_sec}")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
