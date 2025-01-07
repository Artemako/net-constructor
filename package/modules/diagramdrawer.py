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

    # TODO 
    def get_config_parameters(self):
        return {**self.__config_node.get("object_parameters", {}), **self.__config_node.get("type_object_parameters", {})} 

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
    
    # TODO
    def get_config_parameters(self):
        return {**self.__config_connection.get("object_parameters", {}), **self.__config_connection.get("type_object_parameters", {})} 


    def get_connection_id(self):
        return self.__connection.get("connection_id")

    def get_data(self):
        return self.__connection.get("data", {})

class Diagramm:

    def __init__(self, data, config_diagramm_parameters):
        self.__type = "diagramm"
        self.__diagramm_type_id = data.get("diagramm_type_id", 0)
        self.__diagramm_name = data.get("diagramm_name", "")
        self.__diagramm_parameters = data.get("diagramm_parameters", {})
        self.__config_diagramm_parameters = config_diagramm_parameters

    def get_type(self):
        return self.__type
    
    def get_diagramm_type_id(self):
        return self.__diagramm_type_id
    
    def get_diagramm_name(self):
        return self.__diagramm_name
    
    def get_parameters(self):
        return self.__diagramm_parameters

    # TODO
    def get_config_parameters(self):
        return self.__config_diagramm_parameters


class DiagrammDrawer:
    """Класс для рисования диаграммы."""

    def __init__(self, obsm, data):
        self.__obsm = obsm
        self.__data = data
        #
        config_diagramm_parameters = self.__obsm.obj_configs.get_config_diagramm_parameters_by_type_id(data.get("diagramm_type_id", 0))
        self.__object_diagramm = Diagramm(data, config_diagramm_parameters)
        #
        self.__nodes = self.__data.get("nodes", [])
        self.__connections = self.__data.get("connections", [])
        #
        self.__config_nodes = self.__obsm.obj_configs.get_nodes()
        self.__config_connections = self.__obsm.obj_configs.get_connections()

    def _get_delta_wrap_x(self, node):
        delta_wrap_x = node.get("parameters", {}).get("delta_wrap_x", {}).get("value", 0)
        print("_get_delta_wrap_x")
        print(node.get("parameters", {}))
        print(node.get("parameters", {}).get("delta_wrap_x", {}))
        print(node.get("parameters", {}).get("delta_wrap_x", {}).get("value", 0))
        return delta_wrap_x

    def _prepare_main_drawing_data(self, start_x, start_y, delta_wrap_y):
        """Подготавливает данные для рисования: в оснвоном координаты."""
        x = start_x
        y = start_y
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
                        }
                    )
                elif not node.get("is_wrap"):
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node),
                            "x": x,
                            "y": y,
                        }
                    )
                else:
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node, before_wrap=True),
                            "x": x,
                            "y": y,
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
                #
                prepared_data.append(
                    {
                        "type": "connection",
                        "object": Connection(connection, config_connection),
                        "x": x,
                        "y": y,
                    }
                )
                # увеличиваем координаты по длине соединения
                parameters = connection.get("parameters", {})
                config_parameters = config_connection.get("parameters", {})
                connection_length = parameters.get(
                    "connection_length", config_parameters.get("connection_length", {})
                ).get("value", 0)
                x += connection_length

        return prepared_data

    def draw(self, painter, start_x, start_y, delta_wrap_y):
        """Рисует диаграмму на переданном объекте QPainter."""
        self.prepared_data = self._prepare_main_drawing_data(start_x, start_y, delta_wrap_y)
        # сначала рисуем соединения
        for index, item in enumerate(self.prepared_data):
            if item.get("type") == "connection":
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
                #
                self._draw_node(
                    painter,
                    object_node,
                    object_before,
                    object_after,
                    x,
                    y,
                )

    def _draw_node(
        self,
        painter,
        object_node,
        object_before,
        object_after,
        x,
        y,
    ):
        node_obj = drawnode.DrawNode(
            painter,
            self.__object_diagramm,
            object_node,
            object_before,
            object_after,
            x,
            y,
        )
        node_obj.draw()

    def _draw_connection(
        self, painter, object_connection, object_node_before, object_node_after, x, y
    ):
        connection_obj = drawconnection.DrawConnection(
            painter,
            self.__object_diagramm,
            object_connection,
            object_node_before,
            object_node_after,
            x,
            y,
        )
        connection_obj.draw()
