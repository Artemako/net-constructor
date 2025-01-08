import json


class Configs:
    def __init__(self):
        self.__global = {}
        self.__nodes = {}
        self.__connections = {}

    def load_configs(self, dir_app):
        #
        with open(dir_app + "/configs/config_global.json", "r", encoding="utf-8") as f:
            self.__global = json.load(f)
        #
        with open(dir_app + "/configs/config_nodes.json", "r", encoding="utf-8") as f:
            self.__nodes = json.load(f)
        #
        with open(
            dir_app + "/configs/config_connections.json", "r", encoding="utf-8"
        ) as f:
            self.__connections = json.load(f)

    def get_nodes(self) -> dict:
        return self.__nodes

    def get_connections(self) -> dict:
        return self.__connections

    def get_config_diagramms(self) -> dict:
        diagramms = self.__global.get("diagramms", {})
        return dict(sorted(diagramms.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_image_parameters(self) -> dict:
        image_parameters = self.__global.get("image_parameters", {})
        return dict(
            sorted(image_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_diagramm_parameters_by_type_id(self, diagramm_type_id) -> dict:
        diagramms = self.__global.get("diagramms", {})
        parameters = diagramms.get(str(diagramm_type_id), {}).get("parameters", {})
        return dict(sorted(parameters.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_diagramm_nodes_by_type_id(self, diagramm_type_id) -> dict:
        diagramms = self.__global.get("diagramms", {})
        nodes = diagramms.get(str(diagramm_type_id), {}).get("nodes", [])
        #
        config_diagramm_nodes = dict()
        for node_type_id in nodes:
            config_diagramm_nodes[node_type_id] = self.__nodes.get(node_type_id, {})
        return config_diagramm_nodes

    def get_config_diagramm_connections_by_type_id(self, diagramm_type_id) -> dict:
        diagramms = self.__global.get("diagramms", {})
        connections = diagramms.get(str(diagramm_type_id), {}).get("connections", [])
        #
        config_diagramm_connections = dict()
        for connection_type_id in connections:
            config_diagramm_connections[connection_type_id] = self.__connections.get(
                connection_type_id, {}
            )
        return config_diagramm_connections

    # TODO
    def get_config_node_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        object_data = self.__nodes.get(node_id, {}).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_node_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        type_object_data = self.__nodes.get(node_id, {}).get("type_object_data", {})
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        objects_data = self.__nodes.get(node_id, {}).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_connection_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        object_data = self.__connections.get(connection_id, {}).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_connection_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        type_object_data = self.__connections.get(connection_id, {}).get(
            "type_object_data", {}
        )
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        objects_data = self.__connections.get(connection_id, {}).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    # TODO
    def get_config_node_parameters_by_node(self, node) -> dict:
        object_parameters = self.__nodes.get(node.get("node_id", "0"), {}).get(
            "object_parameters", {}
        )
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_node_parameters_by_node(self, node) -> dict:
        type_object_parameters = self.__nodes.get(node.get("node_id", "0"), {}).get(
            "type_object_parameters", {}
        )
        return dict(
            sorted(type_object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_parameters_by_node(self, node) -> dict:
        objects_parameters = self.__nodes.get(node.get("node_id", "0"), {}).get(
            "objects_parameters", {}
        )
        return dict(
            sorted(objects_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_connection_parameters_by_connection(self, connection) -> dict:
        object_parameters = self.__connections.get(
            connection.get("connection_id", "0"), {}
        ).get("object_parameters", {})
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_connection_parameters_by_connection(self, connection) -> dict:
        type_object_parameters = self.__connections.get(
            connection.get("connection_id", "0"), {}
        ).get("type_object_parameters", {})
        return dict(
            sorted(type_object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_parameters_by_connection(self, connection) -> dict:
        objects_parameters = self.__connections.get(
            connection.get("connection_id", "0"), {}
        ).get("objects_parameters", {})
        return dict(
            sorted(objects_parameters.items(), key=lambda x: x[1].get("order", 0))
        )
