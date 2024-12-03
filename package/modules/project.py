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
            "image_settings": {"width": 2000, "height": 600},
            "nodes": [],
            "connections": [],
        }
        #
        self.write_project()


    def is_active(self):
        return self.__file_name

    def open_project(self, file_path):
        self.__file_name = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.__data = json.load(f)

    def write_project(self):    
        if self.__file_name:
            with open(self.__file_name, 'w', encoding='utf-8') as f:
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
        new_order = len(self.__data.get("connections", [])) - 1
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