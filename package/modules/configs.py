import json


class Configs:
    def __init__(self):
        self.__global = {}
        self.__nodes = {}
        self.__connections = {}
        self.__cable_lists = {}

    def load_configs(self, dir_app):
        with open(dir_app + "/configs/config_global.json", "r", encoding="utf-8") as f:
            self.__global = json.load(f)
        with open(dir_app + "/configs/config_nodes.json", "r", encoding="utf-8") as f:
            self.__nodes = json.load(f)
        with open(
            dir_app + "/configs/config_connections.json", "r", encoding="utf-8"
        ) as f:
            self.__connections = json.load(f)
        with open(
            dir_app + "/configs/config_cable_lists.json", "r", encoding="utf-8"
        ) as f:
            self.__cable_lists = json.load(f)

    def save_cable_lists(self, dir_app):
        """Сохраняет списки кабелей в файл"""
        with open(
            dir_app + "/configs/config_cable_lists.json", "w", encoding="utf-8"
        ) as f:
            json.dump(self.__cable_lists, f, ensure_ascii=False, indent=4)

    def get_cable_list(self) -> list:
        """Возвращает список кабелей"""
        return self.__cable_lists.get("cable_list", [])

    def update_cable_list(self, cables: list):
        """Обновляет список кабелей"""
        self.__cable_lists["cable_list"] = cables

    def get_node(self, node_id: str) -> dict:
        return self.__nodes.get(node_id, {})

    def get_connection(self, connection_id: str) -> dict:
        return self.__connections.get(connection_id, {})

    def get_nodes(self) -> dict:
        return self.__nodes

    def get_connections(self) -> dict:
        return self.__connections

    def get_config_diagrams(self) -> dict:
        diagrams = self.__global.get("diagrams", {})
        return dict(sorted(diagrams.items(), key=lambda x: x[1].get("order", 0)))


    def get_config_control_sectors(self) -> dict:
        control_sectors_config = self.__global.get("control_sectors_config", {})
        return dict(
            sorted(control_sectors_config.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_diagram_parameters_by_type_id(self, diagram_type_id) -> dict:
        diagrams = self.__global.get("diagrams", {})
        parameters = diagrams.get(str(diagram_type_id), {}).get("parameters", {})
        return dict(sorted(parameters.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_diagram_nodes_by_type_id(self, diagram_type_id) -> dict:
        diagrams = self.__global.get("diagrams", {})
        id_nodes = diagrams.get(str(diagram_type_id), {}).get("id_nodes", [])
        config_diagram_nodes = {
            node_type_id: self.get_node(node_type_id) for node_type_id in id_nodes
        }
        return config_diagram_nodes

    def get_config_diagram_connections_by_type_id(self, diagram_type_id) -> dict:
        diagrams = self.__global.get("diagrams", {})
        id_connections = diagrams.get(str(diagram_type_id), {}).get(
            "id_connections", []
        )
        config_diagram_connections = {
            connection_type_id: self.get_connection(connection_type_id)
            for connection_type_id in id_connections
        }
        return config_diagram_connections

    def get_config_node_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        object_data = self.get_node(node_id).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_node_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        type_object_data = self.get_node(node_id).get("type_object_data", {})
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        objects_data = self.get_node(node_id).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_connection_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        object_data = self.get_connection(connection_id).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_connection_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        type_object_data = self.get_connection(connection_id).get(
            "type_object_data", {}
        )
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        objects_data = self.get_connection(connection_id).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_node_parameters_by_node(self, node) -> dict:
        object_parameters = self.get_node(node.get("node_id", "0")).get(
            "object_parameters", {}
        )
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_node_parameters_by_node(self, node) -> dict:
        type_object_parameters = self.get_node(node.get("node_id", "0")).get(
            "type_object_parameters", {}
        )
        return dict(
            sorted(type_object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_parameters_by_node(self, node) -> dict:
        objects_parameters = self.get_node(node.get("node_id", "0")).get(
            "objects_parameters", {}
        )
        return dict(
            sorted(objects_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_connection_parameters_by_connection(self, connection) -> dict:
        object_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("object_parameters", {})
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_connection_parameters_by_connection(self, connection) -> dict:
        type_object_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("type_object_parameters", {})
        return dict(
            sorted(type_object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_parameters_by_connection(self, connection) -> dict:
        objects_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("objects_parameters", {})
        return dict(
            sorted(objects_parameters.items(), key=lambda x: x[1].get("order", 0))
        )
