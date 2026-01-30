"""Загрузка и доступ к конфигурациям из configs/*.json (глобальные, узлы, соединения, списки)."""

import json
import os


class Configs:
    """Единая точка доступа к конфигам: global, nodes, connections, lists."""

    def __init__(self) -> None:
        self.__global: dict = {}
        self.__nodes: dict = {}
        self.__connections: dict = {}
        self.__lists: dict = {}

    def load_configs(self, dir_app: str) -> None:
        """Загружает все конфигурации из каталога configs приложения."""
        config_dir = os.path.join(dir_app, "configs")
        with open(os.path.join(config_dir, "config_global.json"), encoding="utf-8") as f:
            self.__global = json.load(f)
        with open(os.path.join(config_dir, "config_nodes.json"), encoding="utf-8") as f:
            self.__nodes = json.load(f)
        with open(os.path.join(config_dir, "config_connections.json"), encoding="utf-8") as f:
            self.__connections = json.load(f)
        try:
            with open(os.path.join(config_dir, "config_lists.json"), encoding="utf-8") as f:
                self.__lists = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__lists = {"lists": {}}

    def save_lists(self, dir_app: str) -> None:
        """Сохраняет все списки в configs/config_lists.json."""
        path = os.path.join(dir_app, "configs", "config_lists.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.__lists, f, ensure_ascii=False, indent=4)

    def get_list_by_type(self, list_type: str) -> list:
        """Возвращает список значений по типу"""
        lists = self.__lists.get("lists", {})
        list_config = lists.get(list_type, {})
        items = list_config.get("items", [])
        return [item.get("value", "") for item in items]

    def get_list_config_by_type(self, list_type: str) -> dict:
        """Возвращает полную конфигурацию списка по типу"""
        lists = self.__lists.get("lists", {})
        return lists.get(list_type, {})

    def update_list_by_type(self, list_type: str, items: list):
        """Обновляет список по типу"""
        if "lists" not in self.__lists:
            self.__lists["lists"] = {}
        
        # Преобразуем простой список в структуру с дополнительными параметрами
        structured_items = []
        for item in items:
            if isinstance(item, dict):
                structured_items.append(item)
            else:
                structured_items.append({
                    "value": str(item),
                    "name": str(item),
                    "description": "",
                    "is_default": False
                })
        
        self.__lists["lists"][list_type] = {
            "name": list_type,
            "description": "",
            "type": list_type,
            "items": structured_items
        }

    # Методы для обратной совместимости
    def get_cable_list(self) -> list:
        """Возвращает список кабелей (для обратной совместимости)"""
        return self.get_list_by_type("cable_types")

    def update_cable_list(self, cables: list):
        """Обновляет список кабелей (для обратной совместимости)"""
        self.update_list_by_type("cable_types", cables)

    def get_sector_names_list(self) -> list:
        """Возвращает список названий секторов (для обратной совместимости)"""
        return self.get_list_by_type("sector_names")

    def update_sector_names_list(self, sector_names: list):
        """Обновляет список названий секторов (для обратной совместимости)"""
        self.update_list_by_type("sector_names", sector_names)

    def save_cable_lists(self, dir_app):
        """Сохраняет списки кабелей в файл (для обратной совместимости)"""
        self.save_lists(dir_app)

    def save_sector_names(self, dir_app):
        """Сохраняет список названий секторов в файл (для обратной совместимости)"""
        self.save_lists(dir_app)

    def get_node(self, node_id: str) -> dict:
        """Возвращает конфигурацию узла по идентификатору."""
        return self.__nodes.get(node_id, {})

    def get_connection(self, connection_id: str) -> dict:
        """Возвращает конфигурацию соединения по идентификатору."""
        return self.__connections.get(connection_id, {})

    def get_nodes(self) -> dict:
        """Возвращает словарь конфигураций всех узлов."""
        return self.__nodes

    def get_connections(self) -> dict:
        """Возвращает словарь конфигураций всех соединений."""
        return self.__connections

    def get_config_diagrams(self) -> dict:
        """Возвращает конфигурацию типов диаграмм, отсортированную по порядку."""
        diagrams = self.__global.get("diagrams", {})
        return dict(sorted(diagrams.items(), key=lambda x: x[1].get("order", 0)))


    def get_config_control_sectors(self) -> dict:
        """Возвращает конфигурацию контрольных секторов, отсортированную по порядку."""
        control_sectors_config = self.__global.get("control_sectors_config", {})
        return dict(
            sorted(control_sectors_config.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_diagram_parameters_by_type_id(self, diagram_type_id) -> dict:
        """Возвращает параметры диаграммы по идентификатору типа."""
        diagrams = self.__global.get("diagrams", {})
        parameters = diagrams.get(str(diagram_type_id), {}).get("parameters", {})
        return dict(sorted(parameters.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_diagram_nodes_by_type_id(self, diagram_type_id) -> dict:
        """Возвращает конфигурации узлов диаграммы по идентификатору типа."""
        diagrams = self.__global.get("diagrams", {})
        id_nodes = diagrams.get(str(diagram_type_id), {}).get("id_nodes", [])
        config_diagram_nodes = {
            node_type_id: self.get_node(node_type_id) for node_type_id in id_nodes
        }
        return config_diagram_nodes

    def get_config_diagram_connections_by_type_id(self, diagram_type_id) -> dict:
        """Возвращает конфигурации соединений диаграммы по идентификатору типа."""
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
        """Возвращает данные объекта узла из конфига по экземпляру узла."""
        node_id = node.get("node_id", "0")
        object_data = self.get_node(node_id).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_node_data_by_node(self, node) -> dict:
        """Возвращает типовые данные узла из конфига по экземпляру узла."""
        node_id = node.get("node_id", "0")
        type_object_data = self.get_node(node_id).get("type_object_data", {})
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_node(self, node) -> dict:
        """Возвращает данные объектов узла из конфига по экземпляру узла."""
        node_id = node.get("node_id", "0")
        objects_data = self.get_node(node_id).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_connection_data_by_connection(self, connection) -> dict:
        """Возвращает данные объекта соединения из конфига по экземпляру соединения."""
        connection_id = connection.get("connection_id", "0")
        object_data = self.get_connection(connection_id).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_connection_data_by_connection(self, connection) -> dict:
        """Возвращает типовые данные соединения из конфига по экземпляру соединения."""
        connection_id = connection.get("connection_id", "0")
        type_object_data = self.get_connection(connection_id).get(
            "type_object_data", {}
        )
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_connection(self, connection) -> dict:
        """Возвращает данные объектов соединения из конфига по экземпляру соединения."""
        connection_id = connection.get("connection_id", "0")
        objects_data = self.get_connection(connection_id).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_node_parameters_by_node(self, node) -> dict:
        """Возвращает параметры объекта узла из конфига по экземпляру узла."""
        object_parameters = self.get_node(node.get("node_id", "0")).get(
            "object_parameters", {}
        )
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_node_parameters_by_node(self, node) -> dict:
        """Возвращает типовые параметры узла из конфига по экземпляру узла."""
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
        """Возвращает параметры объекта соединения из конфига по экземпляру соединения."""
        object_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("object_parameters", {})
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_connection_parameters_by_connection(self, connection) -> dict:
        """Возвращает типовые параметры соединения из конфига по экземпляру соединения."""
        type_object_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("type_object_parameters", {})
        return dict(
            sorted(type_object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_parameters_by_connection(self, connection) -> dict:
        """Возвращает параметры объектов соединения из конфига по экземпляру соединения."""
        objects_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("objects_parameters", {})
        return dict(
            sorted(objects_parameters.items(), key=lambda x: x[1].get("order", 0))
        )
