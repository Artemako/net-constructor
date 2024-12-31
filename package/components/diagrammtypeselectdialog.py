from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QLabel, QDialogButtonBox, QHBoxLayout, QListWidgetItem
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

import resources_rc

class DiagramTypeSelectDialog(QDialog):
    def __init__(self, global_diagramms, parent=None):
        self.__data = None

        super().__init__(parent)
        
        self.setWindowTitle("Выбор типа диаграммы")
        self.setFixedSize(900, 400)
        
        main_layout = QVBoxLayout(self)
        
        layout = QHBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(200)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(600, 300) 
        
        for elem in global_diagramms:
            diagramm_name = elem.get("diagramm_name", "")
            item = QListWidgetItem(diagramm_name)
            item.setData(Qt.UserRole, elem)
            self.list_widget.addItem(item)
        
        self.list_widget.currentItemChanged.connect(self.load_image)
        
        layout.addWidget(self.list_widget)
        layout.addWidget(self.image_label)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        main_layout.addLayout(layout)
        main_layout.addWidget(button_box)

    def load_image(self, current, previous):
        if current:
            diagramm_type_id = current.data(Qt.UserRole).get("diagramm_type_id", "")
            image_path = f":/diagramm_previews/resources/diagramm_previews/{diagramm_type_id}.png"
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            ))

    def get_data(self):
        return self.__data
    
    def accept(self):
        self.__data = self.list_widget.currentItem().data(Qt.UserRole)
        super().accept()