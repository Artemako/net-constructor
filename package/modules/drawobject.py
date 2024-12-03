from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext

class DrawObject:

    def __init__(self, painter):
        self.__painter = painter

    def node_gray_diagcross(self, x, y, radius):
        fill_color = Qt.white
        hatch_color = Qt.gray

        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter, pen=QPen(Qt.black, 2), brush=QBrush(fill_color)
        ).get_painter()
        self.__painter.drawEllipse(QPoint(x, y), radius, radius)

        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=QPen(Qt.black, 2),
            brush=QBrush(hatch_color, Qt.DiagCrossPattern),
        ).get_painter()
        self.__painter.drawEllipse(QPoint(x, y), radius, radius)

        self.__painter = painterconfigurator.PainterConfigurator(
            self.__painter,
            pen=QPen(Qt.black, 2),
            brush=QBrush(Qt.NoBrush),
        ).get_painter()
        self.__painter.drawEllipse(QPoint(x, y), radius, radius)


