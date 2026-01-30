"""Диалог удаления контрольной точки (выбор из списка)."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class ControlSectorDeleteDialog(QDialog):
    """Диалог выбора и удаления контрольной точки из списка."""

    def __init__(self, control_sectors, parent=None) -> None:
        super(ControlSectorDeleteDialog, self).__init__(parent)
        self.setWindowTitle("Удаление контрольной точки")
        
        self.setup_ui(control_sectors)
        self.setup_connections()
        
    def setup_ui(self, control_sectors) -> None:
        """Настройка пользовательского интерфейса диалога."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Группа списка контрольных точек
        list_group = QGroupBox("Список контрольных точек")
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(10, 10, 10, 10)
        list_layout.setSpacing(10)
        
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumHeight(200)
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        for index, cs in enumerate(control_sectors):
            text = f"""{index + 1}) {cs.get("data_pars", {}).get("cs_name", {}).get("value", "")}"""
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, cs)
            self.list_widget.addItem(item)
            
        list_layout.addWidget(self.list_widget)
        list_group.setLayout(list_layout)
        main_layout.addWidget(list_group)
        
        # Кнопки диалога
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(10)
        
        buttons_layout.addStretch()
        
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Отмена", self)
        
        self.ok_button.setFixedWidth(100)
        self.cancel_button.setFixedWidth(100)
        
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Устанавливаем политику изменения размера
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setup_connections(self):
        """Настройка связей между элементами"""
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_selected_control_sector(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            return selected_item.data(Qt.UserRole)
        return None
