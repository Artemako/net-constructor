from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawdataparameters as drawdataparameters
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject


class DrawConnection:
    def __init__(
        self,
        painter,
        object_diagramm,
        object_connection,
        object_node_before,
        object_node_after,
        x,
        y,
    ):
        self.__painter = painter
        self.__object_diagramm = object_diagramm
        self.__object_connection = object_connection
        self.__object_node_before = object_node_before
        self.__object_node_after = object_node_after
        self.__x = x
        self.__y = y

    def draw(self):
        # Сначала выбор диграммы, а потом соединения
        pars = drawdataparameters.DrawParameters(
            self.__object_diagramm,
            self.__object_connection,
            self.__object_node_before,
            self.__object_node_after,
        )
        data = drawdataparameters.DrawData(self.__object_connection)
        if self.__object_diagramm.get_diagramm_type_id() == "0":
            if self.__object_connection.get_connection_id() == "0":
                self._draw_connection_type_0(pars, data)

    def _draw_connection_type_0(self, pars, data):
        """Скелетная схема ВОЛП и основные данные цепей кабеля"""
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
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_bold_blue_line_painter()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )

        # подписи к основной линии
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_main_caption_painter()
        # endregion

        # LT и прочие
        # в зависимости от типа вершины
        # region
        text = data.get_sd("ВОК")
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hl_vb(
            text,
            self.__x + before_delta_line_caption_and_node,
            self.__y - pars.get_sp("connection_main_label_vertical_padding"),
        )

        # LB
        text = data.get_sd("количество_ОВ")
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hl_vt(
            text,
            self.__x + before_delta_line_caption_and_node,
            self.__y + pars.get_sp("connection_main_label_vertical_padding"),
        )

        # RT
        text = data.get_sd("физическая_длина")
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hr_vb(
            text,
            self.__x
            + pars.get_sp("connection_length")
            - after_delta_line_caption_and_node,
            self.__y - pars.get_sp("connection_main_label_vertical_padding"),
        )

        # RB
        text = data.get_sd("оптическая_длина")
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hr_vt(
            text,
            self.__x
            + pars.get_sp("connection_length")
            - after_delta_line_caption_and_node,
            self.__y + pars.get_sp("connection_main_label_vertical_padding"),
        )
        # endregion

        # Сплошнык тонкие линии
        # region
        # (строительная_длина)
        # горизонтальная линия - название
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_painter()
        self.__painter.drawLine(
            self.__x - pars.get_sp("distance_thin_line_after_connection_x"),
            self.__y + pars.get_sp("delta_node_and_thin_line"),
            self.__x + pars.get_sp("connection_length") + pars.get_sp("distance_thin_line_after_connection_x"),
            self.__y + pars.get_sp("delta_node_and_thin_line"),
        )
        # стрелки
        drawobject.DrawObject(self.__painter).arrow(
            self.__x + pars.get_sp("connection_length"),
            self.__y + pars.get_sp("delta_node_and_thin_line"),
            pars.get_sp("connection_arrow_width"),
            pars.get_sp("connection_arrow_height"),
            "right",
        )
        drawobject.DrawObject(self.__painter).arrow(
            self.__x,
            self.__y + pars.get_sp("delta_node_and_thin_line"),
            pars.get_sp("connection_arrow_width"),
            pars.get_sp("connection_arrow_height"),
            "left",
        )

        # горизонтальная линия - местоположение
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_painter()
        self.__painter.drawLine(
            self.__x - pars.get_sp("distance_thin_line_after_connection_x"),
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            + pars.get_sp("delta_thins_lines"),
            self.__x + pars.get_sp("connection_length") + pars.get_sp("distance_thin_line_after_connection_x"),
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            + pars.get_sp("delta_thins_lines"),
        )
        # стрелки + проверка соседних узлов
        if pars.get_bp("node_is_connected_with_thin_line_location"):
            drawobject.DrawObject(self.__painter).arrow(
                self.__x,
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("delta_thins_lines"),
                pars.get_sp("connection_arrow_width"),
                pars.get_sp("connection_arrow_height"),
                "left",
            )
        if pars.get_ap("node_is_connected_with_thin_line_location"):
            drawobject.DrawObject(self.__painter).arrow(
                self.__x + pars.get_sp("connection_length"),
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("delta_thins_lines"),
                pars.get_sp("connection_arrow_width"),
                pars.get_sp("connection_arrow_height"),
                "right",
            )
        # endregion

        # Тексты над/под название и название_доп и местоположение и местоположение_доп
        # region
        # Текст над/под с название и название_доп
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_caption_painter()
        #
        center_x = (self.__x + self.__x + pars.get_sp("connection_length")) // 2
        bottom_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            - pars.get_sp("connection_thin_label_vertical_padding")
        )
        top_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            + pars.get_sp("connection_thin_label_vertical_padding")
        )
        #
        text = data.get_sd("название")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(
            text, center_x, bottom_y
        )
        #
        text = data.get_sd("название_доп")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vt(
            text, center_x, top_y
        )

        # Текст над/под с местоположение и местоположение_доп
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_caption_painter()
        #
        center_x = (self.__x + self.__x + pars.get_sp("connection_length")) // 2
        bottom_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            + pars.get_sp("delta_thins_lines")
            - pars.get_sp("connection_thin_label_vertical_padding")
        )
        top_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            + pars.get_sp("delta_thins_lines")
            + pars.get_sp("connection_thin_label_vertical_padding")
        )
        #
        text = data.get_sd("местоположение")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(
            text, center_x, bottom_y
        )
        #
        text = data.get_sd("местоположение_доп")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vt(
            text, center_x, top_y
        )

        # endregion
