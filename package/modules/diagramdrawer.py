import package.modules.drawnode as drawnode
import package.modules.drawconnection as drawconnection


class Node:
    def __init__(
        self, node=None, config_node=None, before_wrap=False, after_wrap=False
    ):
        self.__type = "node"
        self.__node = node
        self.__config_node = config_node
        self.__before_wrap = False
        self.__after_wrap = False

    def get_type(self):
        return self.__type

    def get_node(self):
        return self.__node

    def get_id(self):
        return self.__node.get("id")

    def get_config_node(self):
        return self.__config_node

    def get_metrics(self):
        return self.__node.get("metrics", {})

    def get_config_metrics(self):
        return self.__config_node.get("metrics", {})

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

    def get_metrics(self):
        return self.__connection.get("metrics", {})

    def get_config_metrics(self):
        return self.__config_connection.get("metrics", {})

    def get_connection_id(self):
        return self.__connection.get("connection_id")

    def get_data(self):
        return self.__connection.get("data", {})


class DiagramDrawer:
    """Класс для рисования диаграммы."""

    def __init__(self, obsm, data):
        self.__obsm = obsm
        self.__data = data
        #
        self.__nodes = data.get("nodes", [])
        self.__connections = data.get("connections", [])
        #
        self.__config_nodes = self.__obsm.obj_configs.get_nodes()
        self.__config_connections = self.__obsm.obj_configs.get_connections()

    def prepare_main_drawing_data(self, start_x, start_y):
        """Подготавливает данные для рисования: в оснвоном координаты."""
        x = start_x
        y = start_y
        #
        prepared_data = []
        #
        max_length = max(len(self.__nodes), len(self.__connections))
        # проход по всем узлам и соединениям по очереди
        for i in range(max_length):
            if i < len(self.__nodes):
                node = self.__nodes[i]
                # config
                node_id = node.get("node_id")
                if node_id is not None:
                    node_id_str = str(node_id)
                    config_node = self.__config_nodes.get(node_id_str, {})
                else:
                    config_node = {}
                #
                if not node.get("is_wrap"):
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
                    # TODO y += 200 на кастомное меняемое значение
                    x = start_x
                    y += 200
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node, after_wrap=True),
                            "x": x,
                            "y": y,
                        }
                    )

            # TODO Учитывать размер узла для подписей connections
            if i < len(self.__connections):
                connection = self.__connections[i]
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
                metrics = connection.get("metrics", {})
                config_metrics = config_connection.get("metrics", {})
                length = metrics.get("length", config_metrics.get("length", {})).get(
                    "value", 0
                )
                x += length

        return prepared_data

    def draw(self, painter, start_x, start_y):
        """Рисует диаграмму на переданном объекте QPainter."""
        self.prepared_data = self.prepare_main_drawing_data(start_x, start_y)
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
                self.draw_connection(
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
                self.draw_node(
                    painter,
                    object_node,
                    object_before,
                    object_after,
                    x,
                    y,
                )

    def draw_node(
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
            object_node,
            object_before,
            object_after,
            x,
            y,
        )
        node_obj.draw()

    def draw_connection(
        self, painter, object_connection, object_node_before, object_node_after, x, y
    ):
        connection_obj = drawconnection.DrawConnection(
            painter, object_connection, object_node_before, object_node_after, x, y
        )
        connection_obj.draw()
