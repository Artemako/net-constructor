from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext

class DrawObject:

    def __init__(self, painter):
        self.__painter = painter

    def node_gray_diagcross(self, x, y, node_radius):
        fill_color = Qt.white
        hatch_color = Qt.gray

        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter, pen=QPen(Qt.black, 2), brush=QBrush(fill_color)
        ).get_painter()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)

        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=QPen(Qt.black, 2),
            brush=QBrush(hatch_color, Qt.DiagCrossPattern),
        ).get_painter()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)

        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=QPen(Qt.black, 2),
            brush=QBrush(Qt.NoBrush),
        ).get_painter()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)

    def arrow(self, x, y, width, height, direction):
        # direction = "left", "right"
        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=None,
            brush=QBrush(Qt.black),            
        ).get_painter()
        if direction == "right":
            points = QPolygon(
                [
                    QPoint(x - width, y + height // 2),
                    QPoint(x, y),
                    QPoint(x - width, y - height // 2),
                    QPoint(int(x - 0.8 * width), y),
                ]
            )
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
    