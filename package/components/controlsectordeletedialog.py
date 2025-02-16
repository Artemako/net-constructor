from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QListWidgetItem,
)
from PySide6.QtCore import Qt


class ControlSectorDeleteDialog(QDialog):
    def __init__(self, control_sectors, parent=None):
        super(ControlSectorDeleteDialog, self).__init__(parent)
        self.setWindowTitle("Удаление контрольной точки")
        #
        layout = QVBoxLayout(self)
        #
        self.list_widget = QListWidget(self)
        for cs in control_sectors:
            item = QListWidgetItem(cs.get("cs_name", ""))
            item.setData(Qt.UserRole, cs)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)
        #
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Отмена", self)
        #
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        #
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        #
        self.setLayout(layout)

    def get_selected_control_sector(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            return selected_item.data(Qt.UserRole)
        return None
