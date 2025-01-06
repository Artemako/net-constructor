import json
import uuid


class Project:
    def __init__(self) -> None:
        self.__file_name = None
        self.__data = None

    def get_data(self):
        return self.__data

    def create_new_project(self, diagramm_data, image_parameters, file_path):
        self.__file_name = file_path
        self.__data = {
            "diagramm_type_id": diagramm_data.get("type_id", "0"),
            "diagramm_name": diagramm_data.get("name", ""),
            "diagramm_parameters": diagramm_data.get("parameters", {}),
            "image_parameters": image_parameters,
            "nodes": [],
            "connections": [],
        }
        #
        self.write_project()

    def is_active(self):
        return self.__file_name

    def open_project(self, file_path):
        self.__file_name = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.__data = json.load(f)

    def write_project(self):
        if self.__file_name:
            with open(self.__file_name, "w", encoding="utf-8") as f:
                json.dump(self.__data, f, indent=4, ensure_ascii=False)

    def change_type_diagramm(self, new_diagramm):
        self.__data["diagramm_type_id"] = new_diagramm.get("type_id", "0")
        self.__data["diagramm_name"] = new_diagramm.get("name", "")
        # TODO Подумать что делать с параметрами
        # self.__data["diagramm_parameters"] = new_diagramm.get("parameters", {})
        self.write_project()

    def set_new_order_nodes(self, new_order_nodes):
        print("set_new_order_nodes():\n" f"new_order_nodes={new_order_nodes}\n")
        nodes = []
        for index, node in enumerate(new_order_nodes):
            node["order"] = index
            nodes.append(node)
        # Это рискованно но ладно
        self.__data["nodes"] = new_order_nodes

    def set_new_order_connections(self, new_order_connections):
        print(
            "set_new_order_connections():\n"
            f"new_order_connections={new_order_connections}\n"
        )
        connections = []
        for index, connection in enumerate(new_order_connections):
            connection["order"] = index
            connections.append(connection)
        # Это рискованно но ладно
        self.__data["connections"] = new_order_connections

    def add_pair(self, key_dict_node_and_key_dict_connection):
        key_dict_node = key_dict_node_and_key_dict_connection.get("node")
        key_dict_connection = key_dict_node_and_key_dict_connection.get("connection")
        #
        if len(self.__data.get("nodes", [])) == 0:
            self._add_node(key_dict_node)
        else:
            self._add_node(key_dict_node)
            self._add_connection(key_dict_connection)
        self.write_project()

    def _add_node(self, key_dict_node):
        node_key = key_dict_node.get("node_key")
        node_dict = key_dict_node.get("node_dict")
        #
        new_id = uuid.uuid4().hex
        #
        new_order = len(self.__data.get("nodes", []))
        # TODO
        new_data = {**node_dict.get("object_data", {}), **node_dict.get("type_object_data", {})}
        #
        new_is_wrap = node_dict.get("is_wrap", False)
        # TODO 
        new_parameters = {**node_dict.get("object_parameters", {}), **node_dict.get("type_object_parameters", {})}
        #
        new_dict = {
            "id": new_id,
            "order": new_order,
            "node_id": node_key,
            "data": new_data,
            "is_wrap": new_is_wrap,
            "parameters": new_parameters,
        }
        self.__data["nodes"].append(new_dict)

    def _add_connection(self, key_dict_connection):
        connection_key = key_dict_connection.get("connection_key")
        connection_dict = key_dict_connection.get("connection_dict")
        #
        new_id = uuid.uuid4().hex
        #
        new_order = len(self.__data.get("connections", []))
        # TODO
        new_data = {**connection_dict.get("object_data", {}), **connection_dict.get("type_object_data", {})}
        # TODO
        new_parameters = {**connection_dict.get("object_parameters", {}), **connection_dict.get("type_object_parameters", {})}
        #
        new_dict = {
            "id": new_id,
            "order": new_order,
            "connection_id": connection_key,
            "data": new_data,
            "parameters": new_parameters,
        }
        self.__data["connections"].append(new_dict)

    def delete_pair(self, node, connection):
        if node:
            delete_id = node.get("id", "")
            if delete_id:
                self.__data["nodes"] = list(
                    filter(lambda x: x.get("id", "") != delete_id, self.__data["nodes"])
                )
                sorted_nodes = sorted(
                    self.__data["nodes"], key=lambda x: x.get("order", 0)
                )
                self.__data["nodes"] = []
                for index, node in enumerate(sorted_nodes):
                    node["order"] = index
                    self.__data["nodes"].append(node)
        if connection:
            delete_id = connection.get("id", "")
            if delete_id:
                self.__data["connections"] = list(
                    filter(
                        lambda x: x.get("id", "") != delete_id,
                        self.__data["connections"],
                    )
                )
                sorted_connections = sorted(
                    self.__data["connections"], key=lambda x: x.get("order", 0)
                )
                self.__data["connections"] = []
                for index, connection in enumerate(sorted_connections):
                    connection["order"] = index
                    self.__data["connections"].append(connection)
        self.write_project()

    def wrap_node(self, node):
        _id = node.get("id", "")
        for node in self.__data["nodes"]:
            if node["id"] == _id:
                node["is_wrap"] = not node.get("is_wrap", True)
                break
        self.write_project()

    def save_project(
        self,
        obj,
        is_node,
        is_general_tab,
        is_editor_tab,
        config_nodes,
        config_connections,
        diagramm_type_id,
        diagramm_name,
        new_image_parameters,
        new_diagramm_parameters,
        new_data,
        new_parameters,
    ):
        # Проверка на вкладку
        if is_general_tab:
            self.__data["diagramm_type_id"] = diagramm_type_id
            self.__data["diagramm_name"] = diagramm_name
            #
            for key, value in new_diagramm_parameters.items():
                self.__data["diagramm_parameters"][key] = value
            for key, value in new_image_parameters.items():
                self.__data["image_parameters"][key] = value
        elif is_editor_tab:
            if is_node:
                _id = obj.get("id", "")
                for node in self.__data["nodes"]:
                    if node["id"] == _id:
                        for key, value in new_data.items():
                            node["data"][key] = value
                        for key, value in new_parameters.items():
                            self._check_empty_parameters_key(node, key, is_node=True)
                            node["parameters"][key] = value
                            self._check_global_parameters_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                            )
                        break
            else:
                _id = obj.get("id", "")
                for connection in self.__data["connections"]:
                    if connection["id"] == _id:
                        for key, value in new_data.items():
                            connection["data"][key] = value
                        for key, value in new_parameters.items():
                            self._check_empty_parameters_key(
                                connection, key, is_node=False
                            )
                            connection["parameters"][key] = value
                            self._check_global_parameters_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                            )
                        break
        self.write_project()

    def _check_empty_parameters_key(self, object, key, is_node=False):
        if is_node:
            if key not in object["parameters"]:
                object["parameters"][key] = {}
        else:
            if key not in object["parameters"]:
                object["parameters"][key] = {}

    def _check_global_parameters_key(
        self, config_nodes, config_connections, object, key, is_node=False
    ):
        if is_node:
            node_id = object.get("node_id", "")
            node_dict = config_nodes.get(node_id, {})
            is_global = (
                node_dict.get("parameters", {}).get(key, {}).get("is_global", False)
            )

            if is_global:
                value = object["parameters"].get(key, {}).get("value", None)
                if value is not None:
                    for other_node in self.__data.get("nodes", []):
                        if other_node.get("node_id", "") == node_id:
                            other_node["parameters"][key] = {"value": value}
        else:
            connection_id = object.get("connection_id", "")
            connection_dict = config_connections.get(connection_id, {})
            is_global = (
                connection_dict.get("parameters", {})
                .get(key, {})
                .get("is_global", False)
            )

            if is_global:
                value = object["parameters"].get(key, {}).get("value", None)
                if value is not None:
                    for other_connection in self.__data.get("connections", []):
                        if other_connection.get("connection_id", "") == connection_id:
                            other_connection["parameters"][key] = {"value": value}
