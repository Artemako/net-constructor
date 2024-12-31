from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QLabel, QDialogButtonBox, QHBoxLayout, QListWidgetItem
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class DiagramTypeSelectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Выбор типа диаграммы")
        self.setMinimumSize(800, 400)
        
        main_layout = QVBoxLayout(self)
        
        layout = QHBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(200)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 400)  # Увеличиваем минимальный размер
        
        diagrams = [
            ("Круговая диаграмма", "pics/1.png"),
            ("Столбчатая диаграмма", "pics/2.png"),
            ("Линейная диаграмма", "pics/3.png")
        ]
        
        for name, image_path in diagrams:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, image_path)
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
            image_path = current.data(Qt.UserRole)
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            ))

    def get_selected_diagram(self):
        item = self.list_widget.currentItem()
        if item:
            return item.text()
        return None

# Пример использования
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    dialog = DiagramTypeSelectDialog()
    if dialog.exec() == QDialog.Accepted:
        print("Выбранный тип диаграммы: ", dialog.get_selected_diagram())
    
    sys.exit(app.exec())
