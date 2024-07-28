from pathlib import Path
from typing import Optional, Callable, Any

from aqt.qt import QHBoxLayout, QLabel, Qt, QSpinBox, QComboBox, QGroupBox, QWidget, QVBoxLayout, QLayout, QPushButton, \
    QIcon, QCheckBox, QDesktopServices, QUrl, QSize

from ...config.settings import Settings


class GroupVBox(QGroupBox):
    def __init__(self, title: Optional[str] = None):
        super().__init__()
        self.__layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.__layout)
        if title:
            self.setTitle(title)

    def set_enabled(self, enabled: bool) -> None:
        self.setEnabled(enabled)

    def add_widget(self, widget: QWidget) -> None:
        self.__layout.addWidget(widget)

    def add_layout(self, layout: QLayout) -> None:
        self.__layout.addLayout(layout)

    def set_alignment(self, alignment: Qt.AlignmentFlag) -> None:
        self.__layout.setAlignment(alignment)


class TitledComboBoxLayout(QHBoxLayout):
    def __init__(self, title: str, settings: Settings, url: Optional[str] = None, items: Optional[list[str]] = None):
        super().__init__()
        label: QLabel = QLabel(title)
        self.__combo_box: QComboBox = QComboBox(None)
        if items:
            self.__combo_box.addItems(items)
        button: InfoButton = InfoButton(url, settings)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(label)
        self.addWidget(self.__combo_box)
        self.addWidget(button)

    def set_current_text(self, current_text: str) -> None:
        self.__combo_box.setCurrentText(current_text)

    def add_current_text_changed_callback(self, callback: Callable[[Any], None]) -> None:
        self.__combo_box.currentTextChanged.connect(callback)


class TitledSpinBoxLayout(QHBoxLayout):
    def __init__(self, title: str, settings: Settings, url: Optional[str] = None, minimum: Optional[int] = None,
                 maximum: Optional[int] = None, value: Optional[int] = None):
        super().__init__()
        self.__label: QLabel = QLabel(title)
        self.__spin_box: QSpinBox = QSpinBox(None)
        if minimum:
            self.__spin_box.setMinimum(minimum)
        if maximum:
            self.__spin_box.setMaximum(maximum)
        if value:
            self.__spin_box.setValue(value)
        button: InfoButton = InfoButton(url, settings)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.__label)
        self.addWidget(self.__spin_box)
        self.addWidget(button)

    def get_value(self) -> int:
        return self.__spin_box.value()

    def set_value(self, value: int) -> None:
        self.__spin_box.setValue(value)

    def set_enabled(self, enabled: bool) -> None:
        self.__label.setEnabled(enabled)
        self.__spin_box.setEnabled(enabled)

    def add_editing_finished_callback(self, callback: Callable[[], None]) -> None:
        self.__spin_box.editingFinished.connect(callback)


class CheckboxWithInfo(QHBoxLayout):
    def __init__(self, text: str, url: str, settings: Settings):
        super().__init__()
        button: InfoButton = InfoButton(url, settings)
        self.__checkbox: QCheckBox = QCheckBox(text)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.__checkbox)
        self.addWidget(button)

    def add_checkbox_listener(self, callback: Callable[[bool], None]) -> None:
        self.__checkbox.stateChanged.connect(callback)

    def is_checked(self) -> bool:
        return self.__checkbox.isChecked()

    def set_checked(self, checked: bool) -> None:
        self.__checkbox.setChecked(checked)


class InfoButton(QPushButton):
    def __init__(self, url: str, settings: Settings):
        super().__init__()
        self.__url: str = url
        icon: Path = settings.module_dir.joinpath("config").joinpath("ui").joinpath("question.png")
        self.setIcon(QIcon(str(icon)))
        size: int = 15
        self.setIconSize(QSize(size, size))
        self.setFixedWidth(size + 6)
        self.clicked.connect(self.__open_link)
        self.setToolTip("Open documentation in browser")
        self.setStyleSheet("border: none;")

    def __open_link(self) -> None:
        QDesktopServices.openUrl(QUrl(self.__url))
