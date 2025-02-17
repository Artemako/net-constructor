from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QImage
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.diagramdrawer as diagramdrawer


class ImageWidget(QWidget):
    """Класс виджета для отображения диаграммы."""

    def __init__(self, parent=None):
        self.__obsm = None
        super().__init__(parent)
        self.__image = None
        self.__zoom_level = 1.0
        self.__pan_offset = QPointF(0, 0)
        self.__last_mouse_position = QPoint()
        self.__panning_active = False
        self.__diagram_drawer = None

    def set_obsm(self, obsm):
        self.__obsm = obsm

    def run(self, data):
        """Инициализирует данные и создает изображение."""
        self.__diagram_drawer = diagramdrawer.DiagramDrawer(self.__obsm, data)
        self.__image = self.create_image(data)
        self.update()

    def save_image(self, file_name):
        self.__image.save(file_name, "PNG")

    def create_image(self, data):
        print("create_image")
        #
        width = int(data.get("image_parameters", {}).get("width", {}).get("value", 0))
        height = int(data.get("image_parameters", {}).get("height", {}).get("value", 0))
        #
        start_x = int(
            data.get("diagram_parameters", {}).get("start_x", {}).get("value", 0)
        )
        start_y = int(
            data.get("diagram_parameters", {}).get("start_y", {}).get("value", 0)
        )
        delta_wrap_y = int(
            data.get("diagram_parameters", {}).get("delta_wrap_y", {}).get("value", 0)
        )

        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        if self.__diagram_drawer:
            self.__diagram_drawer.draw(painter, start_x, start_y, delta_wrap_y)
        painter.end()

        return image

    def paintEvent(self, event):
        """Отвечает за отрисовку изображения на виджете."""
        if self.__image:
            widget_painter = QPainter(self)
            widget_painter.setRenderHint(QPainter.SmoothPixmapTransform)
            widget_painter.translate(self.__pan_offset)
            widget_painter.scale(self.__zoom_level, self.__zoom_level)
            widget_painter.drawImage(0, 0, self.__image)
            widget_painter.end()

    def mousePressEvent(self, event):
        """Обрабатывает нажатие мыши."""
        if event.button() == Qt.LeftButton:
            self.__panning_active = True
            self.__last_mouse_position = event.pos()

    def mouseMoveEvent(self, event):
        """Обрабатывает движение мыши."""
        if self.__panning_active:
            delta = event.pos() - self.__last_mouse_position
            self.__pan_offset += delta
            self.__last_mouse_position = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Обрабатывает отпускание кнопки мыши."""
        if event.button() == Qt.LeftButton:
            self.__panning_active = False

    def wheelEvent(self, event):
        """Обрабатывает прокрутку колесика мыши для зума."""
        cursor_position = event.position()
        cursor_point = (cursor_position - self.__pan_offset) / self.__zoom_level
        zoom_factor = 1.1 if event.angleDelta().y() > 0 else 1 / 1.1
        self.__zoom_level *= zoom_factor
        new_cursor_point = (cursor_position - self.__pan_offset) / self.__zoom_level
        self.__pan_offset += (new_cursor_point - cursor_point) * self.__zoom_level
        self.update()
