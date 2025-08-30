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
        control_sectors,
        to_right_physical_length,
        start_x,
        delta_wrap_y,
    ):
        self.__painter = painter
        self.__object_diagram = object_diagram
        self.__object_connection = object_connection
        self.__object_node_before = object_node_before
        self.__object_node_after = object_node_after
        self.__x = x
        self.__y = y
        self.__control_sectors = control_sectors
        self.__to_right_physical_length = to_right_physical_length
        self.__start_x = start_x
        self.__delta_wrap_y = delta_wrap_y
        print(
            f"LALALA self.__to_right_physical_length = {self.__to_right_physical_length}"
        )

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
            + nf.get(data.get_sd("физ_и_опт_длины", "фд"))
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
            + nf.get(data.get_sd("физ_и_опт_длины", "од"))
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
            + nf.get(data.get_sd("физ_и_опт_длины", "фд"))
            + pars.get_sp("постфикс_расстояния"),
            (2 * self.__x + pars.get_sp("connection_length")) // 2,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
            True,
        )

        draw_text_caption(
            pars.get_sp("префикс_оптическая_длина")
            + nf.get(data.get_sd("физ_и_опт_длины", "од"))
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

        def draw_main_line(
            cs_lenght, cs_name, cs_physical_length, is_first=False, is_last=False
        ):
            # ОСНОВНАЯ ЛИНИЯ
            self.__painter = get_painter_connection_line()
            self.__painter.drawLine(
                self.__x,
                self.__y,
                self.__x + cs_lenght,
                self.__y,
            )
            # Текст над/под с названием и физическая_длина
            before_half_width = 0
            after_half_width = 0
            #
            before_padding = 0
            after_padding = 0
            # Условия для первого и для последнего сектора
            if is_first and self.__object_node_before.get_node_id() == "101":
                before_half_width = pars.get_bp("node_width") // 2
                before_padding = before_half_width
            elif is_first and self.__object_node_before.get_node_id() == "100":
                before_half_width = pars.get_bp("node_radius")
                before_padding = before_half_width
            if is_last and self.__object_node_after.get_node_id() == "101":
                after_half_width = pars.get_ap("node_width") // 2
                after_padding = after_half_width
            elif is_last and self.__object_node_after.get_node_id() == "100":
                after_half_width = pars.get_ap("node_radius")
                after_padding = after_half_width
            #
            center_x = (
                (self.__x + before_half_width)
                + (self.__x - after_half_width + cs_lenght)
            ) // 2
            #
            print(f"cs_lenght = {cs_lenght}")
            #
            drawtext.DrawText().draw_multiline_text_by_hc_vb(
                get_painter_text_caption,
                cs_name,
                center_x,
                self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
                cs_lenght - before_padding - after_padding - 10,
            )
            #
            drawtext.DrawText().draw_multiline_text_by_hc_vt(
                get_painter_text_caption,
                nf.get(cs_physical_length) + pars.get_sp("постфикс_расстояния"),
                center_x,
                self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
                cs_lenght - before_padding - after_padding - 10,
            )

        def draw_control_point(is_before_wrap=False, is_after_wrap=False):
            def get_painter_figure_border():
                return painterconfigurator.PainterConfigurator(
                    self.__painter
                ).get_painter_figure_border(
                    pen_color=pars.get_sp("node_border_color"),
                    pen_weight=pars.get_sp("node_border_weight"),
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
                    if is_before_wrap:
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
                    elif is_after_wrap:
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

            # рисование значения физической длины
            x = self.__x
            # TODO Для первых и послдених вершин
            # if node_id == "101" and (not self.__object_before or self.__object_node.get_after_wrap()):
            #     x += pars.get_sp("node_width") // 2
            # elif node_id == "101" and (not self.__object_after or self.__object_node.get_before_wrap()):
            #     x -= pars.get_sp("node_width") // 2
            drawtext.DrawText().draw_singleline_text_rotated_by_hc_vt(
                get_painter_text_caption,
                nf.get(self.__to_right_physical_length)
                + pars.get_sp("постфикс_расстояния"),
                x,
                self.__y + pars.get_sp("node_caption_physics_vertical_padding"),
            )

        len_control_sectors = len(self.__control_sectors)
        if len_control_sectors > 0:
            total_len = 1 + (len_control_sectors - 1) * 2
            for index in range(total_len):
                cs = self.__control_sectors[index // 2]
                #
                is_last = index == total_len - 1
                #
                if index % 2 == 0:
                    # Сектор
                    draw_main_line(
                        cs.get("data_pars", {}).get("cs_lenght", {}).get("value", 0),
                        cs.get("data_pars", {}).get("cs_name", {}).get("value", ""),
                        cs.get("data_pars", {})
                        .get("cs_physical_length", {})
                        .get("value", 0),
                        index == 0,
                        index == total_len - 1,
                    )
                    # self.__x += (
                    #     cs.get("data_pars", {}).get("cs_lenght", {}).get("value", 0)
                    # )
                    self.__x = cs["x"]
                    self.__y = cs["y"]
                    self.__to_right_physical_length += (
                        cs.get("data_pars", {})
                        .get("cs_physical_length", {})
                        .get("value", 0)
                    )
                else:
                    # Контрольная точка
                    if cs.get("is_wrap", False) and not is_last:
                        draw_control_point(is_before_wrap=True)
                        # self.__x = self.__start_x + cs.get("data_pars", {}).get(
                        #     "cs_delta_wrap_x", {}
                        # ).get("value", 0)
                        # self.__y += self.__delta_wrap_y
                        self.__x = cs["wrap_x"]
                        self.__y = cs["wrap_y"]
                        draw_control_point(is_after_wrap=True)
                    else:
                        draw_control_point()

        else:
            draw_main_line(
                pars.get_sp("connection_length"),
                data.get_sd("название"),
                data.get_sd("физ_и_опт_длины", "фд"),
                True,
                True,
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
        before_half_width = 0
        after_half_width = 0
        #
        if self.__object_node_before.get_node_id() == "151":
            before_half_width = pars.get_bp("node_width") // 2
            before_padding = before_half_width
        elif self.__object_node_before.get_node_id() == "150":
            before_padding = pars.get_bp("node_radius")
        if self.__object_node_after.get_node_id() == "151":
            after_half_width = pars.get_ap("node_width") // 2
            after_padding = after_half_width
        elif self.__object_node_after.get_node_id() == "150":
            after_padding = pars.get_ap("node_radius")
        #
        center_x = (
            (self.__x + before_half_width)
            + (self.__x - after_half_width + pars.get_sp("connection_length"))
        ) // 2
        #
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_caption,
            nf.get(data.get_sd("физ_и_опт_длины", "од"))
            + pars.get_sp("постфикс_расстояния"),
            center_x,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
            pars.get_sp("connection_length") - before_padding - after_padding - 10,
        )

        # МЕТКИ
        # Получаем значение начальной метки (если пустое или не число - используем 0)
        start_metka_str = data.get_sd("нач_метка")
        try:
            start_metka_value = int(float(start_metka_str)) if start_metka_str else 0
        except (ValueError, TypeError):
            start_metka_value = 0

        start_metka = str(start_metka_value).zfill(4)

        # Получаем значение физической длины (если пустое или не число - используем 0)
        physical_length_str = data.get_sd("физ_и_опт_длины", "фд")
        try:
            physical_length = (
                int(float(physical_length_str)) if physical_length_str else 0
            )
        except (ValueError, TypeError):
            physical_length = 0

        # Вычисляем конечную метку (начальная + длина)
        end_metka_value = start_metka_value + physical_length
        end_metka = str(end_metka_value).zfill(4)

        # Формируем текст метки с учетом направления
        direction_metka = (
            data.get_sd("direction_metka") == "True"
        )  # сравнение с строкой True ибо это дата, а не параметр
        text_metki = (
            f"{end_metka}-{start_metka}"
            if direction_metka
            else f"{start_metka}-{end_metka}"
        )
        # print(f"BLABLA {direction_metka, text_metki}")

        # Рисуем текст метки и физическую длину
        drawtext.DrawText().draw_multiline_text_by_hc_vt(
            get_painter_text_caption,
            text_metki
            + "\n"
            + nf.get(data.get_sd("физ_и_опт_длины", "фд"))
            + pars.get_sp("постфикс_расстояния"),
            center_x,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
            pars.get_sp("connection_length") - before_padding - after_padding - 10,
        )
