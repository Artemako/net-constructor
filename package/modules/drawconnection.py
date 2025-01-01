from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject


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
        self.__parameters = self.__object_connection.get_parameters()
        self.__config_parameters = self.__object_connection.get_config_parameters()
        #
        self.__before_parameters = self.__object_node_before.get_parameters()
        self.__config_before_parameters = self.__object_node_before.get_config_parameters()
        #
        self.__after_parameters = self.__object_node_after.get_parameters()
        self.__config_after_parameters = self.__object_node_after.get_config_parameters()

    def draw(self):
        if self.__object_connection.get_connection_id() == "0":
            self.draw_connection_type_0()

    def draw_connection_type_0(self):
        """Скелетная схема ВОЛП и основные данные цепей кабеля"""
        # узнать значения
        #region
        length = self.__parameters.get(
            "length", self.__config_parameters.get("length", {})
        ).get("value", 0)
        left_right_margin = self.__parameters.get(
            "left_right_margin", self.__config_parameters.get("left_right_margin", {})
        ).get("value", 0)
        main_label_vertical_padding = self.__parameters.get(
            "main_label_vertical_padding",
            self.__config_parameters.get("main_label_vertical_padding", {}),
        ).get("value", 0)
        delta_node_and_thin_line = self.__parameters.get(
            "delta_node_and_thin_line",
            self.__config_before_parameters.get("delta_node_and_thin_line", {}),
        ).get("value", 0)
        delta_thins_lines = self.__parameters.get(
            "delta_thins_lines",
            self.__config_before_parameters.get("delta_thins_lines", {}),
        ).get("value", 0)
        thin_label_vertical_padding = self.__parameters.get(
            "thin_label_vertical_padding",
            self.__config_before_parameters.get("thin_label_vertical_padding", {}),
        ).get("value", 0)
        arrow_width = self.__parameters.get(
            "arrow_width", self.__config_parameters.get("arrow_width", {})
        ).get("value", 0)
        arrow_height = self.__parameters.get(
            "arrow_height", self.__config_parameters.get("arrow_height", {})
        ).get("value", 0)
        
        # метрики before и after
        before_margin_left_right = self.__before_parameters.get(
            "margin_left_right",
            self.__config_before_parameters.get("margin_left_right", {}),
        ).get("value", 0)
        after_margin_left_right = self.__after_parameters.get(
            "margin_left_right",
            self.__config_after_parameters.get("margin_left_right", {}),
        ).get("value", 0)
        before_is_connected_with_thin_line_location = self.__before_parameters.get(
            "is_connected_with_thin_line_location",
            self.__config_before_parameters.get("is_connected_with_thin_line_location", {}),
        ).get("value", 0)
        after_is_connected_with_thin_line_location = self.__after_parameters.get(
            "is_connected_with_thin_line_location",
            self.__config_after_parameters.get("is_connected_with_thin_line_location", {}),
        ).get("value", 0)
        #endregion

        # ОСНОВНАЯ ЛИНИЯ
        #region
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_bold_blue_line_painter()
        self.__painter.drawLine(self.__x, self.__y, self.__x + length, self.__y)

        # подписи к основной линии
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_main_caption_painter()
        #endregion

        # LT и прочие
        #region
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
        #endregion
        
        # Сплошнык тонкие линии
        #region
        # (строительная_длина)
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
        # стрелки
        drawobject.DrawObject(self.__painter).arrow(
            self.__x + length, self.__y + delta_node_and_thin_line, arrow_width, arrow_height, "right"
        )
        drawobject.DrawObject(self.__painter).arrow(
            self.__x, self.__y + delta_node_and_thin_line, arrow_width, arrow_height, "left"
        )


        # горизонтальная линия - местоположение
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_painter()        
        self.__painter.drawLine(
            self.__x - 5,
            self.__y + delta_node_and_thin_line + delta_thins_lines,
            self.__x + length + 5,
            self.__y + delta_node_and_thin_line + delta_thins_lines,
        )
        # стрелки + проверка соседних узлов
        if before_is_connected_with_thin_line_location:
            drawobject.DrawObject(self.__painter).arrow(
            self.__x, self.__y + delta_node_and_thin_line + delta_thins_lines, arrow_width, arrow_height, "left"
        )
        if after_is_connected_with_thin_line_location:
            drawobject.DrawObject(self.__painter).arrow(
                self.__x + length, self.__y + delta_node_and_thin_line + delta_thins_lines, arrow_width, arrow_height, "right"
            )
        #endregion

        # Тексты над/под название и название_доп и местоположение и местоположение_доп
        #region
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

        #endregion