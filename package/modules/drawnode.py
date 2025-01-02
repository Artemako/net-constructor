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
        object_diagramm,
        object_node,
        object_before,
        object_after,
        x,
        y,
    ):
        self.__painter = painter
        self.__object_diagramm = object_diagramm
        self.__object_node = object_node
        self.__object_before = object_before
        self.__object_after = object_after
        self.__x = x
        self.__y = y
        #
        self.__diagramm_parameters = self.__object_diagramm.get_parameters()
        self.__config_diagramm_parameters = self.__object_diagramm.get_config_parameters()
        #
        self.__parameters = self.__object_node.get_parameters()
        self.__config_parameters = self.__object_node.get_config_parameters()


    def draw(self):
        # Сначала выбор диграммы, а потом узла
        if self.__object_diagramm.get_diagramm_type_id() == 0:
            #
            node_margin_top = self.__diagramm_parameters.get(
                "node_margin_top", self.__config_diagramm_parameters.get("node_margin_top", {})
            ).get("value", 0)
            title_pixel_size = self.__diagramm_parameters.get(
                "title_pixel_size", self.__config_diagramm_parameters.get("title_pixel_size", {})
            ).get("value", 0)
            node_radius = self.__diagramm_parameters.get(
                "node_radius", self.__config_diagramm_parameters.get("node_radius", {})
            ).get("value", 0)
            delta_node_and_thin_line = self.__diagramm_parameters.get(
                "delta_node_and_thin_line", self.__config_diagramm_parameters.get("delta_node_and_thin_line", {})
            ).get("value", 0)
            delta_thins_lines = self.__diagramm_parameters.get(
                "delta_thins_lines", self.__config_diagramm_parameters.get("delta_thins_lines", {})
            ).get("value", 0)
            #
            if self.__object_node.get_node_id() == "0":
                self._draw_node_id_0(node_margin_top, title_pixel_size, node_radius, delta_node_and_thin_line, delta_thins_lines)
            elif self.__object_node.get_node_id() == "1":
                self._draw_node_id_1(node_margin_top, title_pixel_size, node_radius, delta_node_and_thin_line, delta_thins_lines)

    def _draw_node_id_0(self, node_margin_top, title_pixel_size, node_radius, delta_node_and_thin_line, delta_thins_lines):
        # TODO Починить параметры!!!
        """Круглый, заливка диагональная штриховка, подпись сверху"""

        node_is_connected_with_thin_line_location = self.__parameters.get(
            "node_is_connected_with_thin_line_location",
            self.__config_parameters.get("node_is_connected_with_thin_line_location", {}),
        ).get("value", 0)
        
        # тонкая вертикальная линия
        def draw_vertical_thin_line():
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
            # рисовать линию - если node_is_connected_with_thin_line_location 
            if node_is_connected_with_thin_line_location:
                self.__painter.drawLine(
                    self.__x,
                    self.__y + delta_node_and_thin_line,
                    self.__x,
                    self.__y + delta_node_and_thin_line + delta_thins_lines + 5,
                )

        if self.__object_before and self.__object_before.get_type() == "connection":
            draw_vertical_thin_line()
        elif self.__object_after and self.__object_after.get_type() == "connection":
            draw_vertical_thin_line()

        # рисование вершины
        drawobject.DrawObject(self.__painter).node_gray_diagcross(
            self.__x, self.__y, node_radius
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
            text, self.__x, self.__y - node_margin_top
        )

    

    def _draw_node_id_1(self, node_margin_top, title_pixel_size, node_radius, delta_node_and_thin_line, delta_thins_lines):
        """Как и node_id 0 + большой круг с треугольник"""
        fill_color = Qt.white
        big_radius = node_radius * 2

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
        self._draw_node_id_0(node_margin_top, title_pixel_size, node_radius, delta_node_and_thin_line, delta_thins_lines)
