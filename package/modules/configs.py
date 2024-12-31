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
    
    
    def get_global(self):
        return self.__global

    def get_nodes(self):
        return self.__nodes
    
    def get_connections(self):
        return self.__connections


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

    def get_config_node_metrics_by_node(self, node):
        metrics = self.__nodes.get(node.get("node_id", "0"), {}).get("metrics", {})
        sorted_metrics = dict(sorted(metrics.items(), key=lambda x: x[1].get("order", 0)))
        return sorted_metrics
    
    def get_config_connection_metrics_by_connection(self, connection):
        metrics = self.__connections.get(connection.get("connection_id", "0"), {}).get("metrics", {})
        sorted_metrics = dict(sorted(metrics.items(), key=lambda x: x[1].get("order", 0)))
        return sorted_metrics
