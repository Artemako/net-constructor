from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint, QRect

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext


class DrawObject:
    def __init__(self):
        self.__painter = None

    def node_gray_diagcross(
        self, painter_figure_border, painter_figure_border_fill, x, y, node_radius
    ):
        self.__painter = painter_figure_border()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)
        #
        self.__painter = painter_figure_border_fill()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)

    def node_big_circle_and_triangle(self, painter_figure_border, x, y, node_border_radius):
        # Рисуем круг и треугольник
        points = QPolygon(
            [
                QPoint(x, y - node_border_radius),
                QPoint(x - node_border_radius * 0.865, y + node_border_radius // 2),
                QPoint(x + node_border_radius * 0.865, y + node_border_radius // 2),
            ]
        )
        self.__painter = painter_figure_border()
        self.__painter.drawEllipse(
            QPoint(x, y), node_border_radius, node_border_radius
        )
        self.__painter.drawPolygon(points)

    def node_reactangle(self, painter_figure_border, painter_figure_border_fill, center_x, center_y, width, height):
        self.__painter = painter_figure_border()
        self.__painter.drawRect(QRect(center_x - width // 2, center_y - height // 2, width, height))
        #
        self.__painter = painter_figure_border_fill()
        self.__painter.drawRect(QRect(center_x - width // 2, center_y - height // 2, width, height))


    def arrow(self, painter_arrow, x, y, width, height, direction):
        # direction = "left", "right"
        self.__painter = painter_arrow()
        if direction == "right":
            points = QPolygon(
                [
                    QPoint(x - width, y + height // 2),
                    QPoint(x, y),
                    QPoint(x - width, y - height // 2),
                    QPoint(int(x - 0.8 * width), y),
                ]
            )
            self.__painter.drawPolygon(points)
        #
        elif direction == "left":
            points = QPolygon(
                [
                    QPoint(x + width, y + height // 2),
                    QPoint(x, y),
                    QPoint(x + width, y - height // 2),
                    QPoint(int(x + 0.8 * width), y),
                ]
            )
            self.__painter.drawPolygon(points)

    def wrap_arrow(
        self, painter_arrow, painter_line, x, y, width, height, length, type_wrap
    ):
        # only right direction
        if type_wrap == "before_wrap":
            # стрелка
            self.arrow(painter_arrow, x + length, y, width, height, "right")
            #
            self.__painter = painter_line()
            self.__painter.drawLine(QPoint(x, y), QPoint(x + length, y))

        elif type_wrap == "after_wrap":
            # стрелка
            self.arrow(painter_arrow, x, y, width, height, "right")
            # линия
            self.__painter = painter_line()
            self.__painter.drawLine(QPoint(x - length, y), QPoint(x, y))
