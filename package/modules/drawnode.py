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
        to_right_optical_length,
        to_right_physical_length,
        to_left_optical_length,
        to_left_physical_length,
    ):
        self.__painter = painter
        self.__object_diagramm = object_diagramm
        self.__object_node = object_node
        self.__object_before = object_before
        self.__object_after = object_after
        self.__x = x
        self.__y = y
        self.__to_right_optical_length = to_right_optical_length
        self.__to_right_physical_length = to_right_physical_length
        self.__to_left_optical_length = to_left_optical_length
        self.__to_left_physical_length = to_left_physical_length

    def draw(self):
        # Сначала выбор диграммы, а потом узла
        data = drawdataparameters.DrawData(self.__object_node)
        # "Скелетная схема ВОЛП и основные данные цепей кабеля"
        if self.__object_diagramm.get_diagramm_type_id() == "0":
            #
            pars = drawdataparameters.DrawParameters(
                self.__object_diagramm,
                self.__object_node,
                self.__object_before,
                self.__object_after,
            )
            node_id = self.__object_node.get_node_id()
            self._draw_node_ids_0_1(pars, data, node_id)
        # "Схема размещения строительных длин и смонтированных муфт на участках регенерации между оконечными пунктами ВОЛП"
        elif self.__object_diagramm.get_diagramm_type_id() == "50":
            # TODO
            pars = drawdataparameters.DrawParameters(
                self.__object_diagramm,
                self.__object_node,
                self.__object_before,
                self.__object_after,
            )
            node_id = self.__object_node.get_node_id()
            self._draw_node_ids_50_51(pars, data, node_id)
        # "Скелетная схема размещения строительных длин кабеля и смонтированных муфт на участке регенерации"
        # "Монтажная схема участка регенерации"

    def _draw_node_ids_0_1(self, pars, data, node_id="0"):
        def get_painter_figure_border():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_border(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
            )

        def get_painter_figure_border_fill():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_figure_border_fill(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
                fill_color=pars.get_sp("node_fill_color"),
                fill_pattern_name=pars.get_sp("node_fill_style"),
            )

        def get_painter_text_name():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_color"),
                font_name=pars.get_sp("font_name"),
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
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="Qt.SolidPattern",
            )

        # радиус вершины
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "1":
            node_border_radius *= 2

        # рисование wrap стрелки
        if self.__object_node.get_before_wrap():
            drawobject.DrawObject().wrap_arrow(
                get_painter_arrow,
                get_painter_thin_line,
                self.__x + node_border_radius,
                self.__y,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                pars.get_sp("wrap_arrow_length"),
                "before_wrap",
            )
        elif self.__object_node.get_after_wrap():
            drawobject.DrawObject().wrap_arrow(
                get_painter_arrow,
                get_painter_thin_line,
                self.__x - node_border_radius,
                self.__y,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                pars.get_sp("wrap_arrow_length"),
                "after_wrap",
            )

        # тонкая вертикальная линия
        def draw_vertical_thin_line():
            painter_thin_line = get_painter_thin_line()
            painter_thin_line.drawLine(
                QPointF(self.__x, self.__y),
                QPointF(
                    self.__x,
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("distance_thin_line_after_connection_y"),
                ),
            )
            # рисовать линию ЕСЛИ is_location И node_is_connected_with_thin_line_location
            if pars.get_sp("is_location") and pars.get_sp(
                "node_is_connected_with_thin_line_location"
            ):
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
            drawobject.DrawObject().node_big_circle_and_triangle(
                get_painter_figure_border,
                self.__x,
                self.__y,
                node_border_radius,
            )

        # Рисование вершины
        drawobject.DrawObject().node_gray_diagcross(
            get_painter_figure_border,
            get_painter_figure_border_fill,
            self.__x,
            self.__y,
            pars.get_sp("node_radius"),
        )

        # Рисование названия
        text = data.get_sd("название")
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_name,
            text,
            self.__x,
            self.__y - node_border_radius - pars.get_sp("node_margin_top"),
        )

    def _draw_node_ids_50_51(self, pars, data, node_id="50"):
        ...

        def get_painter_figure_border():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_border(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
            )

        def get_painter_figure_border_fill():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_figure_border_fill(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
                fill_color=pars.get_sp("node_fill_color"),
                fill_pattern_name=pars.get_sp("node_fill_style"),
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
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="Qt.SolidPattern",
            )

        # радиус вершины
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "51":
            node_border_radius *= 2

        # рисование wrap стрелки
        if self.__object_node.get_before_wrap():
            drawobject.DrawObject().wrap_arrow(
                get_painter_arrow,
                get_painter_thin_line,
                self.__x + node_border_radius,
                self.__y,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                pars.get_sp("wrap_arrow_length"),
                "before_wrap",
            )
        elif self.__object_node.get_after_wrap():
            drawobject.DrawObject().wrap_arrow(
                get_painter_arrow,
                get_painter_thin_line,
                self.__x - node_border_radius,
                self.__y,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                pars.get_sp("wrap_arrow_length"),
                "after_wrap",
            )

        # тонкая вертикальная линия
        painter_thin_line = get_painter_thin_line()
        delta_node_and_arrow_and_distance_thin_line_after_connection_y = max(
            pars.get_sp("delta_node_and_to_right_arrow"),
            pars.get_sp("delta_node_and_to_left_arrow"),
        ) + pars.get_sp("distance_thin_line_after_connection_y")
        #
        painter_thin_line.drawLine(
            QPointF(
                self.__x,
                self.__y
                - delta_node_and_arrow_and_distance_thin_line_after_connection_y,
            ),
            QPointF(
                self.__x,
                self.__y
                + delta_node_and_arrow_and_distance_thin_line_after_connection_y,
            )
        )
        # TODO + дельта ТЕкст и стрелочик (выбор над/под)
        # рисование to_right to_left стрелок с линией и со значениями
        # to_right
        if not(self.__object_node.get_after_wrap() or not self.__object_before):
            ...

        # to_left
        if not(self.__object_node.get_before_wrap() or not self.__object_after):
            ...
    

        # # рисовать линию ЕСЛИ is_location И node_is_connected_with_thin_line_location
        # if pars.get_sp("is_location") and pars.get_sp(
        #     "node_is_connected_with_thin_line_location"
        # ):
        #     painter_thin_line.drawLine(
        #         self.__x,
        #         self.__y + pars.get_sp("delta_node_and_thin_line"),
        #         self.__x,
        #         self.__y
        #         + pars.get_sp("delta_node_and_thin_line")
        #         + pars.get_sp("delta_thins_lines")
        #         + pars.get_sp("distance_thin_line_after_connection_y"),
        #     )

        # # Проверяем наличие соединения
        # if self.__object_before and self.__object_before.get_type() == "connection":
        #     draw_vertical_thin_line()
        # elif self.__object_after and self.__object_after.get_type() == "connection":
        #     draw_vertical_thin_line()

        # if node_id == "1":
        #     drawobject.DrawObject().node_big_circle_and_triangle(
        #         get_painter_figure_border,
        #         self.__x,
        #         self.__y,
        #         node_border_radius,
        #     )

        # # Рисование вершины
        # drawobject.DrawObject().node_gray_diagcross(
        #     get_painter_figure_border,
        #     get_painter_figure_border_fill,
        #     self.__x,
        #     self.__y,
        #     pars.get_sp("node_radius"),
        # )

        # # Рисование названия
        # text = data.get_sd("название")
        # drawtext.DrawText().draw_multiline_text_by_hc_vb(
        #     get_painter_text_name,
        #     text,
        #     self.__x,
        #     self.__y - node_border_radius - pars.get_sp("node_margin_top"),
        # )
