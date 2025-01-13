from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox


class ConfirmChangingDiagramType(QDialog):
    def __init__(self, new_diagram, parent=None):
        super(ConfirmChangingDiagramType, self).__init__(parent)
        self.__new_diagram = new_diagram
        #
        self.setWindowTitle("Подтверждение")
        #
        diagram_name = self.__new_diagram.get("name", "")
        self.label = QLabel(f'Вы уверены, что хотите изменить тип диаграммы на "{diagram_name}"?')
        
        self.ok_button = QPushButton("ОК")
        self.cancel_button = QPushButton("Отмена")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

