from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawdataparameters as drawdataparameters
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject
import package.modules.numberformatter as numberformatter


class DrawConnection:
    def __init__(
        self,
        painter,
        object_diagram,
        object_connection,
        object_node_before,
        object_node_after,
        x,
        y,
    ):
        self.__painter = painter
        self.__object_diagram = object_diagram
        self.__object_connection = object_connection
        self.__object_node_before = object_node_before
        self.__object_node_after = object_node_after
        self.__x = x
        self.__y = y

    def draw(self):
        # Сначала выбор диграммы, а потом соединения
        pars = drawdataparameters.DrawParameters(
            self.__object_diagram,
            self.__object_connection,
            self.__object_node_before,
            self.__object_node_after,
        )
        data = drawdataparameters.DrawData(self.__object_connection)
        #
        diagram_type_id = self.__object_diagram.get_diagram_type_id()
        connection_id = self.__object_connection.get_connection_id()
        #
        nf = numberformatter.NumberFormatter()
        nf.set_precision_number(pars.get_sp("precision_number"))
        nf.set_precision_separator(pars.get_sp("precision_separator"))
        #
        if diagram_type_id == "0":
            if connection_id == "0":
                self._draw_connection_type_0(pars, data, nf)
        #
        elif diagram_type_id == "50":
            if connection_id == "50":
                self._draw_connection_type_50(pars, data, nf)
        #
        elif diagram_type_id == "100":
            if connection_id == "100":
                self._draw_connection_type_100(pars, data, nf)
        #
        elif diagram_type_id == "150":
            if connection_id == "150":
                self._draw_connection_type_150(pars, data, nf)

    def _draw_connection_type_0(self, pars, data, nf):
        # Функции для получения различных пейнтеров
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
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

        def get_painter_text_name_and_location():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_name_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_name_pixel_size"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        #  Для LT и прочие
        before_delta_line_caption_and_node = 0
        after_delta_line_caption_and_node = 0
        #
        if self.__object_node_before.get_node_id() == "0":
            before_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + pars.get_bp("node_radius")
        elif self.__object_node_before.get_node_id() == "1":
            before_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + 2 * pars.get_bp("node_radius")
        #
        if self.__object_node_after.get_node_id() == "0":
            after_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + pars.get_ap("node_radius")
        elif self.__object_node_after.get_node_id() == "1":
            after_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + 2 * pars.get_ap("node_radius")

        # ОСНОВНАЯ ЛИНИЯ
        # region
        self.__painter = get_painter_connection_line()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )
        # endregion

        # подписи к основной линии (LT и прочие)
        # region
        text = pars.get_sp("префикс_ВОК") + data.get_sd("ВОК")
        drawtext.DrawText().draw_singleline_text_by_hl_vb(
            get_painter_text_caption,
            text,
            self.__x + before_delta_line_caption_and_node,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
        )

        # LB
        text = pars.get_sp("префикс_количество_ОВ") + data.get_sd("количество_ОВ")
        drawtext.DrawText().draw_singleline_text_by_hl_vt(
            get_painter_text_caption,
            text,
            self.__x + before_delta_line_caption_and_node,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
        )

        # RT
        text = (
            pars.get_sp("префикс_физическая_длина")
            + nf.get(data.get_sd("физическая_длина"))
            + pars.get_sp("постфикс_расстояния")
        )
        drawtext.DrawText().draw_singleline_text_by_hr_vb(
            get_painter_text_caption,
            text,
            self.__x
            + pars.get_sp("connection_length")
            - after_delta_line_caption_and_node,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
        )

        # RB
        text = (
            pars.get_sp("префикс_оптическая_длина")
            + nf.get(data.get_sd("оптическая_длина"))
            + pars.get_sp("постфикс_расстояния")
        )
        drawtext.DrawText().draw_singleline_text_by_hr_vt(
            get_painter_text_caption,
            text,
            self.__x
            + pars.get_sp("connection_length")
            - after_delta_line_caption_and_node,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
        )
        # endregion

        # тонкие линии
        # region
        # (строительная_длина)
        # горизонтальная линия - название
        self.__painter = get_painter_thin_line()
        self.__painter.drawLine(
            QPoint(
                self.__x - pars.get_sp("distance_thin_line_after_connection_x"),
                self.__y + pars.get_sp("delta_node_and_thin_line"),
            ),
            QPoint(
                self.__x
                + pars.get_sp("connection_length")
                + pars.get_sp("distance_thin_line_after_connection_x"),
                self.__y + pars.get_sp("delta_node_and_thin_line"),
            ),
        )
        # стрелки
        drawobject.DrawObject().arrow(
            get_painter_arrow,
            self.__x + pars.get_sp("connection_length"),
            self.__y + pars.get_sp("delta_node_and_thin_line"),
            pars.get_sp("arrow_width"),
            pars.get_sp("arrow_height"),
            "right",
        )
        drawobject.DrawObject().arrow(
            get_painter_arrow,
            self.__x,
            self.__y + pars.get_sp("delta_node_and_thin_line"),
            pars.get_sp("arrow_width"),
            pars.get_sp("arrow_height"),
            "left",
        )

        # горизонтальная линия - местоположение
        if pars.get_bp("is_location"):
            self.__painter = get_painter_thin_line()
            self.__painter.drawLine(
                QPoint(
                    self.__x - pars.get_sp("distance_thin_line_after_connection_x"),
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                ),
                QPoint(
                    self.__x
                    + pars.get_sp("connection_length")
                    + pars.get_sp("distance_thin_line_after_connection_x"),
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                ),
            )
            # стрелки + проверка соседних узлов
            if pars.get_bp("node_is_connected_with_thin_line_location"):
                drawobject.DrawObject().arrow(
                    get_painter_arrow,
                    self.__x,
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    "left",
                )
            if pars.get_ap("node_is_connected_with_thin_line_location"):
                drawobject.DrawObject().arrow(
                    get_painter_arrow,
                    self.__x + pars.get_sp("connection_length"),
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    "right",
                )
        # endregion

        # Тексты над/под название и название_доп и местоположение и местоположение_доп
        # region
        # Текст над/под с название и название_доп
        center_x = (self.__x + self.__x + pars.get_sp("connection_length")) // 2
        bottom_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            - pars.get_sp("connection_thin_caption_vertical_padding")
        )
        top_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            + pars.get_sp("connection_thin_caption_vertical_padding")
        )
        #
        text = data.get_sd("название")
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_name_and_location, text, center_x, bottom_y
        )
        #
        text = data.get_sd("название_доп")
        drawtext.DrawText().draw_multiline_text_by_hc_vt(
            get_painter_text_name_and_location, text, center_x, top_y
        )

        # Текст над/под с местоположение и местоположение_доп
        if pars.get_bp("is_location"):
            center_x_with_delta = (
                (self.__x + self.__x + pars.get_sp("connection_length")) // 2
            ) + pars.get_sp("connection_location_delta_x")
            bottom_y = (
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("delta_thins_lines")
                - pars.get_sp("connection_thin_caption_vertical_padding")
            )
            top_y = (
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("delta_thins_lines")
                + pars.get_sp("connection_thin_caption_vertical_padding")
            )
            #
            text = data.get_sd("местоположение")
            drawtext.DrawText().draw_multiline_text_by_hc_vb(
                get_painter_text_name_and_location, text, center_x_with_delta, bottom_y
            )
            #
            text = data.get_sd("местоположение_доп")
            drawtext.DrawText().draw_multiline_text_by_hc_vt(
                get_painter_text_name_and_location, text, center_x_with_delta, top_y
            )

        # endregion

    def _draw_connection_type_50(self, pars, data, nf):
        # Функции для получения различных пейнтеров
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        # ОСНОВНАЯ ЛИНИЯ
        self.__painter = get_painter_connection_line()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )

        def draw_text_caption(text, center_x, y, is_top):
            func_text = (
                drawtext.DrawText().draw_multiline_text_by_hc_vt
                if is_top
                else drawtext.DrawText().draw_multiline_text_by_hc_vb
            )
            func_text(get_painter_text_caption, text, center_x, y)

        draw_text_caption(
            pars.get_sp("префикс_физическая_длина")
            + nf.get(data.get_sd("физическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            (2 * self.__x + pars.get_sp("connection_length")) // 2,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
            True,
        )

        draw_text_caption(
            pars.get_sp("префикс_оптическая_длина")
            + nf.get(data.get_sd("оптическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            (2 * self.__x + pars.get_sp("connection_length")) // 2,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
            False,
        )

    def _draw_connection_type_100(self, pars, data, nf):
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        # ОСНОВНАЯ ЛИНИЯ
        self.__painter = get_painter_connection_line()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )

        # Текст над/под с названием и физическая_длина
        before_width = 0
        after_width = 0
        #
        if self.__object_node_before.get_node_id() == "101":
            before_width = pars.get_bp("node_width")
        if self.__object_node_after.get_node_id() == "101":
            after_width = pars.get_ap("node_width")
        #
        center_x = (
            (self.__x + before_width // 2)
            + (self.__x - after_width // 2 + pars.get_sp("connection_length"))
        ) // 2
        #
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_caption,
            data.get_sd("название"),
            center_x,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
        )
        #
        drawtext.DrawText().draw_multiline_text_by_hc_vt(
            get_painter_text_caption,
            nf.get(data.get_sd("физическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            center_x,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
        )


    def _draw_connection_type_150(self, pars, data, nf):
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        # ОСНОВНАЯ ЛИНИЯ
        self.__painter = get_painter_connection_line()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )

        # Текст над/под 
        before_width = 0
        after_width = 0
        #
        if self.__object_node_before.get_node_id() == "151":
            before_width = pars.get_bp("node_width")
        if self.__object_node_after.get_node_id() == "151":
            after_width = pars.get_ap("node_width")
        #
        center_x = (
            (self.__x + before_width // 2)
            + (self.__x - after_width // 2 + pars.get_sp("connection_length"))
        ) // 2
        #
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_caption,
            nf.get(data.get_sd("оптическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            center_x,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
        )
        #
        drawtext.DrawText().draw_multiline_text_by_hc_vt(
            get_painter_text_caption,
            data.get_sd("название_доп")
            + "\n"
            + nf.get(data.get_sd("физическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            center_x,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
        )