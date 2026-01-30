from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QImage, QColor
from PySide6.QtCore import Qt

class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image_width = 200
        self.image_height = 100

    def paintEvent(self, event):
        # Создаем изображение нужного размера
        image = QImage(self.image_width, self.image_height, QImage.Format_ARGB32)
        image.fill(Qt.white)  # Заполняем белым цветом или любым другим, который вам нужен
        
        # Создаем QPainter для изображения
        painter = QPainter(image)
        painter.setPen(QColor(255, 0, 0))  # Устанавливаем цвет пера, например, красный
        painter.drawRect(10, 10, 50, 50)   # Рисуем прямоугольник или другую фигуру
        
        # Заканчиваем рисование на изображении
        painter.end()
        
        # Создаем QPainter для виджета и рисуем изображение на виджете
        widget_painter = QPainter(self)
        widget_painter.drawImage(0, 0, image)

if __name__ == "__main__":
    app = QApplication([])
    widget = ImageWidget()
    widget.resize(300, 200)
    widget.show()
    app.exec()
