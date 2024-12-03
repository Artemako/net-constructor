import json


class Configs:
    def __init__(self):
        self.__nodes = {}
        self.__connections = {}

    def load_configs(self, dir_app):
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
