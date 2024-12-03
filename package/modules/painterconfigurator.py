from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt


class PainterConfigurator:
    def __init__(self, painter, pen=None, brush=None, font=None):
        self.painter = painter

        self.painter.setPen(pen if pen is not None else Qt.NoPen)
        self.painter.setBrush(brush if brush is not None else Qt.NoBrush)
        self.painter.setFont(font if font is not None else QFont())

    def get_painter(self):
        return self.painter
        