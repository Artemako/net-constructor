from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpacerItem,
    QSizePolicy
)
from PySide6.QtCore import QSize

class NodeConnectSelectDialog(QDialog):
    def __init__(
        self, config_diagram_nodes, config_diagram_connections, parent=None
    ):
        super(NodeConnectSelectDialog, self).__init__(parent)
        self.setWindowTitle("Выберите узел и соединение")
        self.config_diagram_nodes = config_diagram_nodes
        
        # Узел
        label_node = QLabel("Узел")
        self.combo_box_nodes = QComboBox(self)
        self.combo_box_nodes.currentIndexChanged.connect(self._update_node_fields)
        
        # Название узла
        label_node_name = QLabel("Название")
        self.line_edit_node_name = QLineEdit()
        
        # Местоположение узла
        self.label_node_place = QLabel("Местоположение") 
        self.line_edit_node_place = QLineEdit()
        
        # Соединение
        label_connection = QLabel("Соединение")
        self.combo_box_connections = QComboBox(self)
        
        # Кнопки
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Отмена", self)

        # Заполняем комбобокс узлов
        self._populate_nodes()
        
        # Заполняем комбобокс соединений
        self._populate_connections(config_diagram_connections)

        # Настройка layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        # Вертикальная пружина для прижатия содержимого вверх
        vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self)
        layout.addWidget(label_node)
        layout.addWidget(self.combo_box_nodes)
        layout.addWidget(label_node_name)
        layout.addWidget(self.line_edit_node_name)
        layout.addWidget(self.label_node_place)
        layout.addWidget(self.line_edit_node_place)
        layout.addWidget(label_connection)
        layout.addWidget(self.combo_box_connections)
        layout.addLayout(button_layout)
        layout.addItem(vertical_spacer)  # Добавляем пружину в конец

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self._update_node_fields()

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