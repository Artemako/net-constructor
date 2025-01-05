from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox


class ConfirmChangingDiagrammType(QDialog):
    def __init__(self, new_diagramm, parent=None):
        super(ConfirmChangingDiagrammType, self).__init__(parent)
        self.__new_diagramm = new_diagramm
        #
        self.setWindowTitle("Подтверждение")
        #
        diagramm_name = self.__new_diagramm.get("name", "")
        self.label = QLabel(f'Вы уверены, что хотите изменить тип диаграммы на "{diagramm_name}"?')
        
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

