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
    
    def get_nodes(self):
        return self.__nodes
    
    def get_connections(self):
        return self.__connections
    
    def get_config_diagramms(self):
        diagramms = self.__global.get("diagramms", {})
        return dict(sorted(diagramms.items(), key=lambda x: x[1].get("order", 0)))
    
    def get_config_image_parameters(self):
        image_parameters = self.__global.get("image_parameters", {})
        return dict(sorted(image_parameters.items(), key=lambda x: x[1].get("order", 0)))
    
    def get_config_diagramm_parameters_by_type_id(self, diagramm_type_id):  
        diagramms = self.__global.get("diagramms", {})
        parameters = diagramms.get(str(diagramm_type_id), {}).get("parameters", {})
        return dict(sorted(parameters.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_node_data_by_node(self, node):
        node_id = node.get("node_id", "0")
        data = self.__nodes.get(node_id, {}).get("data", {})
        sorted_data = dict(sorted(data.items(), key=lambda x: x[1].get("order", 0)))
        return sorted_data
    
    def get_config_connection_data_by_connection(self, connection):
        connection_id = connection.get("connection_id", "0")
        data = self.__connections.get(connection_id, {}).get("data", {})
        sorted_data = dict(sorted(data.items(), key=lambda x: x[1].get("order", 0)))
        return sorted_data

    def get_config_node_parameters_by_node(self, node):
        parameters = self.__nodes.get(node.get("node_id", "0"), {}).get("parameters", {})
        sorted_parameters = dict(sorted(parameters.items(), key=lambda x: x[1].get("order", 0)))
        return sorted_parameters
    
    def get_config_connection_parameters_by_connection(self, connection):
        parameters = self.__connections.get(connection.get("connection_id", "0"), {}).get("parameters", {})
        sorted_parameters = dict(sorted(parameters.items(), key=lambda x: x[1].get("order", 0)))
        return sorted_parameters
