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
        self.__config_before_metrics = (
            self.__object_node_before.get_config_metrics()
        )
        #
        self.__after_metrics = self.__object_node_after.get_metrics()
        self.__config_after_metrics = self.__object_node_after.get_config_metrics()

    def draw(self):
        if self.__object_connection.get_connection_id() == "0":
            self.draw_connection_type_0()

    def draw_connection_type_0(self):
        # узнать значения
        length = self.__metrics.get(
            "length", self.__config_metrics.get("length", {})
        ).get("value", 0)
        left_right_margin = self.__metrics.get(
            "left_right_margin", self.__config_metrics.get("left_right_margin", {})
        ).get("value", 0)
        label_vertical_padding = self.__metrics.get(
            "label_vertical_padding",
            self.__config_metrics.get("label_vertical_padding", {}),
        ).get("value", 0)

        #
        before_margin_left_right = self.__before_metrics.get(
            "margin_left_right", self.__config_before_metrics.get("margin_left_right", {})
        ).get("value", 0)
        after_margin_left_right = self.__after_metrics.get(
            "margin_left_right", self.__config_after_metrics.get("margin_left_right", {})
        ).get("value", 0)
        

        # основная линия
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=QPen(Qt.blue, 4),
            brush=QBrush(Qt.NoBrush),
        ).get_painter()
        self.__painter.drawLine(self.__x, self.__y, self.__x + length, self.__y)

        # подписи к основной линии
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=QPen(Qt.darkGray, 2),
            brush=QBrush(Qt.NoBrush),
            font=QFont().setPixelSize(12),
        ).get_painter()

        # LT
        data_text = self.__object_connection.get_data().get("ВОК", {}).get("value", "")
        text = f"ВОК {data_text}"
        drawtext.DrawText(self.__painter).draw_lefted_by_left_single_line_text(
            text, self.__x + left_right_margin + before_margin_left_right, self.__y - label_vertical_padding
        )

        # LB
        data_text = (
            self.__object_connection.get_data()
            .get("количество_ОВ", {})
            .get("value", "")
        )
        text = f"кол-во ОВ - {data_text}"
        drawtext.DrawText(self.__painter).draw_lefted_by_left_single_line_text(
            text, self.__x + left_right_margin + before_margin_left_right, self.__y + label_vertical_padding + 8
        )

        # RT
        data_text = (
            self.__object_connection.get_data()
            .get("физическая_длина", {})
            .get("value", "")
        )
        text = f"физическая длина - {data_text}"
        drawtext.DrawText(self.__painter).draw_righted_by_right_single_line_text(
            text,
            self.__x + length - left_right_margin - after_margin_left_right,
            self.__y - label_vertical_padding,
        )

        # RB
        data_text = (
            self.__object_connection.get_data()
            .get("оптическая_длина", {})
            .get("value", "")
        )
        text = f"оптическая_длина - {data_text}"
        drawtext.DrawText(self.__painter).draw_righted_by_right_single_line_text(
            text,
            self.__x + length - left_right_margin - after_margin_left_right,
            self.__y + label_vertical_padding + 8,
        )
