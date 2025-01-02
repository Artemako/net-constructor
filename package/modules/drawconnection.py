from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject


class ConnectionParameters:
    def __init__(
        self,
        object_diagramm,
        object_connection,
        object_node_before=None,
        object_node_after=None,
    ):
        self.__object_diagramm = object_diagramm
        self.__object_connection = object_connection
        self.__object_node_before = object_node_before
        self.__object_node_after = object_node_after
        #
        self.__self_parameters = {}
        self.__node_before_parameters = {}
        self.__node_after_parameters = {}
        #
        new_dict_diagramm_parameters = self._get_dict(
            self.__object_diagramm.get_parameters(),
            self.__object_diagramm.get_config_parameters(),
        )
        self.__self_parameters = {
            **new_dict_diagramm_parameters,
            **self._get_dict(
                self.__object_connection.get_parameters(),
                self.__object_connection.get_config_parameters(),
            ),
        }
        #
        if self.__object_node_before:
            self.__node_before_parameters = {
                **new_dict_diagramm_parameters,
                **self._get_dict(
                    self.__object_node_before.get_parameters(),
                    self.__object_node_before.get_config_parameters(),
                ),
            }
        if self.__object_node_after:
            self.__node_after_parameters = {
                **new_dict_diagramm_parameters,
                **self._get_dict(
                    self.__object_node_after.get_parameters(),
                    self.__object_node_after.get_config_parameters(),
                ),
            }

    def _get_dict(self, parameters, config_parameters) -> dict:
        new_dict = {}
        # по конфигу
        for key, dict_value in config_parameters.items():
            new_dict[key] = dict_value.get("value", 0)
        # по файлу
        for key in config_parameters.keys():
            value = parameters.get(key, {}).get("value", 0)
            if value:
                new_dict[key] = value
        #
        return new_dict

    def get_sp_by_key(self, key):
        return self.__self_parameters.get(key, 0)

    def get_nbp_by_key(self, key):
        return self.__node_before_parameters.get(key, 0)

    def get_nap_by_key(self, key):
        return self.__node_after_parameters.get(key, 0)


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
        #

        #
        # self.__diagramm_parameters = self.__object_diagramm.get_parameters()
        # self.__config_diagramm_parameters = self.__object_diagramm.get_config_parameters()
        # #
        # self.__parameters = self.__object_connection.get_parameters()
        # self.__config_parameters = self.__object_connection.get_config_parameters()
        # #
        # self.__before_parameters = self.__object_node_before.get_parameters()
        # self.__config_before_parameters = self.__object_node_before.get_config_parameters()
        # #
        # self.__after_parameters = self.__object_node_after.get_parameters()
        # self.__config_after_parameters = self.__object_node_after.get_config_parameters()

    def draw(self):
        # Сначала выбор диграммы, а потом соединения
        if self.__object_diagramm.get_diagramm_type_id() == 0:
            if self.__object_connection.get_connection_id() == "0":
                pars = ConnectionParameters(
                    self.__object_diagramm,
                    self.__object_connection,
                    self.__object_node_before,
                    self.__object_node_after,
                )
                self._draw_connection_type_0(pars)

    def _draw_connection_type_0(self, pars):
        """Скелетная схема ВОЛП и основные данные цепей кабеля"""
        # region
        # pars.get_sp_by_key("connection_length") = self.__parameters.get(
        #     "pars.get_sp_by_key("connection_length")", self.__config_parameters.get("pars.get_sp_by_key("connection_length")", {})
        # ).get("value", 0)
        # pars.get_sp_by_key("connection_caption_margin_left_right") = self.__parameters.get(
        #     "pars.get_sp_by_key("connection_caption_margin_left_right")", self.__config_parameters.get("pars.get_sp_by_key("connection_caption_margin_left_right")", {})
        # ).get("value", 0)
        # pars.get_sp_by_key("connection_main_label_vertical_padding") = self.__parameters.get(
        #     "pars.get_sp_by_key("connection_main_label_vertical_padding")",
        #     self.__config_parameters.get("pars.get_sp_by_key("connection_main_label_vertical_padding")", {}),
        # ).get("value", 0)
        # pars.get_sp_by_key("connection_thin_label_vertical_padding") = self.__parameters.get(
        #     "pars.get_sp_by_key("connection_thin_label_vertical_padding")",
        #     self.__config_before_parameters.get("pars.get_sp_by_key("connection_thin_label_vertical_padding")", {}),
        # ).get("value", 0)
        # pars.get_sp_by_key("connection_arrow_width") = self.__parameters.get(
        #     "pars.get_sp_by_key("connection_arrow_width")", self.__config_parameters.get("pars.get_sp_by_key("connection_arrow_width")", {})
        # ).get("value", 0)
        # pars.get_sp_by_key("connection_arrow_height") = self.__parameters.get(
        #     "pars.get_sp_by_key("connection_arrow_height")", self.__config_parameters.get("pars.get_sp_by_key("connection_arrow_height")", {})
        # ).get("value", 0)

        # # метрики before и after
        # before_margin_left_right = self.__before_parameters.get(
        #     "margin_left_right",
        #     self.__config_before_parameters.get("margin_left_right", {}),
        # ).get("value", 0)
        # after_margin_left_right = self.__after_parameters.get(
        #     "margin_left_right",
        #     self.__config_after_parameters.get("margin_left_right", {}),
        # ).get("value", 0)
        # before_is_connected_with_thin_line_location = self.__before_parameters.get(
        #     "node_is_connected_with_thin_line_location",
        #     self.__config_before_parameters.get("node_is_connected_with_thin_line_location", {}),
        # ).get("value", 0)
        # after_is_connected_with_thin_line_location = self.__after_parameters.get(
        #     "node_is_connected_with_thin_line_location",
        #     self.__config_after_parameters.get("node_is_connected_with_thin_line_location", {}),
        # ).get("value", 0)
        # endregion

        # ОСНОВНАЯ ЛИНИЯ
        # region
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_bold_blue_line_painter()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp_by_key("connection_length"),
            self.__y,
        )

        # подписи к основной линии
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_main_caption_painter()
        # endregion

        # LT и прочие
        # region
        text = self.__object_connection.get_data().get("ВОК", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hl_vb(
            text,
            self.__x
            + pars.get_sp_by_key(
                "connection_caption_margin_left_right"
            ),  # + before_margin_left_right,
            self.__y - pars.get_sp_by_key("connection_main_label_vertical_padding"),
        )

        # LB
        text = (
            self.__object_connection.get_data()
            .get("количество_ОВ", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hl_vt(
            text,
            self.__x
            + pars.get_sp_by_key(
                "connection_caption_margin_left_right"
            ),  # + before_margin_left_right,
            self.__y + pars.get_sp_by_key("connection_main_label_vertical_padding"),
        )

        # RT
        text = (
            self.__object_connection.get_data()
            .get("физическая_длина", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hr_vb(
            text,
            self.__x
            + pars.get_sp_by_key("connection_length")
            - pars.get_sp_by_key(
                "connection_caption_margin_left_right"
            ),  # - after_margin_left_right,
            self.__y - pars.get_sp_by_key("connection_main_label_vertical_padding"),
        )

        # RB
        text = (
            self.__object_connection.get_data()
            .get("оптическая_длина", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_singleline_text_by_hr_vt(
            text,
            self.__x
            + pars.get_sp_by_key("connection_length")
            - pars.get_sp_by_key(
                "connection_caption_margin_left_right"
            ),  # - after_margin_left_right,
            self.__y + pars.get_sp_by_key("connection_main_label_vertical_padding"),
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
            self.__x - 5,
            self.__y + pars.get_sp_by_key("delta_node_and_thin_line"),
            self.__x + pars.get_sp_by_key("connection_length") + 5,
            self.__y + pars.get_sp_by_key("delta_node_and_thin_line"),
        )
        # стрелки
        drawobject.DrawObject(self.__painter).arrow(
            self.__x + pars.get_sp_by_key("connection_length"),
            self.__y + pars.get_sp_by_key("delta_node_and_thin_line"),
            pars.get_sp_by_key("connection_arrow_width"),
            pars.get_sp_by_key("connection_arrow_height"),
            "right",
        )
        drawobject.DrawObject(self.__painter).arrow(
            self.__x,
            self.__y + pars.get_sp_by_key("delta_node_and_thin_line"),
            pars.get_sp_by_key("connection_arrow_width"),
            pars.get_sp_by_key("connection_arrow_height"),
            "left",
        )

        # горизонтальная линия - местоположение
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_painter()
        self.__painter.drawLine(
            self.__x - 5,
            self.__y
            + pars.get_sp_by_key("delta_node_and_thin_line")
            + pars.get_sp_by_key("delta_thins_lines"),
            self.__x + pars.get_sp_by_key("connection_length") + 5,
            self.__y
            + pars.get_sp_by_key("delta_node_and_thin_line")
            + pars.get_sp_by_key("delta_thins_lines"),
        )
        # стрелки + проверка соседних узлов
        if pars.get_nbp_by_key("before_is_connected_with_thin_line_location"):
            drawobject.DrawObject(self.__painter).arrow(
                self.__x,
                self.__y
                + pars.get_sp_by_key("delta_node_and_thin_line")
                + pars.get_sp_by_key("delta_thins_lines"),
                pars.get_sp_by_key("connection_arrow_width"),
                pars.get_sp_by_key("connection_arrow_height"),
                "left",
            )
        if pars.get_nap_by_key("after_is_connected_with_thin_line_location"):
            drawobject.DrawObject(self.__painter).arrow(
                self.__x + pars.get_sp_by_key("connection_length"),
                self.__y
                + pars.get_sp_by_key("delta_node_and_thin_line")
                + pars.get_sp_by_key("delta_thins_lines"),
                pars.get_sp_by_key("connection_arrow_width"),
                pars.get_sp_by_key("connection_arrow_height"),
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
        center_x = (self.__x + self.__x + pars.get_sp_by_key("connection_length")) // 2
        bottom_y = (
            self.__y
            + pars.get_sp_by_key("delta_node_and_thin_line")
            - pars.get_sp_by_key("connection_thin_label_vertical_padding")
        )
        top_y = (
            self.__y
            + pars.get_sp_by_key("delta_node_and_thin_line")
            + pars.get_sp_by_key("connection_thin_label_vertical_padding")
        )
        #
        text = self.__object_connection.get_data().get("название", {}).get("value", "")
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(
            text, center_x, bottom_y
        )
        #
        text = (
            self.__object_connection.get_data().get("название_доп", {}).get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vt(
            text, center_x, top_y
        )

        # Текст над/под с местоположение и местоположение_доп
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter
        ).get_thin_line_caption_painter()
        #
        center_x = (self.__x + self.__x + pars.get_sp_by_key("connection_length")) // 2
        bottom_y = (
            self.__y
            + pars.get_sp_by_key("delta_node_and_thin_line")
            + pars.get_sp_by_key("delta_thins_lines")
            - pars.get_sp_by_key("connection_thin_label_vertical_padding")
        )
        top_y = (
            self.__y
            + pars.get_sp_by_key("delta_node_and_thin_line")
            + pars.get_sp_by_key("delta_thins_lines")
            + pars.get_sp_by_key("connection_thin_label_vertical_padding")
        )
        #
        text = (
            self.__object_connection.get_data()
            .get("местоположение", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vb(
            text, center_x, bottom_y
        )
        #
        text = (
            self.__object_connection.get_data()
            .get("местоположение_доп", {})
            .get("value", "")
        )
        drawtext.DrawText(self.__painter).draw_multiline_text_by_hc_vt(
            text, center_x, top_y
        )

        # endregion
