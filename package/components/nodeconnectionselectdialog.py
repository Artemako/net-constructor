"""Диалог выбора узла и соединения для редактирования."""

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class NodeConnectSelectDialog(QDialog):
    """Диалог выбора узла и соединения по конфигу диаграммы."""

    def __init__(
        self, config_diagram_nodes, config_diagram_connections, parent=None
    ) -> None:
        super(NodeConnectSelectDialog, self).__init__(parent)
        self.setWindowTitle("Выберите узел и соединение")
        self.config_diagram_nodes = config_diagram_nodes
        
        self.setup_ui()
        self.setup_connections()
        
        # Заполняем комбобокс узлов
        self._populate_nodes()
        
        # Заполняем комбобокс соединений
        self._populate_connections(config_diagram_connections)
        
        self._update_node_fields()

    def setup_ui(self) -> None:
        """Настройка пользовательского интерфейса диалога."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Группа выбора узла
        node_group = QGroupBox("Выбор узла")
        node_layout = QVBoxLayout()
        node_layout.setContentsMargins(10, 10, 10, 10)
        node_layout.setSpacing(10)
        
        # Узел
        label_node = QLabel("Узел:")
        self.combo_box_nodes = QComboBox(self)
        self.combo_box_nodes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        node_layout.addWidget(label_node)
        node_layout.addWidget(self.combo_box_nodes)
        
        # Название узла
        label_node_name = QLabel("Название:")
        self.line_edit_node_name = QLineEdit()
        self.line_edit_node_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        node_layout.addWidget(label_node_name)
        node_layout.addWidget(self.line_edit_node_name)
        
        # Местоположение узла
        self.label_node_place = QLabel("Местоположение:")
        self.line_edit_node_place = QLineEdit()
        self.line_edit_node_place.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        node_layout.addWidget(self.label_node_place)
        node_layout.addWidget(self.line_edit_node_place)
        
        node_group.setLayout(node_layout)
        main_layout.addWidget(node_group)
        
        # Группа выбора соединения
        connection_group = QGroupBox("Выбор соединения")
        connection_layout = QVBoxLayout()
        connection_layout.setContentsMargins(10, 10, 10, 10)
        connection_layout.setSpacing(10)
        
        # Соединение
        label_connection = QLabel("Соединение:")
        self.combo_box_connections = QComboBox(self)
        self.combo_box_connections.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        connection_layout.addWidget(label_connection)
        connection_layout.addWidget(self.combo_box_connections)
        
        connection_group.setLayout(connection_layout)
        main_layout.addWidget(connection_group)
        
        # Вертикальная пружина для прижатия содержимого вверх
        vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(vertical_spacer)
        
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
        self.setMinimumSize(400, 350)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setup_connections(self):
        """Настройка связей между элементами"""
        self.combo_box_nodes.currentIndexChanged.connect(self._update_node_fields)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _populate_nodes(self):
        """Заполняет комбобокс узлами"""
        self.combo_box_nodes.clear()
        for node_key, node_dict in self.config_diagram_nodes.items():
            node_name = node_dict.get("object_data", {}).get("название", {}).get("value", "")
            self.combo_box_nodes.addItem(
                node_name, ({"node_key": node_key, "node_dict": node_dict})
            )

    def _populate_connections(self, config_diagram_connections):
        """Заполняет комбобокс соединениями"""
        self.combo_box_connections.clear()
        for connection_key, connection_dict in config_diagram_connections.items():
            connection_name = (
                connection_dict.get("object_data", {}).get("название", {}).get("value", "")
            )
            self.combo_box_connections.addItem(
                connection_name,
                (
                    {
                        "connection_key": connection_key,
                        "connection_dict": connection_dict,
                    }
                ),
            )

    def _update_node_fields(self):
        """Обновляет поля узла при изменении выбора"""
        current_data = self.combo_box_nodes.currentData()
        if current_data:
            node_dict = current_data["node_dict"]
            object_data = node_dict.get("object_data", {})
            
            # Обновляем название
            node_name = object_data.get("название", {}).get("value", "")
            self.line_edit_node_name.setText(node_name)
            
            # Проверяем наличие поля "местоположение" в object_data (независимо от значения)
            has_place_field = "местоположение" in object_data
            self.label_node_place.setVisible(has_place_field)
            self.line_edit_node_place.setVisible(has_place_field)
            
            # Если поле есть - заполняем его текущим значением
            if has_place_field:
                node_place = object_data["местоположение"].get("value", "")
                self.line_edit_node_place.setText(node_place)
            
            # Подстраиваем размер окна
            self.adjustSize()

    def get_selected_key_dict_node_and_key_dict_connection(self):
        node_data = self.combo_box_nodes.currentData()
        node_dict = node_data["node_dict"].copy()
        object_data = node_dict.get("object_data", {}).copy()
        
        # Обновляем название
        node_name = self.line_edit_node_name.text()
        if "название" in object_data or node_name:
            if "название" not in object_data:
                object_data["название"] = {"value": node_name}
            else:
                object_data["название"]["value"] = node_name
        
        # Обновляем местоположение, если поле существует (независимо от видимости)
        if "местоположение" in object_data:
            node_place = self.line_edit_node_place.text()
            object_data["местоположение"]["value"] = node_place
        
        node_dict["object_data"] = object_data
        
        return {
            "node": {
                "node_key": node_data["node_key"],
                "node_dict": node_dict
            },
            "connection": self.combo_box_connections.currentData()
        }