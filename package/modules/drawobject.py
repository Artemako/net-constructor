from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext

class DrawObject:

    def __init__(self):
        self.__painter = None

    def node_gray_diagcross(self, painter_figure_border, painter_figure_border_fill, x, y, node_radius):

        self.__painter = painter_figure_border()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)
        #
        self.__painter = painter_figure_border_fill()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)
        
        

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
    