"""Проект: данные диаграммы, узлы, соединения, файлы NCE."""

import json
import uuid
import copy

import package.constants as constants


class Project:
    """Данные диаграммы: узлы, соединения, сектора, файл NCE, архив параметров по типам."""

    def __init__(self) -> None:
        self.__file_name = None
        self.__data = None
        self.__copied_node_data = None
        self.__copied_connection_data = None
        self.__copied_control_sector_data = None
        self.__configs = None

    def set_configs(self, configs) -> None:
        """Устанавливает ссылку на конфиги для чтения названий по умолчанию из config_global."""
        self.__configs = configs

    def get_data(self):
        return self.__data

    def create_new_project(self, diagram_data, control_sectors_config, file_path):
        self.__file_name = file_path
        self.__data = {
            "diagram_type_id": diagram_data.get("type_id", "0"),
            "diagram_name": diagram_data.get("name", ""),
            "diagram_parameters": diagram_data.get("parameters", {}),
            "control_sectors_config": control_sectors_config,
            "nodes": [],
            "connections": [],
            "archived_parameters": {},
        }
        self._write_project()

    def create_demo_project(self, diagram_data, control_sectors_config):
        """Создаёт пустой демо-проект в памяти без пути к файлу (не сохраняется на диск)."""
        self.__file_name = None
        self.__data = {
            "diagram_type_id": diagram_data.get("type_id", "0"),
            "diagram_name": diagram_data.get("name", ""),
            "diagram_parameters": diagram_data.get("parameters", {}),
            "control_sectors_config": control_sectors_config,
            "nodes": [],
            "connections": [],
            "archived_parameters": {},
        }

    def has_project_data(self):
        """Возвращает True, если загружены данные проекта (для отображения и редактирования)."""
        return self.__data is not None

    def is_active(self):
        return self.__file_name

    def open_project(self, file_path):
        self.__file_name = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.__data = json.load(f)

    def save_as_project(self, file_path):
        self.__file_name = file_path
        self._write_project()

    def _write_project(self):
        if self.__file_name:
            with open(self.__file_name, "w", encoding="utf-8") as f:
                json.dump(self.__data, f, indent=4, ensure_ascii=False)

    def change_type_diagram(self, new_diagram, config_nodes, config_connections):
        """Меняет тип диаграммы: архив параметров по старому типу, обновление узлов/соединений, восстановление из архива."""
        # Сохраняем текущие параметры в архив
        current_type_id = self.__data["diagram_type_id"]

        # Инициализируем архив для текущего типа диаграммы, если его еще нет
        if current_type_id not in self.__data["archived_parameters"]:
            self.__data["archived_parameters"][current_type_id] = {
                "nodes": {},
                "connections": {},
                "diagram_parameters": {},  # Добавляем архив для diagram_parameters
            }

        # Сохраняем параметры узлов
        for node in self.__data["nodes"]:
            node_id = node["id"]
            self.__data["archived_parameters"][current_type_id]["nodes"][node_id] = {
                "parameters": node["parameters"]
            }

        # Сохраняем параметры соединений
        for connection in self.__data["connections"]:
            connection_id = connection["id"]
            self.__data["archived_parameters"][current_type_id]["connections"][
                connection_id
            ] = {"parameters": connection["parameters"]}

        # Сохраняем текущие diagram_parameters в архив
        self.__data["archived_parameters"][current_type_id]["diagram_parameters"] = (
            copy.deepcopy(self.__data["diagram_parameters"])
        )

        # Обновляем тип схемы и параметры
        new_diagram_type_id = new_diagram.get("type_id", "0")
        self._update_diagram_nodes(new_diagram_type_id, config_nodes)
        self._update_diagram_connections(new_diagram_type_id, config_connections)

        # Восстанавливаем параметры из архива, если они есть, иначе выбираем параметры из новой диаграммы
        if new_diagram_type_id in self.__data["archived_parameters"]:
            archived_params = self.__data["archived_parameters"][new_diagram_type_id]

            # Восстанавливаем параметры узлов / соединений
            for node in self.__data["nodes"]:
                node_id = node["id"]
                if node_id in archived_params["nodes"]:
                    node["parameters"] = archived_params["nodes"][node_id]["parameters"]

            for connection in self.__data["connections"]:
                connection_id = connection["id"]
                if connection_id in archived_params["connections"]:
                    connection["parameters"] = archived_params["connections"][
                        connection_id
                    ]["parameters"]

            # Восстанавливаем diagram_parameters из архива
            self.__data["diagram_parameters"] = archived_params.get(
                "diagram_parameters", {}
            )
        else:
            # Если нет архива для нового типа диаграммы, используем параметры из новой диаграммы
            self.__data["diagram_parameters"] = new_diagram.get("parameters", {})

        # Обновляем данные диаграммы
        self.__data["diagram_type_id"] = new_diagram_type_id
        self.__data["diagram_name"] = new_diagram.get("name", "")
        self._write_project()

    def set_new_order_nodes(self, new_order_nodes):
        print(f"set_new_order_nodes():\nnew_order_nodes={new_order_nodes}\n")
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

    def set_new_order_control_sectors(self, obj, new_order_control_sectors):
        # TODO: set_new_order_control_sectors — проверить
        print(
            "set_new_order_control_sectors():\n"
            f"new_order_control_sectors={new_order_control_sectors}\n"
        )
        control_sectors = []
        for index, control_sector in enumerate(new_order_control_sectors):
            control_sector["order"] = index
            control_sectors.append(control_sector)
        connection_id = obj.get("id")
        for connection in self.__data.get("connections", []):
            if connection["id"] == connection_id:
                connection["control_sectors"] = control_sectors
                break
        self._write_project()
        return control_sectors

    def add_pair(self, key_dict_node_and_key_dict_connection):
        """Добавляет пару узел + соединение (сначала узел, потом соединение)."""
        key_dict_node = key_dict_node_and_key_dict_connection.get("node")
        key_dict_connection = key_dict_node_and_key_dict_connection.get("connection")
        if len(self.__data.get("nodes", [])) == 0:
            self._add_node(key_dict_node)
        else:
            self._add_node(key_dict_node)
            self._add_connection(key_dict_connection)
        self._write_project()

    def add_control_sector(
        self, obj, name=None, physical_length=None, length=None, penultimate=False
    ) -> list:
        """Добавляет контрольный сектор с возможностью указания параметров по умолчанию"""
        connection_id = obj.get("id")
        control_sectors_return = []

        for connection in self.__data.get("connections", []):
            if connection["id"] == connection_id:
                new_id = uuid.uuid4().hex
                new_order = len(connection.get("control_sectors", []))
                if penultimate:
                    new_order -= 1
                new_config = copy.deepcopy(
                    self.__data.get("control_sectors_config", {})
                )

                # Устанавливаем значения по умолчанию, если они переданы
                if name is not None:
                    new_config["cs_name"]["value"] = name
                if physical_length is not None:
                    new_config["cs_physical_length"]["value"] = physical_length
                if length is not None:
                    new_config["cs_lenght"]["value"] = length

                new_control_sector = {
                    "id": new_id,
                    "order": new_order,
                    "is_wrap": False,
                    "data_pars": new_config,
                }
                if penultimate:
                    connection["control_sectors"].insert(new_order, new_control_sector)
                else:
                    # Иначе добавляем в конец
                    connection["control_sectors"].append(new_control_sector)

                # Обновляем порядок всех секторов
                for index, cs in enumerate(connection["control_sectors"]):
                    cs["order"] = index

                control_sectors_return = connection.get("control_sectors", [])
                break

        self._write_project()
        return control_sectors_return

    def _update_diagram_nodes(self, new_diagram_type_id, config_nodes):
        """Переводит node_id узлов в новый тип диаграммы по маппингу."""
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

    def _update_diagram_connections(self, new_diagram_type_id, config_connections):
        """Переводит connection_id соединений в новый тип диаграммы по маппингу."""
        dtd = constants.DiagramToDiagram()
        for connection in self.__data.get("connections", []):
            old_connection_id = connection.get("connection_id")
            new_connection_id = dtd.get_new_type_id(
                new_diagram_type_id,
                old_connection_id,
                is_node=False,
            )
            connection["connection_id"] = (
                new_connection_id if new_connection_id else old_connection_id
            )
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

        new_id = uuid.uuid4().hex
        new_order = len(self.__data.get("nodes", []))

        # Получаем данные и параметры по умолчанию из конфигурации
        default_data = self._get_combined_data(node_dict)
        default_parameters = self._get_combined_parameters(node_dict)

        # Для objects_data/objects_parameters берем значения из любого существующего объекта
        if self.__data.get("nodes"):
            first_existing_node = self.__data["nodes"][0]
            self._update_objects_values(
                first_existing_node, node_dict, default_data, default_parameters
            )

        # Для type_object_data/type_object_parameters берем значения из объектов с тем же node_id
        existing_nodes = [
            n for n in self.__data.get("nodes", []) if n["node_id"] == node_key
        ]
        if existing_nodes:
            self._update_type_values(
                existing_nodes[0], node_dict, default_data, default_parameters
            )

        new_is_wrap = node_dict.get("is_wrap", False)

        new_dict = {
            "id": new_id,
            "order": new_order,
            "node_id": node_key,
            "data": default_data,
            "is_wrap": new_is_wrap,
            "parameters": default_parameters,
        }
        self.__data["nodes"].append(new_dict)

    def _add_connection(self, key_dict_connection):
        connection_key = key_dict_connection.get("connection_key")
        connection_dict = key_dict_connection.get("connection_dict")

        new_id = uuid.uuid4().hex
        new_order = len(self.__data.get("connections", []))

        # Получаем данные и параметры по умолчанию из конфигурации
        default_data = self._get_combined_data(connection_dict)
        default_parameters = self._get_combined_parameters(connection_dict)

        # Для objects_data/objects_parameters берем значения из любого существующего объекта
        if self.__data.get("connections"):
            first_existing_connection = self.__data["connections"][0]
            self._update_objects_values(
                first_existing_connection,
                connection_dict,
                default_data,
                default_parameters,
            )

        # Для type_object_data/type_object_parameters берем значения из объектов с тем же connection_id
        existing_connections = [
            c
            for c in self.__data.get("connections", [])
            if c["connection_id"] == connection_key
        ]
        if existing_connections:
            self._update_type_values(
                existing_connections[0],
                connection_dict,
                default_data,
                default_parameters,
            )

        new_dict = {
            "id": new_id,
            "order": new_order,
            "connection_id": connection_key,
            "data": default_data,
            "parameters": default_parameters,
            "control_sectors": [],
        }
        self.__data["connections"].append(new_dict)

        # Добавляем 3 сектора по умолчанию
        self._add_default_control_sectors(new_dict)

        self._write_project()

    def _add_default_control_sectors(self, connection):
        """Добавляет 3 сектора по умолчанию для нового соединения."""
        config = self.__data.get("control_sectors_config", {})

        # Названия тех. запаса и сектора — из config_global (окно «Управление списком названий секторов»)
        if self.__configs is not None:
            tech_name, main_name = self.__configs.get_control_sectors_default_names()
        else:
            tech_name = config.get("cs_tech_name_default", {}).get(
                "value", "Тех. запас"
            )
            main_name = config.get("cs_name", {}).get("value", "Сектор")

        nodes = self.__data.get("nodes", [])
        connection_order = connection.get("order", 0)
        left_node = nodes[connection_order] if connection_order < len(nodes) else None
        right_node = (
            nodes[connection_order + 1] if connection_order + 1 < len(nodes) else None
        )

        tech_length = config.get("cs_tech_lenght_default", {}).get("value", 140)

        # Определяем физическую длину для первого тех. запаса
        if left_node and left_node.get("node_id") in ["1", "51", "101", "151"]:  # Кросс
            tech_phys_length = config.get("cs_tech_cross_lenght_default", {}).get(
                "value", 10
            )
        else:  # Муфта
            tech_phys_length = config.get(
                "cs_tech_mufta_physical_length_default", {}
            ).get("value", 15)

        # Создаем первый тех. запас
        self.add_control_sector(
            connection,
            name=tech_name,
            physical_length=tech_phys_length,
            length=tech_length,
        )

        # Добавляем средний сектор (основной)
        main_length = config.get("cs_lenght", {}).get("value", 200)
        self.add_control_sector(
            connection,
            name=main_name,
            physical_length=0,  # По умолчанию не заполнено
            length=main_length,
        )

        # Добавляем второй тех. запас
        if right_node and right_node.get("node_id") in [
            "1",
            "51",
            "101",
            "151",
        ]:  # Кросс
            tech_phys_length = config.get("cs_tech_cross_lenght_default", {}).get(
                "value", 10
            )
        else:  # Муфта
            tech_phys_length = config.get(
                "cs_tech_mufta_physical_length_default", {}
            ).get("value", 15)

        self.add_control_sector(
            connection,
            name=tech_name,
            physical_length=tech_phys_length,
            length=tech_length,
        )

    def _update_objects_values(
        self, existing_obj, config_dict, default_data, default_parameters
    ):
        """Обновляет objects_data и objects_parameters из любого существующего объекта"""
        # Обновляем objects_data
        objects_data = config_dict.get("objects_data", {})
        for key in objects_data:
            if key in existing_obj["data"]:
                default_data[key] = existing_obj["data"][key]

        # Обновляем objects_parameters
        objects_parameters = config_dict.get("objects_parameters", {})
        for key in objects_parameters:
            if key in existing_obj["parameters"]:
                default_parameters[key] = existing_obj["parameters"][key]

    def _update_type_values(
        self, existing_obj, config_dict, default_data, default_parameters
    ):
        """Обновляет type_object_data и type_object_parameters из объектов с тем же типом"""
        # Обновляем type_object_data
        type_object_data = config_dict.get("type_object_data", {})
        for key in type_object_data:
            if key in existing_obj["data"]:
                default_data[key] = existing_obj["data"][key]

        # Обновляем type_object_parameters
        type_object_parameters = config_dict.get("type_object_parameters", {})
        for key in type_object_parameters:
            if key in existing_obj["parameters"]:
                default_parameters[key] = existing_obj["parameters"][key]

    def restore_pair(self, node_data, connection_data):
        """Восстанавливает пару узел+соединение в конце списков (для отмены удаления / повтора добавления)."""
        if not node_data:
            return
        node_copy = copy.deepcopy(node_data)
        node_copy["order"] = len(self.__data.get("nodes", []))
        self.__data.setdefault("nodes", []).append(node_copy)
        if connection_data:
            conn_copy = copy.deepcopy(connection_data)
            conn_copy["order"] = len(self.__data.get("connections", []))
            self.__data.setdefault("connections", []).append(conn_copy)
        self._write_project()

    def delete_pair(self, node, connection):
        """Удаляет пару узел+соединение из данных и пересчитывает порядок."""
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

    def delete_control_sector(self, obj, selected_cs) -> list:
        connection_id = obj.get("id")
        control_sectors_return = []
        for connection in self.__data.get("connections", []):
            if connection["id"] == connection_id:
                # удаляем кт
                control_sectors = connection.get("control_sectors", [])
                control_sectors = [
                    cs for cs in control_sectors if cs["id"] != selected_cs["id"]
                ]
                # обновляем порядок оставшихся кт
                for index, cs in enumerate(control_sectors):
                    cs["order"] = index
                # обновляем список кт
                connection["control_sectors"] = control_sectors
                control_sectors_return = control_sectors
                break
        self._write_project()
        return control_sectors_return

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
        new_diagram_parameters,
        new_data,
        new_parameters,
    ):
        # Проверка на вкладку
        if is_general_tab:
            self.__data["diagram_type_id"] = diagram_type_id
            self.__data["diagram_name"] = diagram_name
            for key, value in new_diagram_parameters.items():
                self.__data["diagram_parameters"][key] = value
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
        config_dict = config_nodes if is_node else config_connections
        obj_dict = config_dict.get(obj_id, {})
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
        config_dict = config_nodes if is_node else config_connections
        obj_dict = config_dict.get(obj_id, {})
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

    def copy_node_data(self, node):
        """Копирует данные вершины (только data)"""
        self.__copied_node_data = copy.deepcopy(node.get("data", {}))

    def paste_node_data(self, node):
        """Вставляет данные в вершину (только data)"""
        if self.__copied_node_data:
            node["data"] = copy.deepcopy(self.__copied_node_data)
            self._write_project()

    def has_copied_node_data(self):
        """Проверяет, есть ли скопированные данные вершины"""
        return self.__copied_node_data is not None

    def copy_connection_data(self, connection):
        """Копирует данные соединения (только data)"""
        self.__copied_connection_data = copy.deepcopy(connection.get("data", {}))

    def paste_connection_data(self, connection):
        """Вставляет данные в соединение (только data)"""
        if self.__copied_connection_data:
            connection["data"] = copy.deepcopy(self.__copied_connection_data)
            self._write_project()

    def has_copied_connection_data(self):
        """Проверяет, есть ли скопированные данные соединения"""
        return self.__copied_connection_data is not None

    def copy_control_sector_data(self, control_sector):
        """Копирует данные контрольного сектора (только data_pars)"""
        self.__copied_control_sector_data = copy.deepcopy(
            control_sector.get("data_pars", {})
        )

    def paste_control_sector_data(self, control_sector):
        """Вставляет данные в контрольный сектор (только data_pars)"""
        if self.__copied_control_sector_data:
            control_sector["data_pars"] = copy.deepcopy(
                self.__copied_control_sector_data
            )
            self._write_project()

    def has_copied_control_sector_data(self):
        """Проверяет, есть ли скопированные данные контрольного сектора"""
        return self.__copied_control_sector_data is not None
