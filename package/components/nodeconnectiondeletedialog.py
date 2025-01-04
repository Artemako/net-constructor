from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox

class NodeConnectionDeleteDialog(QDialog):
    def __init__(self, nodes, connections, parent=None):
        super(NodeConnectionDeleteDialog, self).__init__(parent)
        self.setWindowTitle("Удаление узла и соединения")
        
        self.__nodes = nodes
        self.__connections = connections

        # Выпадающий список для выбора узла
        label_node = QLabel("Выберите узел")
        self.combo_box_nodes = QComboBox(self)
        for index, node in enumerate(self.__nodes):
            node_name = node.get("data", {}).get("название", {}).get("value", "")
            self.combo_box_nodes.addItem(f"{index + 1}) {node_name}", node)

        # Выпадающий список для выбора соединения
        label_connection = QLabel("Выберите соединение")
        self.combo_box_connections = QComboBox(self)
        self.update_connections()

        # Кнопки подтверждения и отмены
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Отмена", self)

        # Организация компоновки
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout(self)
        layout.addWidget(label_node)
        layout.addWidget(self.combo_box_nodes)
        layout.addWidget(label_connection)
        layout.addWidget(self.combo_box_connections)
        layout.addLayout(button_layout)

        # Связывание событий
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.combo_box_nodes.currentIndexChanged.connect(self.update_connections)

    def update_connections(self):
        self.combo_box_connections.clear()
        selected_node = self.combo_box_nodes.currentData()
        if not selected_node:
            return

        selected_node_order = selected_node.get("order", 0)
        available_connections = [
            con for con in self.__connections
            if con.get("order", 0) in [selected_node_order - 1, selected_node_order]
        ]
        if not available_connections:
            QMessageBox.warning(self, "Внимание", "Нет доступных соединений для выбранного узла.")
            return
        for con in available_connections:
            prefix = ""
            if con.get("order", 0) == selected_node_order - 1:
                prefix = "Левое)"
            elif con.get("order", 0) == selected_node_order:
                prefix = "Правое)"
            connection_name = con["data"].get("название", {}).get("value", "")
            self.combo_box_connections.addItem(f"{prefix} {connection_name}", con)

    def get_selected_node_and_connection(self):
        return {
            "node": self.combo_box_nodes.currentData(),
            "connection": self.combo_box_connections.currentData()
        }

# 
