from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPoint

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
        self.__to_right_optical_length = str(to_right_optical_length)
        self.__to_right_physical_length = str(to_right_physical_length)
        self.__to_left_optical_length = str(to_left_optical_length)
        self.__to_left_physical_length = str(to_left_physical_length)

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
                QPoint(self.__x, self.__y),
                QPoint(
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
                    QPoint(
                        self.__x, self.__y + pars.get_sp("delta_node_and_thin_line")
                    ),
                    QPoint(
                        self.__x,
                        self.__y
                        + pars.get_sp("delta_node_and_thin_line")
                        + pars.get_sp("delta_thins_lines")
                        + pars.get_sp("distance_thin_line_after_connection_y"),
                    ),
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
            self.__y - pars.get_sp("node_margin_top"),
        )

    def _draw_node_ids_50_51(self, pars, data, node_id="50"):

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

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("node_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_caption_pixel_size"),
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
            QPoint(
                self.__x,
                self.__y
                - delta_node_and_arrow_and_distance_thin_line_after_connection_y,
            ),
            QPoint(
                self.__x,
                self.__y
                + delta_node_and_arrow_and_distance_thin_line_after_connection_y,
            ),
        )
        # рисование to_right to_left стрелок с линией и со значениями

        def draw_line_and_arrow(x, y, length, delta, direction):
            self.__painter = get_painter_thin_line()
            self.__painter.drawLine(QPoint(x + length, y - delta), QPoint(x, y - delta))
            self.__painter.drawLine(QPoint(x + length, y + delta), QPoint(x, y + delta))
            #
            drawobject.DrawObject().arrow(
                get_painter_arrow,
                x,
                y - delta,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                direction
            )
            drawobject.DrawObject().arrow(
                get_painter_arrow,
                x,
                y + delta,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                direction
            )

        def draw_text_caption(text, x, y, is_top_caption, horizontal_padding, vertical_padding, is_to_right=False):
            draw_func = None
            if is_to_right:
                draw_func = (
                    drawtext.DrawText().draw_singleline_text_by_hr_vb
                    if is_top_caption
                    else drawtext.DrawText().draw_singleline_text_by_hr_vt
                )
            else:
                draw_func = (
                    drawtext.DrawText().draw_singleline_text_by_hl_vb
                    if is_top_caption
                    else drawtext.DrawText().draw_singleline_text_by_hl_vt
                )
            #
            draw_func(
                get_painter_text_caption,
                text,
                x - horizontal_padding if is_to_right else x + horizontal_padding,
                y - vertical_padding if is_top_caption else y + vertical_padding
            )

        def draw_to_right():
            length = pars.get_sp("to_left_and_to_right_arrow_length")
            delta = pars.get_sp("delta_node_and_to_right_arrow")
            #
            draw_line_and_arrow(self.__x, self.__y, -length, delta, "right")
            #
            text_physical = self.__to_right_physical_length + pars.get_sp("постфикс_расстояния")
            # print(f"self.__to_right_physical_length = {self.__to_right_physical_length}")
            # print(f"text_physical = {text_physical}")
            draw_text_caption(
                text_physical,
                self.__x,
                self.__y - delta,
                pars.get_sp("is_top_node_top_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right = True
            )
            #
            text_optical = self.__to_right_optical_length + pars.get_sp("постфикс_расстояния")
            draw_text_caption(
                text_optical,
                self.__x,
                self.__y + delta,
                pars.get_sp("is_top_node_bottom_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right = True
            )

        def draw_to_left():            
            length = pars.get_sp("to_left_and_to_right_arrow_length")
            delta = pars.get_sp("delta_node_and_to_left_arrow")
            #
            draw_line_and_arrow(self.__x, self.__y, length, delta, "left")
            #
            text_physical = self.__to_left_physical_length + pars.get_sp("постфикс_расстояния")
            draw_text_caption(
                text_physical,
                self.__x,
                self.__y - delta,
                pars.get_sp("is_top_node_top_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right = False
            )
            #
            text_optical = self.__to_left_optical_length + pars.get_sp("постфикс_расстояния")
            print(f"text_optical = {text_optical}")
            print(f"постфикс_расстояния = {data.get_sd('постфикс_расстояния')}")
            print(f"self.__to_left_optical_length = {self.__to_left_optical_length}")
            draw_text_caption(
                text_optical,
                self.__x,
                self.__y + delta,
                pars.get_sp("is_top_node_bottom_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right = False
            )

        #
        if not (self.__object_node.get_after_wrap() or not self.__object_before):
            draw_to_right()
        #
        if not (self.__object_node.get_before_wrap() or not self.__object_after):
            draw_to_left()



        if node_id == "51":
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
            self.__y - pars.get_sp("node_margin_top"),
        )
