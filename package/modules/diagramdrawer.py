import package.modules.drawnode as drawnode
import package.modules.drawconnection as drawconnection


class Node:
    def __init__(
        self, node=None, config_node=None, before_wrap=False, after_wrap=False
    ):
        self.__type = "node"
        self.__node = node
        self.__config_node = config_node
        self.__before_wrap = before_wrap
        self.__after_wrap = after_wrap

    def get_type(self):
        return self.__type

    def get_node(self):
        return self.__node

    def get_id(self):
        return self.__node.get("id")

    def get_config_node(self):
        return self.__config_node

    def get_parameters(self):
        return self.__node.get("parameters", {})

    def get_config_parameters(self):
        return {
            **self.__config_node.get("object_parameters", {}),
            **self.__config_node.get("type_object_parameters", {}),
            **self.__config_node.get("objects_parameters", {}),
        }

    def get_node_id(self):
        return self.__node.get("node_id")

    def get_data(self):
        return self.__node.get("data", {})

    def get_is_wrap(self):
        return self.__before_wrap or self.__after_wrap

    def get_before_wrap(self):
        return self.__before_wrap

    def get_after_wrap(self):
        return self.__after_wrap


class Connection:
    def __init__(self, connection, config_connection):
        self.__type = "connection"
        self.__connection = connection
        self.__config_connection = config_connection

    def get_type(self):
        return self.__type

    def get_connection(self):
        return self.__connection

    def get_config_connection(self):
        return self.__config_connection

    def get_parameters(self):
        return self.__connection.get("parameters", {})

    def get_config_parameters(self):
        return {
            **self.__config_connection.get("object_parameters", {}),
            **self.__config_connection.get("type_object_parameters", {}),
            **self.__config_connection.get("objects_parameters", {}),
        }

    def get_connection_id(self):
        return self.__connection.get("connection_id")

    def get_data(self):
        return self.__connection.get("data", {})


class Diagram:
    def __init__(self, data, config_diagram_parameters):
        self.__type = "diagram"
        self.__diagram_type_id = data.get("diagram_type_id", 0)
        self.__diagram_name = data.get("diagram_name", "")
        self.__diagram_parameters = data.get("diagram_parameters", {})
        self.__config_diagram_parameters = config_diagram_parameters

    def get_type(self):
        return self.__type

    def get_diagram_type_id(self):
        return self.__diagram_type_id

    def get_diagram_name(self):
        return self.__diagram_name

    def get_parameters(self):
        return self.__diagram_parameters

    def get_config_parameters(self):
        return self.__config_diagram_parameters


class DiagramDrawer:
    """Класс для рисования диаграммы."""

    def __init__(self, obsm, data):
        self.__obsm = obsm
        self.__data = data
        #
        config_diagram_parameters = (
            self.__obsm.obj_configs.get_config_diagram_parameters_by_type_id(
                data.get("diagram_type_id", 0)
            )
        )
        self.__object_diagram = Diagram(data, config_diagram_parameters)
        #
        self.__nodes = self.__data.get("nodes", [])
        self.__connections = self.__data.get("connections", [])
        #
        self.__config_nodes = self.__obsm.obj_configs.get_nodes()
        self.__config_connections = self.__obsm.obj_configs.get_connections()

    def _get_delta_wrap_x(self, node):
        delta_wrap_x = (
            node.get("parameters", {}).get("delta_wrap_x", {}).get("value", 0)
        )
        print("_get_delta_wrap_x")
        print(node.get("parameters", {}))
        print(node.get("parameters", {}).get("delta_wrap_x", {}))
        print(node.get("parameters", {}).get("delta_wrap_x", {}).get("value", 0))
        return delta_wrap_x

    def _prepare_main_drawing_data(self):
        """Подготавливает данные для рисования"""
        start_x = int(self.__data.get("diagram_parameters", {}).get("start_x", {}).get("value", 0))
        start_y = int(self.__data.get("diagram_parameters", {}).get("start_y", {}).get("value", 0))
        delta_wrap_y = int(self.__data.get("diagram_parameters", {}).get("delta_wrap_y", {}).get("value", 0))
        #
        x = start_x
        y = start_y
        #
        to_right_optical_length = 0
        to_right_physical_length = 0
        #
        prepared_data = []
        #
        max_length = max(len(self.__nodes), len(self.__connections))
        # проход по всем узлам и соединениям по очереди
        for index in range(max_length):
            if index < len(self.__nodes):
                node = self.__nodes[index]
                # config
                node_id = node.get("node_id")
                if node_id is not None:
                    node_id_str = str(node_id)
                    config_node = self.__config_nodes.get(node_id_str, {})
                else:
                    config_node = {}
                #
                if index == 0:
                    x = start_x + self._get_delta_wrap_x(node)
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )
                elif not node.get("is_wrap"):
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )
                else:
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node, before_wrap=True),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )
                    x = start_x + self._get_delta_wrap_x(node)
                    y += delta_wrap_y
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node, after_wrap=True),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )

            if index < len(self.__connections):
                connection = self.__connections[index]
                # config
                connection_id = connection.get("connection_id")
                if connection_id is not None:
                    connection_id_str = str(connection_id)
                    config_connection = self.__config_connections.get(
                        connection_id_str, {}
                    )
                else:
                    config_connection = {}
                # parameters соединения
                parameters = connection.get("parameters", {})
                # Так по идее не работает config_connection.get("parameters", {})
                config_parameters = config_connection.get("parameters", {})
                #
                connection_length = parameters.get(
                    "connection_length",
                    config_parameters.get("connection_length", {}),
                ).get("value", 0)
                # data соединения
                data = connection.get("data", {})
                # Так по идее не работает config_connection.get("data", {})
                config_data = config_connection.get("data", {})
                connection_optical_length = data.get(
                    "оптическая_длина", config_data.get("оптическая_длина", {})
                ).get("value", 0)
                connection_physical_length = data.get(
                    "физическая_длина", config_data.get("физическая_длина", {})
                ).get("value", 0)
                #
                prepared_data.append(
                    {
                        "type": "connection",
                        "object": Connection(connection, config_connection),
                        "x": x,
                        "y": y,
                        "connection_optical_length": connection_optical_length,
                        "connection_physical_length": connection_physical_length,
                    }
                )
                # увеличиваем координаты по длине соединения
                x += connection_length
                # увеличиваем optical_length и physical_length
                to_right_optical_length += connection_optical_length
                to_right_physical_length += connection_physical_length

        return prepared_data, to_right_optical_length, to_right_physical_length

    def _set_to_left_lengths(
        self, prepared_data, to_right_optical_length, to_right_physical_length
    ):
        to_left_optical_length = to_right_optical_length
        to_left_physical_length = to_right_physical_length
        #
        for item in prepared_data:
            if item.get("type") == "node":
                item["to_left_optical_length"] = to_left_optical_length
                item["to_left_physical_length"] = to_left_physical_length
                print("_set_to_left_lengths item", item)
            #
            elif item.get("type") == "connection":
                to_left_optical_length -= item.get("connection_optical_length", 0)
                to_left_physical_length -= item.get("connection_physical_length", 0)

        return prepared_data
    

    def draw(self, painter):
        """Рисует диаграмму на переданном объекте QPainter."""
        # подготавливаем данные
        prepared_data, to_right_optical_length, to_right_physical_length = self._prepare_main_drawing_data()
        self.prepared_data = self._set_to_left_lengths(prepared_data, to_right_optical_length, to_right_physical_length)
        # сначала рисуем соединения
        for index, item in enumerate(self.prepared_data):
            if item.get("type") == "connection":
                # Кроме вершин ничего другого быть не может
                object_node_before = self.prepared_data[index - 1].get("object")
                object_node_after = self.prepared_data[index + 1].get("object")
                #
                object_connection = item.get("object")
                x = item.get("x")
                y = item.get("y")
                #
                self._draw_connection(
                    painter,
                    object_connection,
                    object_node_before,
                    object_node_after,
                    x,
                    y,
                )

        # Затем рисуем узлы
        for index, item in enumerate(self.prepared_data):
            if item.get("type") == "node":
                #
                object_before = None
                try:
                    if index > 0:
                        object_before = self.prepared_data[index - 1].get("object")
                except IndexError:
                    object_before = None
                #
                object_after = None
                try:
                    object_after = self.prepared_data[index + 1].get("object")
                except IndexError:
                    object_after = None
                #
                object_node = item.get("object")
                x = item.get("x")
                y = item.get("y")
                to_right_optical_length = item.get("to_right_optical_length")
                to_right_physical_length = item.get("to_right_physical_length")
                to_left_optical_length = item.get("to_left_optical_length")
                to_left_physical_length = item.get("to_left_physical_length")
                self._draw_node(
                    painter,
                    object_node,
                    object_before,
                    object_after,
                    x,
                    y,
                    to_right_optical_length,
                    to_right_physical_length,
                    to_left_optical_length,
                    to_left_physical_length,
                )

    def _draw_node(
        self,
        painter,
        object_node,
        object_before,
        object_after,
        x,
        y,
        to_right_optical_length,
        to_right_physical_length,
        to_left_optical_length,
        to_left_physical_length,
    ):
        node_obj = drawnode.DrawNode(
            painter,
            self.__object_diagram,
            object_node,
            object_before,
            object_after,
            x,
            y,
            to_right_optical_length,
            to_right_physical_length,
            to_left_optical_length,
            to_left_physical_length,
        )
        node_obj.draw()

    def _draw_connection(
        self, painter, object_connection, object_node_before, object_node_after, x, y
    ):
        connection_obj = drawconnection.DrawConnection(
            painter,
            self.__object_diagram,
            object_connection,
            object_node_before,
            object_node_after,
            x,
            y,
        )
        connection_obj.draw()
