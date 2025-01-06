from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawdataparameters as drawdataparameters
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

    def draw(self):
        # Сначала выбор диграммы, а потом узла
        data = drawdataparameters.DrawData(self.__object_node)
        if self.__object_diagramm.get_diagramm_type_id() == "0":
            #
            pars = drawdataparameters.DrawParameters(
                self.__object_diagramm,
                self.__object_node,
                self.__object_before,
                self.__object_after,
            )
            node_id = self.__object_node.get_node_id()
            if node_id == "0":
                self._draw_node_ids_0_1(pars, data, node_id)
            elif node_id == "1":
                self._draw_node_ids_0_1(pars, data, node_id)

    def _draw_node_id_0(self, pars, data, node_id):
        self._draw_node_ids_0_1(pars, data, node_id)

    def _draw_node_ids_0_1(self, pars, data, node_id="0"):
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
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("distance_thin_line_after_connection_y"),
            )
            # рисовать линию - если pars.get_sp("node_is_connected_with_thin_line_location")
            if pars.get_sp("node_is_connected_with_thin_line_location"):
                self.__painter.drawLine(
                    self.__x,
                    self.__y + pars.get_sp("delta_node_and_thin_line"),
                    self.__x,
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines")
                    + pars.get_sp("distance_thin_line_after_connection_y"),
                )

        if self.__object_before and self.__object_before.get_type() == "connection":
            draw_vertical_thin_line()
        elif self.__object_after and self.__object_after.get_type() == "connection":
            draw_vertical_thin_line()

        if node_id == "1":
            # рисование большого круга с треугольником
            big_radius = pars.get_sp("node_radius") * 2
            # данные по треугольнику
            points = QPolygon(
                [
                    QPoint(self.__x, self.__y - big_radius),
                    QPoint(self.__x - big_radius * 0.865, self.__y + big_radius // 2),
                    QPoint(self.__x + big_radius * 0.865, self.__y + big_radius // 2),
                ]
            )

            self.__painter = painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_figure_painter()
            # рисуем круг, а потом треугольник
            self.__painter.drawEllipse(
                QPoint(self.__x, self.__y), big_radius, big_radius
            )
            self.__painter.drawPolygon(points)

        # рисование вершины
        drawobject.DrawObject(self.__painter).node_gray_diagcross(
            self.__x, self.__y, pars.get_sp("node_radius")
        )

        # рисование названия
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "0":
            pass
        elif node_id == "1":
            node_border_radius *= 2
        #
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
        ).get_main_name_painter(pars.get_sp("node_name_pixel_size"))
        text = data.get_sd("название")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(
            text,
            self.__x,
            self.__y - node_border_radius - pars.get_sp("node_margin_top"),
        )
