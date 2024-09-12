import logging
from logging import Logger

from anki.notes import Note
from aqt.qt import QDialog, QLabel, QIcon, QGridLayout, QPushButton, QFont, QSize, QMargins, QDialogButtonBox, Qt

from .files_table import FilesTable
from ...calculator.size_calculator import SizeCalculator
from ...calculator.size_formatter import SizeFormatter
from ...config.config import Config
from ..config.config_ui import ConfigUi
from ...config.settings import Settings
from ...types import SizeStr, MediaFile, SizeBytes
from .file_type_helper import FileTypeHelper

log: Logger = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
class DetailsDialog(QDialog):
    __total_size_row: int = 0
    __texts_size_row: int = 1
    __files_size_row: int = 2
    __files_table_row: int = 3
    __button_box_row: int = 4

    def __init__(self, size_calculator: SizeCalculator, file_type_helper: FileTypeHelper, config_ui: ConfigUi,
                 config: Config, settings: Settings):
        super().__init__(parent=None)
        self.__size_calculator: SizeCalculator = size_calculator
        self.__config_ui: ConfigUi = config_ui
        self.setWindowTitle('"Note Size" addon')
        self.__total_size_label: QLabel = self.__total_size_label()
        self.__texts_size_label: QLabel = QLabel()
        self.__files_size_label: QLabel = QLabel()
        self.__files_table: FilesTable = FilesTable(file_type_helper, config, settings)

        self.__settings_icon: QIcon = QIcon(str(settings.module_dir / "ui" / "web" / "setting.png"))

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
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

    def __total_size_label(self) -> QLabel:
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
        button.setStyleSheet("border: none;")
        button.clicked.connect(self.__on_configuration_button_clicked)
        margin: int = 1
        icon_size: QSize = button.size().shrunkBy(QMargins(margin, margin, margin, margin))
        button.setIconSize(icon_size)
        return button

    def __on_configuration_button_clicked(self) -> None:
        self.__config_ui.show_configuration_dialog()

    def __refresh_total_note_size(self, note: Note) -> None:
        size: SizeStr = SizeFormatter.bytes_to_str(
            self.__size_calculator.calculate_note_total_size(note, use_cache=False))
        text: str = f"Total note size: {size}"
        self.__total_size_label.setText(text)

    def __refresh_texts_size(self, note: Note) -> None:
        size: SizeStr = SizeFormatter.bytes_to_str(
            self.__size_calculator.calculate_note_texts_size(note, use_cache=False))
        text: str = f"Texts size: {size}"
        self.__texts_size_label.setText(text)

    def __refresh_files_size(self, note: Note) -> None:
        size: SizeStr = SizeFormatter.bytes_to_str(
            self.__size_calculator.calculate_note_files_size(note, use_cache=False))
        text: str = f"Files size: {size}"
        self.__files_size_label.setText(text)

    def show_note(self, note: Note) -> None:
        self.__refresh_total_note_size(note)
        self.__refresh_texts_size(note)
        self.__refresh_files_size(note)
        file_sizes: dict[MediaFile, SizeBytes] = self.__size_calculator.note_file_sizes(note, use_cache=False)
        self.__files_table.show_files(file_sizes)
        self.show()
        self.__files_table.recalculate_window_sizes()
        self.adjustSize()