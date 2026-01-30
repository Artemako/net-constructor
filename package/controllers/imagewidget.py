"""Виджет отображения диаграммы: масштаб, панорама, экспорт в изображение."""

import math

from PySide6.QtCore import QPoint, QPointF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QImage, QPainter
from PySide6.QtWidgets import QWidget

from package.modules import diagramdrawer
from package.modules.license import is_demo_mode

# Демо-режим: фиксированные размер и шаг надписей «демо» (количество зависит от размера изображения)
_DEMO_WATERMARK_FONT_PT = 36
_DEMO_WATERMARK_STEP_X = 100
_DEMO_WATERMARK_STEP_Y = 80


class ImageWidget(QWidget):
    """Виджет для отображения диаграммы с зумом и панорамой."""

    def __init__(self, parent=None) -> None:
        self.__obsm = None
        super().__init__(parent)
        self.__image = None
        self.__zoom_level = 1.0
        self.__pan_offset = QPointF(0, 0)
        self.__last_mouse_position = QPoint()
        self.__panning_active = False
        self.__diagram_drawer = None

    def set_obsm(self, obsm) -> None:
        """Устанавливает ссылку на менеджер объектов приложения."""
        self.__obsm = obsm

    def clear(self) -> None:
        """Очищает изображение и сбрасывает состояние виджета."""
        self.__image = None
        self.__diagram_drawer = None
        self.__zoom_level = 1.0
        self.__pan_offset = QPointF(0, 0)
        self.update()

    def run(self, data, is_new: bool = False) -> None:
        """Строит диаграмму по данным и при необходимости подгоняет по размеру виджета."""
        self.__diagram_drawer = diagramdrawer.DiagramDrawer(self.__obsm, data)
        self.__image = self.create_image(data)

        if is_new:
            self._fit_image_to_widget()
            if is_demo_mode():
                QTimer.singleShot(0, self._fit_image_to_widget)

        self.update()

    def _fit_image_to_widget(self) -> None:
        """Подгоняет масштаб и смещение по размеру виджета."""
        if self.__image is None:
            return
        widget_width = self.width()
        widget_height = self.height()
        image_width = self.__image.width()
        image_height = self.__image.height()

        if image_width > 0 and image_height > 0:
            # Вычисляем коэффициенты масштабирования
            zoom_x = widget_width / image_width
            zoom_y = widget_height / image_height

            # Минимальный коэффициент масштабирования, чтобы изображение полностью помещалось в виджете
            initial_zoom_level = min(zoom_x, zoom_y)

            # Находим ближайшую степень 1.1 к initial_zoom_level
            log_zoom = math.log(initial_zoom_level, 1.1)
            rounded_log_zoom = round(log_zoom)
            self.__zoom_level = 1.1**rounded_log_zoom

            # Центрируем изображение
            offset_x = (widget_width - image_width * self.__zoom_level) / 2
            offset_y = (widget_height - image_height * self.__zoom_level) / 2
            self.__pan_offset = QPointF(offset_x, offset_y)

    def save_image(self, file_name: str) -> None:
        """Сохраняет текущее изображение в PNG-файл."""
        self.__image.save(file_name, "PNG")

    def create_image(self, data):
        """Создаёт QImage диаграммы по данным проекта."""
        start_x = int(
            data.get("diagram_parameters", {}).get("indent_left", {}).get("value", 0)
        )
        start_y = int(
            data.get("diagram_parameters", {}).get("indent_top", {}).get("value", 0)
        )
        indent_right = int(
            data.get("diagram_parameters", {}).get("indent_right", {}).get("value", 0)
        )
        indent_bottom = int(
            data.get("diagram_parameters", {}).get("indent_bottom", {}).get("value", 0)
        )
        delta_wrap_y = int(
            data.get("diagram_parameters", {}).get("delta_wrap_y", {}).get("value", 0)
        )
        is_center = bool(
            data.get("diagram_parameters", {}).get("is_center", {}).get("value", False)
        )
        max_nodes_in_row = int(
            data.get("diagram_parameters", {}).get("max_nodes_in_row", {}).get("value", 0)
        )

        # начальная ширина и высота
        width = start_x + indent_right
        start_height = start_y + indent_bottom

        # временное изображение для расчета высоты
        temp_image = QImage(width, start_height, QImage.Format_ARGB32)
        temp_image.fill(Qt.white)
        #
        painter = QPainter(temp_image)
        # подготовка данных перед рисованием
        rows, calc_width = self.__diagram_drawer._preparation_draw(
            start_x, start_y, delta_wrap_y, indent_right, is_center, max_nodes_in_row
        )
        # Вычисляем итоговую высоту
        if rows.get_rows():
            amount_rows = len(rows.get_rows())
            calc_height = start_height + delta_wrap_y * (amount_rows - 1)
        else:
            calc_height = start_height
        painter.end()

        # Итоговое изображение с рассчитанной высотой
        image = QImage(calc_width, calc_height, QImage.Format_ARGB32)
        image.fill(Qt.white)
        # Рисуем диаграмму на итоговом изображении
        painter = QPainter(image)
        self.__diagram_drawer.draw(painter, start_x, delta_wrap_y)
        if is_demo_mode():
            self._draw_demo_watermarks(painter, calc_width, calc_height)
        painter.end()

        return image

    def _draw_demo_watermarks(self, painter, width, height):
        """Рисует полупрозрачные красные надписи «демо» на изображении схемы."""
        painter.save()
        color = QColor(255, 0, 0, 100)
        painter.setPen(color)
        font = QFont()
        font.setPointSize(_DEMO_WATERMARK_FONT_PT)
        painter.setFont(font)
        text = "демо"
        step_x = _DEMO_WATERMARK_STEP_X
        step_y = _DEMO_WATERMARK_STEP_Y
        y = 0
        while y < height + step_y:
            x = 0
            while x < width + step_x:
                painter.save()
                painter.translate(int(x), int(y))
                painter.rotate(45)
                painter.drawText(0, 0, text)
                painter.restore()
                x += step_x
            y += step_y
        painter.restore()

    def resizeEvent(self, event) -> None:
        """При изменении размера в демо-режиме подгоняем изображение по центру."""
        super().resizeEvent(event)
        if is_demo_mode() and self.__image is not None:
            self._fit_image_to_widget()
            self.update()

    def paintEvent(self, event) -> None:
        """Отрисовка изображения на виджете."""
        if self.__image:
            widget_painter = QPainter(self)
            widget_painter.setRenderHint(QPainter.SmoothPixmapTransform)
            widget_painter.translate(self.__pan_offset)
            widget_painter.scale(self.__zoom_level, self.__zoom_level)
            widget_painter.drawImage(0, 0, self.__image)
            widget_painter.end()

    def mousePressEvent(self, event) -> None:
        """Обработка нажатия мыши (начало панорамы)."""
        if event.button() == Qt.LeftButton:
            self.__panning_active = True
            self.__last_mouse_position = event.pos()

    def mouseMoveEvent(self, event) -> None:
        """Обработка движения мыши (панорама)."""
        if self.__panning_active:
            delta = event.pos() - self.__last_mouse_position
            self.__pan_offset += delta
            self.__last_mouse_position = event.pos()
            self.update()

    def mouseReleaseEvent(self, event) -> None:
        """Обработка отпускания кнопки мыши (конец панорамы)."""
        if event.button() == Qt.LeftButton:
            self.__panning_active = False

    def wheelEvent(self, event) -> None:
        """Обработка прокрутки колеса мыши (зум)."""
        cursor_position = event.position()
        cursor_point = (cursor_position - self.__pan_offset) / self.__zoom_level
        zoom_factor = 1.1 if event.angleDelta().y() > 0 else 1 / 1.1
        self.__zoom_level *= zoom_factor
        new_cursor_point = (cursor_position - self.__pan_offset) / self.__zoom_level
        self.__pan_offset += (new_cursor_point - cursor_point) * self.__zoom_level
        self.update()
