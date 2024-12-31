from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext


class DrawConnection:
    def __init__(
        self, painter, object_connection, object_node_before, object_node_after, x, y
    ):
        self.__painter = painter
        self.__object_connection = object_connection
        self.__object_node_before = object_node_before
        self.__object_node_after = object_node_after
        self.__x = x
        self.__y = y
        #
        self.__metrics = self.__object_connection.get_metrics()
        self.__config_metrics = self.__object_connection.get_config_metrics()
        #
        self.__before_metrics = self.__object_node_before.get_metrics()
        self.__config_before_metrics = self.__object_node_before.get_config_metrics()
        #
        self.__after_metrics = self.__object_node_after.get_metrics()
        self.__config_after_metrics = self.__object_node_after.get_config_metrics()

    def draw(self):
        if self.__object_connection.get_connection_id() == "0":
            self.draw_connection_type_0()

    def draw_connection_type_0(self):
        """Скелетная схема ВОЛП и основные данные цепей кабеля"""
        # узнать значения
        length = self.__metrics.get(
            "length", self.__config_metrics.get("length", {})
        ).get("value", 0)
        left_right_margin = self.__metrics.get(
            "left_right_margin", self.__config_metrics.get("left_right_margin", {})
        ).get("value", 0)
        main_label_vertical_padding = self.__metrics.get(
            "main_label_vertical_padding",
            self.__config_metrics.get("main_label_vertical_padding", {}),
        ).get("value", 0)
        delta_node_and_thin_line = self.__metrics.get(
            "delta_node_and_thin_line",
            self.__config_before_metrics.get("delta_node_and_thin_line", {}),
        ).get("value", 0)
        delta_thins_lines = self.__metrics.get(
            "delta_thins_lines",
            self.__config_before_metrics.get("delta_thins_lines", {}),
        ).get("value", 0)
        thin_label_vertical_padding = self.__metrics.get(
            "thin_label_vertical_padding",
            self.__config_before_metrics.get("thin_label_vertical_padding", {}),
        ).get("value", 0)
        
        
        # метрики before и after
        before_margin_left_right = self.__before_metrics.get(
            "margin_left_right",
            self.__config_before_metrics.get("margin_left_right", {}),
        ).get("value", 0)
        after_margin_left_right = self.__after_metrics.get(
            "margin_left_right",
            self.__config_after_metrics.get("margin_left_right", {}),
        ).get("value", 0)


        # ОСНОВНАЯ ЛИНИЯ
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_bold_blue_line_painter()
        self.__painter.drawLine(self.__x, self.__y, self.__x + length, self.__y)

        # подписи к основной линии
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_main_caption_painter()

        # LT
        text = self.__object_connection.get_data().get("ВОК", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hl_vb(
            text,
            self.__x + left_right_margin + before_margin_left_right,
            self.__y - main_label_vertical_padding,
        )

        # LB
        text = (
            self.__object_connection.get_data()
            .get("количество_ОВ", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hl_vt(
            text,
            self.__x + left_right_margin + before_margin_left_right,
            self.__y + main_label_vertical_padding,
        )

        # RT
        text = (
            self.__object_connection.get_data()
            .get("физическая_длина", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hr_vb(
            text,
            self.__x + length - left_right_margin - after_margin_left_right,
            self.__y - main_label_vertical_padding,
        )

        # RB
        text = (
            self.__object_connection.get_data()
            .get("оптическая_длина", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hr_vt(
            text,
            self.__x + length - left_right_margin - after_margin_left_right,
            self.__y + main_label_vertical_padding,
        )

        # Сплошная тонкая линия (строительная_длина)
        # горизонтальная линия - название
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_painter()
        self.__painter.drawLine(
            self.__x - 5,
            self.__y + delta_node_and_thin_line,
            self.__x + length + 5,
            self.__y + delta_node_and_thin_line,
        )
        # горизонтальная линия - местоположение
        self.__painter.drawLine(
            self.__x - 5,
            self.__y + delta_node_and_thin_line + delta_thins_lines,
            self.__x + length + 5,
            self.__y + delta_node_and_thin_line + delta_thins_lines,
        )

        # Текст над/под с название и название_доп
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_caption_painter()
        #
        center_x = (self.__x + self.__x + length) // 2
        bottom_y = self.__y + delta_node_and_thin_line - thin_label_vertical_padding
        top_y = self.__y + delta_node_and_thin_line + thin_label_vertical_padding
        #
        text = self.__object_connection.get_data().get("название", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(text, center_x, bottom_y)
        #
        text = self.__object_connection.get_data().get("название_доп", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vt(text, center_x, top_y)

        # Текст над/под с местоположение и местоположение_доп
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_caption_painter()
        #
        center_x = (self.__x + self.__x + length) // 2
        bottom_y = self.__y + delta_node_and_thin_line + delta_thins_lines - thin_label_vertical_padding
        top_y = self.__y + delta_node_and_thin_line + delta_thins_lines + thin_label_vertical_padding
        #
        text = self.__object_connection.get_data().get("местоположение", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(text, center_x, bottom_y)
        #
        text = self.__object_connection.get_data().get("местоположение_доп", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vt(text, center_x, top_y)

