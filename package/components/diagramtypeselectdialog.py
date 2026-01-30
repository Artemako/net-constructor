"""Диалог выбора типа диаграммы из списка конфигурации."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QVBoxLayout,
)

import resources_rc


class DiagramTypeSelectDialog(QDialog):
    """Диалог выбора типа диаграммы по списку из конфига."""

    def __init__(self, global_diagrams, parent=None) -> None:
        self.__data = None

        super().__init__(parent)
        
        self.setWindowTitle("Выбор типа диаграммы")
        self.setFixedSize(900, 400)
        
        self.setup_ui(global_diagrams)
        self.setup_connections()

    def setup_ui(self, global_diagrams) -> None:
        """Настройка пользовательского интерфейса диалога."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Группа выбора типа диаграммы
        selection_group = QGroupBox("Выбор типа диаграммы")
        selection_layout = QHBoxLayout()
        selection_layout.setContentsMargins(10, 10, 10, 10)
        selection_layout.setSpacing(10)
        
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(200)
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for key, elem in global_diagrams.items():
            name = elem.get("name", "")
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, elem)
            self.list_widget.addItem(item)

        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

        selection_layout.addWidget(self.list_widget)

        selection_group.setLayout(selection_layout)
        main_layout.addWidget(selection_group)
        
        # Кнопки диалога
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(10)
        
        buttons_layout.addStretch()
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        buttons_layout.addWidget(button_box)
        
        main_layout.addLayout(buttons_layout)
        
        # Устанавливаем политику изменения размера
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setup_connections(self):
        """Настройка связей между элементами."""
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

    def get_data(self):
        return self.__data
    
    def accept(self):
        item = self.list_widget.currentItem()
        if item is None:
            self.reject()
            return
        self.__data = item.data(Qt.UserRole)
        super().accept()
