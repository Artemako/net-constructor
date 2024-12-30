from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject


class DrawNode:
    def __init__(
        self,
        painter,
        object_node,
        x,
        y,
    ):
        self.__painter = painter
        self.__object_node = object_node
        self.__x = x
        self.__y = y
        #
        self.__metrics = object_node.get_metrics()
        self.__config_metrics = object_node.get_config_metrics()

    def draw(self):
        if self.__object_node.get_node_id() == "0":
            self.draw_node_id_0()
        elif self.__object_node.get_node_id() == "1":
            self.draw_node_id_1()

    def draw_node_id_0(self):
        """Круглый, заливка диагональная штриховка, подпись сверху"""
        # узнать значения
        radius = self.__metrics.get(
            "radius", self.__config_metrics.get("radius", {})
        ).get("value", 0)
        margin_top = self.__metrics.get(
            "margin_top", self.__config_metrics.get("margin_top", {})
        ).get("value", 0)
        title_pixel_size = self.__metrics.get(
            "title_pixel_size", self.__config_metrics.get("title_pixel_size", {})
        ).get("value", 0)

        # рисование вершины
        drawobject.DrawObject(self.__painter).node_gray_diagcross(
            self.__x, self.__y, radius
        )

        # рисование
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=QPen(Qt.black, 2),
            brush=QBrush(Qt.NoBrush),
            font=QFont().setPixelSize(title_pixel_size),
        ).get_painter()
        text = self.__object_node.get_data().get("название", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_centered_by_bottom_multiline_text(
            text, self.__x, self.__y - margin_top
        )

    # TODO Подумать про групповые соединения

    def draw_node_id_1(self):
        """Как и node_id 0 + большой круг с треугольник"""
        fill_color = Qt.white

        # узнать значения
        radius = self.__metrics.get(
            "radius", self.__config_metrics.get("radius", {})
        ).get("value", 0)
        big_radius = radius * 2

        # данные по треугольнику
        triangle_height = big_radius
        points = QPolygon(
            [
                QPoint(self.__x, self.__y - triangle_height),
                QPoint(
                    self.__x - triangle_height * 0.865, self.__y + triangle_height // 2
                ),
                QPoint(
                    self.__x + triangle_height * 0.865, self.__y + triangle_height // 2
                ),
            ]
        )

        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter, pen=QPen(Qt.black, 2), brush=QBrush(fill_color)
        ).get_painter()
        # рисуем круг, а потом треугольник
        self.__painter.drawEllipse(QPoint(self.__x, self.__y), big_radius, big_radius)
        self.__painter.drawPolygon(points)

        # рисуем и draw_node_id_0
        self.draw_node_id_0()
