from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon, QColor
from PySide6.QtCore import Qt


class PainterConfigurator:
    def __init__(self, painter, pen=None, brush=None, font=None):
        self.__painter = painter

        self.__painter.setPen(pen if pen is not None else Qt.NoPen)
        self.__painter.setBrush(brush if brush is not None else Qt.NoBrush)
        self.__painter.setFont(font if font is not None else QFont())

    def get_painter(self):
        return self.__painter
        
    def get_painter_text(self, color, pixel_size):
        self.__painter.setPen(QPen(QColor(color), 2))
        font = QFont()
        font.setPixelSize(pixel_size)
        self.__painter.setFont(font)
        return self.__painter

    def get_painter_line(self, color, weight):
        self.__painter.setPen(QPen(QColor(color), weight))
        return self.__painter


    def get_painter_figure_border(self, pen_color, pen_weight):
        self.__painter.setPen(QPen(QColor(pen_color), pen_weight))
        self.__painter.setBrush(QBrush(Qt.white))
        return self.__painter
    
    def get_painter_figure_fill(self, fill_color, fill_pattern):
        self.__painter.setBrush(QBrush(QColor(fill_color), fill_pattern))
        return self.__painter

    def get_painter_figure_border_fill(self, pen_color, pen_weight, fill_color, fill_pattern):
        self.__painter.setPen(QPen(QColor(pen_color), pen_weight))
        self.__painter.setBrush(QBrush(QColor(fill_color), fill_pattern))
        return self.__painter



    # def get_main_name_painter(self, pixel_size = 12):
    #     self.painter.setPen(QPen(Qt.black, 2))
    #     self.painter.setBrush(QBrush(Qt.NoBrush))
    #     font = QFont()
    #     font.setPixelSize(pixel_size)
    #     self.painter.setFont(font)
    #     return self.painter
    
    # def get_bold_blue_line_painter(self):
    #     self.painter.setPen(QPen(Qt.blue, 4))
    #     return self.painter
    

    # def get_main_caption_painter(self, pixel_size = 12):
    #     self.painter.setPen(QPen(Qt.darkGray, 2))
    #     self.painter.setBrush(QBrush(Qt.NoBrush))
    #     font = QFont()
    #     font.setPixelSize(pixel_size)
    #     self.painter.setFont(font)
    #     return self.painter

    # def get_thin_line_painter(self):
    #     self.painter.setPen(QPen(Qt.black, 2))
    #     return self.painter
    
    # def get_thin_line_caption_painter(self, pixel_size = 12):
    #     self.painter.setPen(QPen(Qt.black, 2))
    #     self.painter.setBrush(QBrush(Qt.NoBrush))
    #     font = QFont()
    #     font.setPixelSize(pixel_size)
    #     self.painter.setFont(font)
    #     return self.painter