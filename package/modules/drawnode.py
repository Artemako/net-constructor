from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawdataparameters as drawdataparameters
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject
import package.modules.numberformatter as numberformatter


class DrawNode:
    def __init__(
        self,
        painter,
        object_diagram,
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
        self.__object_diagram = object_diagram
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
        pars = drawdataparameters.DrawParameters(
            self.__object_diagram,
            self.__object_node,
            self.__object_before,
            self.__object_after,
        )
        diagram_type_id = self.__object_diagram.get_diagram_type_id()
        node_id = self.__object_node.get_node_id()
        #
        nf = numberformatter.NumberFormatter()
        nf.set_precision_number(pars.get_sp("precision_number"))
        nf.set_precision_separator(pars.get_sp("precision_separator"))
        #
        # "Скелетная схема ВОЛП и основные данные цепей кабеля"

        if diagram_type_id == "0":
            if node_id == "0" or node_id == "1":
                self._draw_node_ids_0_1(pars, data, node_id, nf)
        # "Схема размещения строительных длин и смонтированных муфт на участках регенерации между оконечными пунктами ВОЛП"
        elif diagram_type_id == "50":
            if node_id == "50" or node_id == "51":
                self._draw_node_ids_50_51(pars, data, node_id, nf)
        # "Скелетная схема размещения строительных длин кабеля и смонтированных муфт на участке регенерации"
        elif diagram_type_id == "100":
            if node_id == "100" or node_id == "101" or node_id == "102":
                print("_draw_node_ids_100_101_102")
                self._draw_node_ids_100_101_102(pars, data, node_id, nf)
        # "Монтажная схема участка регенерации"
        elif diagram_type_id == "150":
            if node_id == "150" or node_id == "151":
                self._draw_node_ids_150_151(pars, data, node_id, nf)

    def _draw_node_ids_0_1(self, pars, data, node_id, nf):
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
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )

        # радиус вершины
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "1":
            node_border_radius *= 2

        # рисование wrap стрелки
        if pars.get_sp("is_wrap_arrow"):
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
        drawobject.DrawObject().node_circle(
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
            self.__y - pars.get_sp("node_name_height"),
        )

    def _draw_node_ids_50_51(self, pars, data, node_id, nf):
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
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )

        # радиус вершины
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "51":
            node_border_radius *= 2

        # рисование wrap стрелки
        if pars.get_sp("is_wrap_arrow"):
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
                direction,
            )
            drawobject.DrawObject().arrow(
                get_painter_arrow,
                x,
                y + delta,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                direction,
            )

        def draw_text_caption(
            text,
            x,
            y,
            is_top_caption,
            horizontal_padding,
            vertical_padding,
            is_to_right=False,
        ):
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
                y - vertical_padding if is_top_caption else y + vertical_padding,
            )

        def draw_to_right():
            length = pars.get_sp("to_left_and_to_right_arrow_length")
            delta = pars.get_sp("delta_node_and_to_right_arrow")
            #
            draw_line_and_arrow(self.__x, self.__y, -length, delta, "right")
            #
            text_physical = nf.get(self.__to_right_physical_length) + pars.get_sp(
                "постфикс_расстояния"
            )
            draw_text_caption(
                text_physical,
                self.__x,
                self.__y - delta,
                pars.get_sp("is_top_node_top_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=True,
            )
            #
            text_optical = nf.get(self.__to_right_optical_length) + pars.get_sp(
                "постфикс_расстояния"
            )
            draw_text_caption(
                text_optical,
                self.__x,
                self.__y + delta,
                pars.get_sp("is_top_node_bottom_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=True,
            )

        def draw_to_left():
            length = pars.get_sp("to_left_and_to_right_arrow_length")
            delta = pars.get_sp("delta_node_and_to_left_arrow")
            #
            draw_line_and_arrow(self.__x, self.__y, length, delta, "left")
            #
            text_physical = nf.get(self.__to_left_physical_length) + pars.get_sp(
                "постфикс_расстояния"
            )
            draw_text_caption(
                text_physical,
                self.__x,
                self.__y - delta,
                pars.get_sp("is_top_node_top_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=False,
            )
            #
            text_optical = nf.get(self.__to_left_optical_length) + pars.get_sp(
                "постфикс_расстояния"
            )

            draw_text_caption(
                text_optical,
                self.__x,
                self.__y + delta,
                pars.get_sp("is_top_node_bottom_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=False,
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
        drawobject.DrawObject().node_circle(
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
            self.__y - pars.get_sp("node_name_height"),
        )

    def _draw_node_ids_100_101_102(self, pars, data, node_id, nf):
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

        def get_painter_text_name_add():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_add_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_add_pixel_size"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("node_caption_physics_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_caption_physics_pixel_size"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )

        # рисование wrap стрелки
        def draw_wrap_arrow(node_border_width):
            if pars.get_sp("is_wrap_arrow"):
                if self.__object_node.get_before_wrap():
                    drawobject.DrawObject().wrap_arrow(
                        get_painter_arrow,
                        get_painter_thin_line,
                        self.__x + node_border_width,
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
                        self.__x - node_border_width,
                        self.__y,
                        pars.get_sp("arrow_width"),
                        pars.get_sp("arrow_height"),
                        pars.get_sp("wrap_arrow_length"),
                        "after_wrap",
                    )

        def draw_node_id_100():
            # Рисование wrap стрелки
            draw_wrap_arrow(pars.get_sp("node_radius"))

            # Рисование вершины
            drawobject.DrawObject().node_circle(
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
                self.__y - pars.get_sp("node_name_height"),
            )

        def draw_node_id_101():
            # Рисование wrap стрелки
            draw_wrap_arrow(pars.get_sp("node_width") // 2)

            node_width = pars.get_sp("node_width")
            node_height = pars.get_sp("node_height")
            # Рисование вершины прямоугольника
            drawobject.DrawObject().node_reactangle(
                get_painter_figure_border,
                get_painter_figure_border_fill,
                self.__x,
                self.__y,
                node_width,
                node_height,
            )
            # Рисование названия
            text = data.get_sd("название")
            text_align_name = pars.get_sp("node_name_align")
            #
            if text_align_name == "LeftAlign":
                drawtext.DrawText().draw_multiline_text_by_hl_vb(
                    get_painter_text_name,
                    text,
                    self.__x - node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                )
            elif text_align_name == "RightAlign":
                drawtext.DrawText().draw_multiline_text_by_hr_vb(
                    get_painter_text_name,
                    text,
                    self.__x + node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                )
            else:
                drawtext.DrawText().draw_multiline_text_by_hc_vb(
                    get_painter_text_name,
                    text,
                    self.__x,
                    self.__y - pars.get_sp("node_name_height"),
                )

            # Рисование диапазона c 24 по 48 (внутри прямоугольника)
            text = data.get_sd("название_доп")
            drawtext.DrawText().draw_multiline_text_by_hc_vc(
                get_painter_text_name_add, text, self.__x, self.__y
            )

        def draw_node_id_102():
            # Рисование wrap стрелки
            draw_wrap_arrow(0)
            #
            self.__painter = get_painter_figure_border()
            self.__painter.drawLine(
                self.__x,
                self.__y - pars.get_sp("node_height"),
                self.__x,
                self.__y + pars.get_sp("node_height"),
            )

        # рисование вершины
        if node_id == "100":
            draw_node_id_100()
        elif node_id == "101":
            draw_node_id_101()
        elif node_id == "102":
            draw_node_id_102()

        # рисование значения физической длины
        x = self.__x
        if node_id == "101" and (not self.__object_before or self.__object_node.get_after_wrap()):
            x += pars.get_sp("node_width") // 2
        elif node_id == "101" and (not self.__object_after or self.__object_node.get_before_wrap()):
            x -= pars.get_sp("node_width") // 2
        drawtext.DrawText().draw_singleline_text_rotated_by_hc_vt(
            get_painter_text_caption,
            nf.get(self.__to_right_physical_length) + pars.get_sp("постфикс_расстояния"),
            x,
            self.__y + pars.get_sp("node_caption_physics_vertical_padding"),
        )


    def _draw_node_ids_150_151(self, pars, data, node_id, nf):
    
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

        def get_painter_text_name_add():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_add_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_add_pixel_size"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )
        

        
        # рисование wrap стрелки
        def draw_wrap_arrow(node_border_width):
            if pars.get_sp("is_wrap_arrow"):
                if self.__object_node.get_before_wrap():
                    drawobject.DrawObject().wrap_arrow(
                        get_painter_arrow,
                        get_painter_thin_line,
                        self.__x + node_border_width,
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
                        self.__x - node_border_width,
                        self.__y,
                        pars.get_sp("arrow_width"),
                        pars.get_sp("arrow_height"),
                        pars.get_sp("wrap_arrow_length"),
                        "after_wrap",
                    )

        def draw_node_id_150():
            # рисование wrap стрелки
            draw_wrap_arrow(pars.get_sp("node_radius"))
            # вершина
            drawobject.DrawObject().node_circle(
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
                self.__y - pars.get_sp("node_name_height"),
            )
            # Рисование номера (внутри круга)
            text = data.get_sd("название_доп")
            drawtext.DrawText().draw_multiline_text_by_hc_vc(
                get_painter_text_name_add, text, self.__x, self.__y
            )

        
        def draw_node_id_151():
            node_width = pars.get_sp("node_width")
            # рисование wrap стрелки
            draw_wrap_arrow(node_width // 2)
            # вершина
            drawobject.DrawObject().node_reactangle(
                get_painter_figure_border,
                get_painter_figure_border_fill,
                self.__x,
                self.__y,
                node_width,
                pars.get_sp("node_height"),
            )
            # Рисование названия
            text = data.get_sd("название")

            text_align_name = pars.get_sp("node_name_align")
            #
            if text_align_name == "LeftAlign":
                drawtext.DrawText().draw_multiline_text_by_hl_vb(
                    get_painter_text_name,
                    text,
                    self.__x - node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                )
            elif text_align_name == "RightAlign":
                drawtext.DrawText().draw_multiline_text_by_hr_vb(
                    get_painter_text_name,
                    text,
                    self.__x + node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                )
            else:
                drawtext.DrawText().draw_multiline_text_by_hc_vb(
                    get_painter_text_name,
                    text,
                    self.__x,
                    self.__y - pars.get_sp("node_name_height"),
                )






        
        if node_id == "150":
            draw_node_id_150()
        elif node_id == "151":
            draw_node_id_151()

