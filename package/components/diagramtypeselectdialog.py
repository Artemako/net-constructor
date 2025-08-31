from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QLabel, QDialogButtonBox, QHBoxLayout, QListWidgetItem,
    QGroupBox, QSizePolicy
)
# from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

import resources_rc

class DiagramTypeSelectDialog(QDialog):
    def __init__(self, global_diagrams, parent=None):
        self.__data = None

        super().__init__(parent)
        
        self.setWindowTitle("Выбор типа диаграммы")
        self.setFixedSize(900, 400)
        
        self.setup_ui(global_diagrams)
        self.setup_connections()

    def setup_ui(self, global_diagrams):
        """Настройка пользовательского интерфейса"""
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
        
        # self.image_label = QLabel()
        # self.image_label.setAlignment(Qt.AlignCenter)
        # self.image_label.setFixedSize(600, 300) 
        
        for key, elem in global_diagrams.items():
            name = elem.get("name", "")
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, elem)
            self.list_widget.addItem(item)
        
        # self.list_widget.currentItemChanged.connect(self.load_image)
        
        selection_layout.addWidget(self.list_widget)
        # selection_layout.addWidget(self.image_label)
        
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
        """Настройка связей между элементами"""
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

    # def load_image(self, current, previous):
    #     if current:
    #         type_id = current.data(Qt.UserRole).get("type_id", "")
    #         image_path = f":/diagram_previews/resources/diagram_previews/{type_id}.png"
    #         pixmap = QPixmap(image_path)
    #         self.image_label.setPixmap(pixmap.scaled(
    #             self.image_label.size(), 
    #             Qt.KeepAspectRatio, 
    #             Qt.SmoothTransformation
    #         ))

    def get_data(self):
        return self.__data
    
    def accept(self):
        self.__data = self.list_widget.currentItem().data(Qt.UserRole)
        super().accept()
