import json
import uuid

class Project:
    def __init__(self) -> None:
        self.__file_name = None
        self.__data = None

    def get_data(self):
        return self.__data

    def create_new_project(self, file_path):
        self.__file_name = file_path
        self.__data = {
            "diagramm_settings": {
                "diagramm_type_id": 0,
                "diagramm_name": "Скелетная схема ВОЛП и основные данные цепей кабеля",
            },
            "image_settings": {"width": 2000, "height": 600, "start_x": 150, "start_y": 150},
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

    def add_pair(self, key_dict_node_and_key_dict_connection):
        key_dict_node = key_dict_node_and_key_dict_connection.get("node")
        key_dict_connection = key_dict_node_and_key_dict_connection.get("connection")
        #
        if len(self.__data.get("nodes", [])) == 0:
            self.add_node(key_dict_node)
        else:
            self.add_node(key_dict_node)
            self.add_connection(key_dict_connection)
        self.write_project()

    def add_node(self, key_dict_node):
        node_key = key_dict_node.get("node_key")
        node_dict = key_dict_node.get("node_dict")
        #
        new_id = uuid.uuid4().hex
        #
        new_order = len(self.__data.get("nodes", []))
        #
        new_data = node_dict.get("data", {})
        #
        new_is_wrap = node_dict.get("is_wrap", False)
        #
        new_metrics = {}
        #
        new_dict = {
            "id": new_id,
            "order": new_order,
            "node_id": node_key,
            "data": new_data,
            "is_wrap": new_is_wrap,
            "metrics": new_metrics,
        }
        self.__data["nodes"].append(new_dict)

    def add_connection(self, key_dict_connection):
        connection_key = key_dict_connection.get("connection_key")
        connection_dict = key_dict_connection.get("connection_dict")
        #
        new_id = uuid.uuid4().hex
        #
        new_order = len(self.__data.get("connections", []))
        #
        new_data = connection_dict.get("data", {})
        #
        new_metrics = {}
        #
        new_dict = {
            "id": new_id,
            "order": new_order,
            "connection_id": connection_key,
            "data": new_data,
            "metrics": new_metrics,
        }
        self.__data["connections"].append(new_dict)

    def delete_pair(self, node, connection):
        if node:
            delete_id = node.get("id", "")
            if delete_id:
                self.__data["nodes"] = list(filter(lambda x: x.get("id", "") != delete_id, self.__data["nodes"]))
                sorted_nodes = sorted(self.__data["nodes"], key=lambda x: x.get("order", 0))
                self.__data["nodes"] = []
                for index, node in enumerate(sorted_nodes):
                    node["order"] = index
                    self.__data["nodes"].append(node)
        if connection:
            delete_id = connection.get("id", "")
            if delete_id:
                self.__data["connections"] = list(filter(lambda x: x.get("id", "") != delete_id, self.__data["connections"]))
                sorted_connections = sorted(self.__data["connections"], key=lambda x: x.get("order", 0))
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

    def change_name_node(self, node, name):
        _id = node.get("id", "")
        for node in self.__data["nodes"]:
            if node["id"] == _id:
                node["data"]["название"]["value"] = name
                break

    def change_name_connection(self, connection, name):
        _id = connection.get("id", "")
        for connection in self.__data["connections"]:
            if connection["id"] == _id:
                connection["data"]["название"]["value"] = name
                break


    def save_project(self, object, is_node, is_edit, config_nodes, config_connections, new_diagramm_settings, new_image_settings, new_data, new_metrics):
        print(f"new_diagramm_settings = {new_diagramm_settings},\nnew_image_settings = {new_image_settings},\nnew_data = {new_data},\nnew_metrics = {new_metrics}")
        for key, value in new_diagramm_settings.items():
            self.__data["diagramm_settings"][key] = value
        for key, value in new_image_settings.items():
            self.__data["image_settings"][key] = value
        if is_edit:
            if is_node:
                _id = object.get("id", "")
                for node in self.__data["nodes"]:
                    if node["id"] == _id:
                        for key, value in new_data.items():
                            node["data"][key] = value
                        for key, value in new_metrics.items():
                            self.check_empty_metrics_key(node, key, is_node = True)
                            node["metrics"][key] = value
                            self.check_global_metrics_key(config_nodes, config_connections, object, key, is_node = True)
                        break
            else:
                _id = object.get("id", "")
                for connection in self.__data["connections"]:
                    if connection["id"] == _id:
                        for key, value in new_data.items():
                            connection["data"][key] = value
                        for key, value in new_metrics.items():
                            self.check_empty_metrics_key(connection, key, is_node = False)
                            connection["metrics"][key] = value
                            self.check_global_metrics_key(config_nodes, config_connections, object, key, is_node = False)
                        break
        self.write_project()


    def check_empty_metrics_key(self, object, key, is_node = False):
        if is_node:
            if key not in object["metrics"]:
                object["metrics"][key] = {}
        else:
            if key not in object["metrics"]:
                object["metrics"][key] = {}


    def check_global_metrics_key(self, config_nodes, config_connections, object, key, is_node=False):
        if is_node:
            node_id = object.get("node_id", "0")
            node_dict = config_nodes.get(node_id, {})
            is_global = node_dict.get("metrics", {}).get(key, {}).get("is_global", False)
            
            if is_global:
                value = object["metrics"].get(key, {}).get("value", None)
                if value is not None:
                    for other_node in self.__data.get("nodes", []):
                        if other_node.get("node_id", "0") == node_id:
                            other_node["metrics"][key] = {"value": value}
        else:
            connection_id = object.get("connection_id", "0")
            connection_dict = config_connections.get(connection_id, {})
            is_global = connection_dict.get("metrics", {}).get(key, {}).get("is_global", False)
            
            if is_global:
                value = object["metrics"].get(key, {}).get("value", None)
                if value is not None:
                    for other_connection in self.__data.get("connections", []):
                        if other_connection.get("connection_id", "0") == connection_id:
                            other_connection["metrics"][key] = {"value": value}
