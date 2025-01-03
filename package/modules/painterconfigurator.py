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
        
    def get_figure_painter(self):
        self.painter.setPen(QPen(Qt.black, 2))
        self.painter.setBrush(QBrush(Qt.white))
        return self.painter

    def get_main_name_painter(self, pixel_size = 12):
        self.painter.setPen(QPen(Qt.black, 2))
        self.painter.setBrush(QBrush(Qt.NoBrush))
        font = QFont()
        font.setPixelSize(pixel_size)
        self.painter.setFont(font)
        return self.painter
    
    def get_bold_blue_line_painter(self):
        self.painter.setPen(QPen(Qt.blue, 4))
        return self.painter
    

    def get_main_caption_painter(self, pixel_size = 12):
        self.painter.setPen(QPen(Qt.darkGray, 2))
        self.painter.setBrush(QBrush(Qt.NoBrush))
        font = QFont()
        font.setPixelSize(pixel_size)
        self.painter.setFont(font)
        return self.painter

    def get_thin_line_painter(self):
        self.painter.setPen(QPen(Qt.black, 2))
        return self.painter
    
    def get_thin_line_caption_painter(self, pixel_size = 12):
        self.painter.setPen(QPen(Qt.black, 2))
        self.painter.setBrush(QBrush(Qt.NoBrush))
        font = QFont()
        font.setPixelSize(pixel_size)
        self.painter.setFont(font)
        return self.painter