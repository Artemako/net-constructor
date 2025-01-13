from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon, QColor, QTextOption
from PySide6.QtCore import Qt

import package.constants as constants


class PainterConfigurator:
    def __init__(self, painter, pen=None, brush=None, font=None):
        self.__painter = painter
        #
        self.__fill_styles = constants.FillStyles()
        # self.__text_alignments = constants.TextAlignments()
        self.__line_styles = constants.LineStyles()

        #
        self.__painter.setPen(pen if pen is not None else Qt.NoPen)
        self.__painter.setBrush(brush if brush is not None else Qt.NoBrush)
        self.__painter.setFont(font if font is not None else QFont())

    def _get_fill_pattern(self, fill_pattern_name):
        return self.__fill_styles.get(fill_pattern_name, Qt.SolidPattern)

    def get_painter(self):
        return self.__painter

    def get_painter_text(self, color, font_name, pixel_size):
        self.__painter.setPen(QPen(QColor(color), 2))
        #
        font = QFont()
        if font_name:
            success = font.fromString(font_name)
            if not success:
                font = QFont()
        #
        if pixel_size > 0:
            font.setPixelSize(pixel_size)
        else:
            font.setPixelSize(12)
        #
        self.__painter.setFont(font)
        self.__painter.setRenderHint(QPainter.TextAntialiasing, True)
        return self.__painter

    def get_painter_line(self, color, weight, style_name):
        # self.__painter.setPen(QPen(QColor(color), weight))
        style = self.__line_styles.get(style_name, Qt.SolidLine)
        self.__painter.setPen(QPen(QColor(color), weight, style))
        return self.__painter

    def get_painter_figure_border(self, pen_color, pen_weight):
        self.__painter.setPen(QPen(QColor(pen_color), pen_weight))
        self.__painter.setBrush(QBrush(Qt.white))
        return self.__painter

    def get_painter_figure_fill(self, fill_color, fill_pattern_name):
        self.__painter.setBrush(
            QBrush(QColor(fill_color), self._get_fill_pattern(fill_pattern_name))
        )
        return self.__painter

    def get_painter_figure_border_fill(
        self, pen_color, pen_weight, fill_color, fill_pattern_name
    ):
        self.__painter.setPen(QPen(QColor(pen_color), pen_weight))
        self.__painter.setBrush(
            QBrush(QColor(fill_color), self._get_fill_pattern(fill_pattern_name))
        )
        return self.__painter
