from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel

class NodeConnectSelectDialog(QDialog):
    def __init__(self, config_nodes, config_connections, parent=None):
        super(NodeConnectSelectDialog, self).__init__(parent)
        self.setWindowTitle("Выберите узел и соединение")
        # TODO В зависимости от типа диаграммы выбирать разные поля
        label_node = QLabel("Узел")
        self.combo_box_nodes = QComboBox(self)
        for node_key, node_dict in config_nodes.items():
            node_name = node_dict.get("data", {}).get("название", {}).get("value", "")
            self.combo_box_nodes.addItem(node_name, ({"node_key" : node_key, "node_dict" : node_dict}))
        # TODO В зависимости от типа диаграммы выбирать разные поля
        label_connection = QLabel("Соединение")
        self.combo_box_connections = QComboBox(self)
        print("config_connections" , config_connections)
        for connection_key, connection_dict in config_connections.items():
            connection_name = connection_dict.get("data", {}).get("название", {}).get("value", "")
            self.combo_box_connections.addItem(connection_name, ({"connection_key" : connection_key, "connection_dict" : connection_dict}))
        #
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Отмена", self)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout(self)
        layout.addWidget(label_node)
        layout.addWidget(self.combo_box_nodes)
        layout.addWidget(label_connection)
        layout.addWidget(self.combo_box_connections)
        layout.addLayout(button_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_selected_key_dict_node_and_key_dict_connection(self):
        return {"node" : self.combo_box_nodes.currentData(), "connection" : self.combo_box_connections.currentData()}
    

