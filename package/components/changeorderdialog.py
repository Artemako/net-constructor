from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

class ChangeOrderDialog(QDialog):

    def __init__(self, objects, type_objects, parent=None):
        super(ChangeOrderDialog, self).__init__(parent)
        self.__objects = objects
        self.__type_objects = type_objects
        self.__data = []
        
        if self.__type_objects == "nodes":
            self.setWindowTitle("Изменение порядка вершин")
        elif self.__type_objects == "connections":
            self.setWindowTitle("Изменение порядка соединений")
        
        self.layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)  
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)
        self._populate_list()
        
        self.up_button = QPushButton("Вверх")
        self.down_button = QPushButton("Вниз")
        self.up_button.clicked.connect(self._move_item_up)
        self.down_button.clicked.connect(self._move_item_down)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.up_button)
        button_layout.addWidget(self.down_button)

        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(button_layout)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Отмена")

        button_ok_cancel_layout = QHBoxLayout()
        button_ok_cancel_layout.addWidget(self.ok_button)
        button_ok_cancel_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_ok_cancel_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _populate_list(self):
        for index, obj in enumerate(self.__objects):
            obj_name = obj.get("data", {}).get("название", {}).get("value", "")
            
            item_name = ""
            if self.__type_objects == "nodes":
                item_name = f"{index + 1}) {obj_name}"
            elif self.__type_objects == "connections":
                item_name = f"{index + 1}—{index + 2}) {obj_name}"
            
            item = QListWidgetItem(item_name)
            item.setData(Qt.UserRole, obj)
            self.list_widget.addItem(item)

    def _move_item_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentItem(item)

    def _move_item_down(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1: 
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, item)
            self.list_widget.setCurrentItem(item)

    def _get_ordered_objects(self):
        ordered_objects = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            ordered_objects.append(item.data(Qt.UserRole))
        return ordered_objects

    def accept(self):
        self.__data = self._get_ordered_objects()
        super().accept()

    def get_data(self):
        return self.__data
