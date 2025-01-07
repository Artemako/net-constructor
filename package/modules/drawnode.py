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

    def _draw_node_ids_0_1(self, pars, data, node_id="0"):
        
        def get_painter_figure_border():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_border(pen_color="#000000", pen_weight=2)

        def get_painter_figure_border_fill():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_figure_border_fill(
                pen_color=Qt.black,
                pen_weight=2,
                fill_color="A0A0A4",
                fill_pattern=Qt.DiagCrossPattern,
            )

        def get_painter_text_name():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_color"),
                pixel_size=pars.get_sp("node_name_pixel_size"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(self.__painter).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"), fill_pattern=Qt.SolidPattern
            )


        # тонкая вертикальная линия
        def draw_vertical_thin_line():
            painter_thin_line = get_painter_thin_line()
            painter_thin_line.drawLine(
                self.__x,
                self.__y,
                self.__x,
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("distance_thin_line_after_connection_y"),
            )
            # рисовать линию - если pars.get_sp("node_is_connected_with_thin_line_location")
            if pars.get_sp("node_is_connected_with_thin_line_location"):
                painter_thin_line.drawLine(
                    self.__x,
                    self.__y + pars.get_sp("delta_node_and_thin_line"),
                    self.__x,
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines")
                    + pars.get_sp("distance_thin_line_after_connection_y"),
                )

        # Проверяем наличие соединения
        if self.__object_before and self.__object_before.get_type() == "connection":
            draw_vertical_thin_line()
        elif self.__object_after and self.__object_after.get_type() == "connection":
            draw_vertical_thin_line()

        if node_id == "1":
            # Рисуем большой круг с треугольником
            big_radius = pars.get_sp("node_radius") * 2
            points = QPolygon(
                [
                    QPoint(self.__x, self.__y - big_radius),
                    QPoint(self.__x - big_radius * 0.865, self.__y + big_radius // 2),
                    QPoint(self.__x + big_radius * 0.865, self.__y + big_radius // 2),
                ]
            )

            # Рисуем круг и треугольник
            self.__painter = get_painter_figure_border()
            self.__painter.drawEllipse(
                QPoint(self.__x, self.__y), big_radius, big_radius
            )
            self.__painter.drawPolygon(points)

        # Рисование вершины
        drawobject.DrawObject().node_gray_diagcross(
            get_painter_figure_border, get_painter_figure_border_fill,
            self.__x, self.__y, pars.get_sp("node_radius")
        )

        # Рисование названия
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "1":
            node_border_radius *= 2
        
        text = data.get_sd("название")
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_name,
            text,
            self.__x,
            self.__y - node_border_radius - pars.get_sp("node_margin_top"),
        )


        # рисование wrap стрелки
        # drawobject.DrawObject().arrow(
        #     self.__x + pars.get_sp("connection_length"),
        #     self.__y + pars.get_sp("delta_node_and_thin_line"),
        #     pars.get_sp("arrow_width"),
        #     pars.get_sp("arrow_height"),
        #     "right",
        # )
