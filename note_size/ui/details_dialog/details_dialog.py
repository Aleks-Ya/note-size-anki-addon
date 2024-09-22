import logging
from datetime import datetime
from logging import Logger

from anki.notes import Note
from aqt.qt import QDialog, QLabel, QIcon, QGridLayout, QPushButton, QFont, QSize, QMargins, QDialogButtonBox, Qt

from .details_model import DetailsModel
from .details_model_filler import DetailsModelFiller
from .files_table import FilesTable
from ...calculator.size_calculator import SizeCalculator
from ...calculator.size_formatter import SizeFormatter
from ...config.config import Config
from ..config.config_ui import ConfigUi
from ...config.settings import Settings
from .file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


class DetailsDialog(QDialog):
    __total_size_row: int = 0
    __texts_size_row: int = 1
    __files_size_row: int = 2
    __files_table_row: int = 3
    __button_box_row: int = 4

    def __init__(self, size_calculator: SizeCalculator, size_formatter: SizeFormatter, file_type_helper: FileTypeHelper,
                 details_model_filler: DetailsModelFiller, config_ui: ConfigUi, config: Config, settings: Settings):
        super().__init__(parent=None)
        self.__size_calculator: SizeCalculator = size_calculator
        self.__size_formatter: SizeFormatter = size_formatter
        self.__model: DetailsModel = DetailsModel()
        self.__details_model_filler: DetailsModelFiller = details_model_filler
        self.__config_ui: ConfigUi = config_ui
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('"Note Size" addon')
        self.__total_size_label: QLabel = self.__total_size_label()
        self.__texts_size_label: QLabel = QLabel()
        self.__files_size_label: QLabel = QLabel()
        self.__files_table: FilesTable = FilesTable(file_type_helper, size_formatter, config, settings)

        self.__settings_icon: QIcon = QIcon(str(settings.module_dir / "ui" / "web" / "setting.png"))

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        # noinspection PyUnresolvedReferences
        button_box.rejected.connect(self.__close)

        layout: QGridLayout = QGridLayout(self)

        layout.addWidget(self.__total_size_label, self.__total_size_row, 0)
        # noinspection PyArgumentList
        layout.addWidget(self.__configuration_button(), self.__total_size_row, 1, alignment=Qt.AlignmentFlag.AlignRight)
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

    def __configuration_button(self) -> QPushButton:
        button: QPushButton = QPushButton()
        button.setIcon(self.__settings_icon)
        button.setIconSize(button.sizeHint())
        button.setFixedSize(self.__settings_icon.actualSize(button.iconSize()))
        # noinspection PyUnresolvedReferences
        button.setStyleSheet("border: none;")
        # noinspection PyUnresolvedReferences
        button.clicked.connect(self.__on_configuration_button_clicked)
        margin: int = 1
        # noinspection PyUnresolvedReferences
        icon_size: QSize = button.size().shrunkBy(QMargins(margin, margin, margin, margin))
        button.setIconSize(icon_size)
        return button

    def __on_configuration_button_clicked(self) -> None:
        self.__config_ui.show_configuration_dialog()

    def show_note(self, note: Note) -> None:
        self.__model = self.__details_model_filler.prepare_note_model(note)
        self.__show_model()

    def __show_model(self) -> None:
        start_time: datetime = datetime.now()
        self.__total_size_label.setText(self.__model.total_note_size_text)
        self.__texts_size_label.setText(self.__model.texts_note_size_text)
        self.__files_size_label.setText(self.__model.files_note_size_text)
        self.__files_table.show_files(self.__model.file_sizes)
        # noinspection PyUnresolvedReferences
        self.show()
        self.__files_table.recalculate_window_sizes()
        self.adjustSize()
        end_time: datetime = datetime.now()
        duration_sec: int = round((end_time - start_time).total_seconds())
        log.info(f"Displaying details dialog duration sec: {duration_sec}")
