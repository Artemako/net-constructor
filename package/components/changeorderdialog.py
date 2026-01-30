"""Диалог изменения порядка элементов: вершины, соединения, контрольные точки."""

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


class ChangeOrderDialog(QDialog):
    """Диалог изменения порядка узлов, соединений или контрольных секторов."""

    def __init__(self, objects, type_objects, parent=None) -> None:
        super(ChangeOrderDialog, self).__init__(parent)
        self.__objects = objects
        self.__type_objects = type_objects
        self.__data = []
        
        if self.__type_objects == "nodes":
            self.setWindowTitle("Изменение порядка вершин")
        elif self.__type_objects == "connections":
            self.setWindowTitle("Изменение порядка соединений")
        elif self.__type_objects == "control_sectors":
            self.setWindowTitle("Изменение порядка контрольных точек")
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self) -> None:
        """Настройка пользовательского интерфейса диалога."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Группа списка элементов
        list_group = QGroupBox("Список элементов")
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(10, 10, 10, 10)
        list_layout.setSpacing(10)
        
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)  
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)
        self.list_widget.setMinimumHeight(200)
        self._populate_list()
        
        list_layout.addWidget(self.list_widget)
        
        # Кнопки управления порядком
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 10, 0, 0)
        control_layout.setSpacing(10)
        
        self.up_button = QPushButton("Вверх")
        self.down_button = QPushButton("Вниз")
        
        # Добавляем подсказки
        self.up_button.setToolTip("Переместить выбранный элемент вверх")
        self.down_button.setToolTip("Переместить выбранный элемент вниз")
        
        # Устанавливаем политику изменения размера для заполнения всей ширины
        self.up_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.down_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        control_layout.addWidget(self.up_button)
        control_layout.addWidget(self.down_button)
        
        list_layout.addLayout(control_layout)
        list_group.setLayout(list_layout)
        main_layout.addWidget(list_group)
        
        # Кнопки диалога
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(10)
        
        buttons_layout.addStretch()
        
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Отмена")
        
        self.ok_button.setFixedWidth(100)
        self.cancel_button.setFixedWidth(100)
        
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Устанавливаем политику изменения размера
        self.setMinimumSize(400, 350)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setup_connections(self) -> None:
        """Подключение слотов к сигналам виджетов."""
        self.up_button.clicked.connect(self._move_item_up)
        self.down_button.clicked.connect(self._move_item_down)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _populate_list(self) -> None:
        for index, obj in enumerate(self.__objects):
            item_name = ""
            if self.__type_objects == "nodes":
                obj_name = obj.get("data", {}).get("название", {}).get("value", "")
                item_name = f"{index + 1}) {obj_name}"
            elif self.__type_objects == "connections":
                obj_name = obj.get("data", {}).get("название", {}).get("value", "")
                item_name = f"{index + 1}) {obj_name}"
            elif self.__type_objects == "control_sectors":
                obj_name = obj.get("data_pars", {}).get("cs_name", {}).get("value", "")
                item_name = f"{index + 1}) {obj_name}"
            
            item = QListWidgetItem(item_name)
            item.setData(Qt.UserRole, obj)
            self.list_widget.addItem(item)

    def _move_item_up(self) -> None:
        """Перемещает выбранный элемент вверх."""
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentItem(item)

    def _move_item_down(self) -> None:
        """Перемещает выбранный элемент вниз."""
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
