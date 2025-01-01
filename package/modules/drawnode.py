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
        object_before,
        object_after,
        x,
        y,
    ):
        self.__painter = painter
        self.__object_node = object_node
        self.__object_before = object_before
        self.__object_after = object_after
        self.__x = x
        self.__y = y
        #
        self.__parameters = object_node.get_parameters()
        self.__config_parameters = object_node.get_config_parameters()


    def draw(self):
        if self.__object_node.get_node_id() == "0":
            self.draw_node_id_0()
        elif self.__object_node.get_node_id() == "1":
            self.draw_node_id_1()

    def draw_node_id_0(self):
        # TODO Починить параметры!!!
        """Круглый, заливка диагональная штриховка, подпись сверху"""
        # узнать значения
        margin_top = self.__parameters.get(
            "margin_top", self.__config_parameters.get("margin_top", {})
        ).get("value", 0)
        title_pixel_size = self.__parameters.get(
            "title_pixel_size", self.__config_parameters.get("title_pixel_size", {})
        ).get("value", 0)
        radius = self.__parameters.get(
            "radius", self.__config_parameters.get("radius", {})
        ).get("value", 0)
        is_connected_with_thin_line_location = self.__parameters.get(
            "is_connected_with_thin_line_location",
            self.__config_parameters.get("is_connected_with_thin_line_location", {}),
        ).get("value", 0)
        

        # тонкая вертикальная линия
        def draw_vertical_thin_line(object):
            parameters = object.get_parameters()
            config_parameters = object.get_config_parameters()
            #
            delta_node_and_thin_line = parameters.get(
                "delta_node_and_thin_line", config_parameters.get("delta_node_and_thin_line", {})
            ).get("value", 0)
            delta_thins_lines = parameters.get(
                "delta_thins_lines", config_parameters.get("delta_thins_lines", {})
            ).get("value", 0)
            #
            self.__painter = painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_thin_line_painter()
            #
            self.__painter.drawLine(
                self.__x,
                self.__y,
                self.__x,
                self.__y + delta_node_and_thin_line + 5,
            )
            # рисовать линию - если is_connected_with_thin_line_location 
            if is_connected_with_thin_line_location:
                self.__painter.drawLine(
                    self.__x,
                    self.__y + delta_node_and_thin_line,
                    self.__x,
                    self.__y + delta_node_and_thin_line + delta_thins_lines + 5,
                )

        if self.__object_before and self.__object_before.get_type() == "connection":
            draw_vertical_thin_line(self.__object_before)
        elif self.__object_after and self.__object_after.get_type() == "connection":
            draw_vertical_thin_line(self.__object_after)

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
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(
            text, self.__x, self.__y - margin_top
        )

    

    def draw_node_id_1(self):
        """Как и node_id 0 + большой круг с треугольник"""
        fill_color = Qt.white

        # узнать значения
        radius = self.__parameters.get(
            "radius", self.__config_parameters.get("radius", {})
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
