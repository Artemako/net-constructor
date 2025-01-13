import json
import uuid

import package.constants as constants


class Project:
    def __init__(self) -> None:
        self.__file_name = None
        self.__data = None

    def get_data(self):
        return self.__data

    def create_new_project(self, diagram_data, image_parameters, file_path):
        self.__file_name = file_path
        self.__data = {
            "diagram_type_id": diagram_data.get("type_id", "0"),
            "diagram_name": diagram_data.get("name", ""),
            "diagram_parameters": diagram_data.get("parameters", {}),
            "image_parameters": image_parameters,
            "nodes": [],
            "connections": [],
        }
        #
        self._write_project()

    def is_active(self):
        return self.__file_name

    def open_project(self, file_path):
        self.__file_name = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.__data = json.load(f)

    def _write_project(self):
        if self.__file_name:
            with open(self.__file_name, "w", encoding="utf-8") as f:
                json.dump(self.__data, f, indent=4, ensure_ascii=False)

    def change_type_diagram(self, new_diagram, config_nodes, config_connections):
        old_diagram_type_id = self.__data["diagram_type_id"]
        new_diagram_type_id = new_diagram.get("type_id", "0")
        #
        self._update_diagram_nodes(
            old_diagram_type_id, new_diagram_type_id, config_nodes
        )
        self._update_diagram_connections(
            old_diagram_type_id, new_diagram_type_id, config_connections
        )
        #
        self.__data["diagram_type_id"] = new_diagram_type_id
        self.__data["diagram_name"] = new_diagram.get("name", "")
        self.__data["diagram_parameters"] = new_diagram.get("parameters", {})
        # data точно не трогаем
        self._write_project()

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
        self._write_project()

    # def _update_diagram_nodes(self, old_diagram_type_id, new_diagram_type_id):
    #     dtd = constants.DiagramToDiagram()
    #     for item in self.__data["nodes"]:
    #         old_node_id = item.get("node_id", "0")
    #         new_node_id = dtd.get_new_type_id(old_diagram_type_id, new_diagram_type_id, old_node_id, is_node=True)
    #         item["node_id"] = new_node_id

    # def _update_diagram_connections(self, old_diagram_type_id, new_diagram_type_id):
    #     dtd = constants.DiagramToDiagram()
    #     for item in self.__data["connections"]:
    #         # old_connection_id = item.get("connection_id", "0")
    #         # new_connection_id = dtd.get_new_type_id(old_diagram_type_id, new_diagram_type_id, old_connection_id, is_node=False)
    #         # item["connection_id"] = new_connection_id

    # TODO
    def _update_diagram_nodes(
        self, old_diagram_type_id, new_diagram_type_id, config_nodes
    ):
        dtd = constants.DiagramToDiagram()
        for node in self.__data.get("nodes", []):
            old_node_id = node.get("node_id")
            new_node_id = dtd.get_new_type_id(
                new_diagram_type_id,
                old_node_id,
                is_node=True,
            )
            node["node_id"] = new_node_id if new_node_id else old_node_id
            node["parameters"] = self._get_combined_parameters(
                config_nodes.get(new_node_id, {})
            )

    def _update_diagram_connections(
        self, old_diagram_type_id, new_diagram_type_id, config_connections
    ):
        dtd = constants.DiagramToDiagram()
        for connection in self.__data.get("connections", []):
            old_connection_id = connection.get("connection_id")
            new_connection_id = dtd.get_new_type_id(
                new_diagram_type_id,
                old_connection_id,
                is_node=False,
            )
            connection["connection_id"] = new_connection_id if new_connection_id else old_connection_id
            connection["parameters"] = self._get_combined_parameters(
                config_connections.get(new_connection_id, {})
            )

    def _get_combined_data(self, object_dict):
        return {
            **object_dict.get("object_data", {}),
            **object_dict.get("type_object_data", {}),
            **object_dict.get("objects_data", {}),
        }

    def _get_combined_parameters(self, object_dict):
        return {
            **object_dict.get("object_parameters", {}),
            **object_dict.get("type_object_parameters", {}),
            **object_dict.get("objects_parameters", {}),
        }

    def _add_node(self, key_dict_node):
        node_key = key_dict_node.get("node_key")
        node_dict = key_dict_node.get("node_dict")
        #
        new_id = uuid.uuid4().hex
        new_order = len(self.__data.get("nodes", []))
        #
        new_data = self._get_combined_data(node_dict)
        new_parameters = self._get_combined_parameters(node_dict)
        #
        new_is_wrap = node_dict.get("is_wrap", False)
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
        new_order = len(self.__data.get("connections", []))
        #
        new_data = self._get_combined_data(connection_dict)
        new_parameters = self._get_combined_parameters(connection_dict)
        #
        new_dict = {
            "id": new_id,
            "order": new_order,
            "connection_id": connection_key,
            "data": new_data,
            "parameters": new_parameters,
        }
        self.__data["connections"].append(new_dict)

    # def _add_node(self, key_dict_node):
    #     node_key = key_dict_node.get("node_key")
    #     node_dict = key_dict_node.get("node_dict")
    #     #
    #     new_id = uuid.uuid4().hex
    #     #
    #     new_order = len(self.__data.get("nodes", []))
    #     #
    #     new_data = {
    #         **node_dict.get("object_data", {}),
    #         **node_dict.get("type_object_data", {}),
    #         **node_dict.get("objects_data", {}),
    #     }
    #     #
    #     new_is_wrap = node_dict.get("is_wrap", False)
    #     #
    #     new_parameters = {
    #         **node_dict.get("object_parameters", {}),
    #         **node_dict.get("type_object_parameters", {}),
    #         **node_dict.get("objects_parameters", {}),
    #     }
    #     #
    #     new_dict = {
    #         "id": new_id,
    #         "order": new_order,
    #         "node_id": node_key,
    #         "data": new_data,
    #         "is_wrap": new_is_wrap,
    #         "parameters": new_parameters,
    #     }
    #     self.__data["nodes"].append(new_dict)
    #
    # def _add_connection(self, key_dict_connection):
    #     connection_key = key_dict_connection.get("connection_key")
    #     connection_dict = key_dict_connection.get("connection_dict")
    #     #
    #     new_id = uuid.uuid4().hex
    #     #
    #     new_order = len(self.__data.get("connections", []))
    #     #
    #     new_data = {
    #         **connection_dict.get("object_data", {}),
    #         **connection_dict.get("type_object_data", {}),
    #         **connection_dict.get("objects_data", {}),
    #     }
    #     #
    #     new_parameters = {
    #         **connection_dict.get("object_parameters", {}),
    #         **connection_dict.get("type_object_parameters", {}),
    #         **connection_dict.get("objects_parameters", {}),
    #     }
    #     #
    #     new_dict = {
    #         "id": new_id,
    #         "order": new_order,
    #         "connection_id": connection_key,
    #         "data": new_data,
    #         "parameters": new_parameters,
    #     }
    #     self.__data["connections"].append(new_dict)

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
        self._write_project()

    def wrap_node(self, node):
        _id = node.get("id", "")
        for node in self.__data["nodes"]:
            if node["id"] == _id:
                node["is_wrap"] = not node.get("is_wrap", True)
                break
        self._write_project()

    def save_project(
        self,
        obj,
        is_node,
        is_general_tab,
        is_editor_tab,
        config_nodes,
        config_connections,
        diagram_type_id,
        diagram_name,
        new_image_parameters,
        new_diagram_parameters,
        new_data,
        new_parameters,
    ):
        # Проверка на вкладку
        if is_general_tab:
            self.__data["diagram_type_id"] = diagram_type_id
            self.__data["diagram_name"] = diagram_name
            #
            for key, value in new_diagram_parameters.items():
                self.__data["diagram_parameters"][key] = value
            for key, value in new_image_parameters.items():
                self.__data["image_parameters"][key] = value
        elif is_editor_tab:
            if is_node:
                _id = obj.get("id", "")
                for node in self.__data.get("nodes", []):
                    if node["id"] == _id:
                        for key, value in new_data.items():
                            self._check_empty_data_key(node, key)
                            node["data"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=False,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=False,
                            )
                        for key, value in new_parameters.items():
                            self._check_empty_parameters_key(node, key)
                            node["parameters"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=True,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=True,
                            )
                        break
            else:
                _id = obj.get("id", "")
                for connection in self.__data.get("connections", []):
                    if connection["id"] == _id:
                        for key, value in new_data.items():
                            self._check_empty_data_key(connection, key)
                            connection["data"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=False,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=False,
                            )
                        for key, value in new_parameters.items():
                            self._check_empty_parameters_key(connection, key)
                            connection["parameters"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=True,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=True,
                            )
                        break
        self._write_project()

    def _check_empty_parameters_key(self, object, key):
        if key not in object["parameters"]:
            object["parameters"][key] = {}

    def _check_empty_data_key(self, object, key):
        if key not in object["data"]:
            object["data"][key] = {}

    def _check_type_object_key(
        self,
        config_nodes,
        config_connections,
        obj,
        key,
        is_node=False,
        is_parameter=True,
    ):
        obj_id = obj.get("node_id" if is_node else "connection_id", "")
        #
        config_dict = config_nodes if is_node else config_connections
        obj_dict = config_dict.get(obj_id, {})
        #
        type_object_key = (
            "type_object_parameters" if is_parameter else "type_object_data"
        )
        is_type_object = obj_dict.get(type_object_key, {}).get(key, {})
        if is_type_object:
            target_section = "parameters" if is_parameter else "data"
            value = obj[target_section].get(key, {}).get("value", None)
            if value is not None:
                data_section = "nodes" if is_node else "connections"
                for other_obj in self.__data.get(data_section, []):
                    if (
                        other_obj.get("node_id" if is_node else "connection_id", "")
                        == obj_id
                    ):
                        other_obj[target_section][key] = {"value": value}

    def _check_objects_key(
        self,
        config_nodes,
        config_connections,
        obj,
        key,
        is_node=False,
        is_parameter=True,
    ):
        print("_check_objects_key")
        obj_id = obj.get("node_id" if is_node else "connection_id", "")
        #
        config_dict = config_nodes if is_node else config_connections
        obj_dict = config_dict.get(obj_id, {})
        #
        objects_key = "objects_parameters" if is_parameter else "objects_data"
        is_objects = obj_dict.get(objects_key, {}).get(key, {})
        if is_objects:
            target_section = "parameters" if is_parameter else "data"
            value = obj[target_section].get(key, {}).get("value", None)
            if value is not None:
                data_section = "nodes" if is_node else "connections"
                print("data_section", data_section)
                print("key", key, "value", value)
                for other_obj in self.__data.get(data_section, []):
                    other_obj[target_section][key] = {"value": value}
