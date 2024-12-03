from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt, QRectF, QPoint

import sys
import json

data_json = """
{
    "junctions": [
        {"id": "M-1", "description": "уст. муфта М-1 на уст. опоре №б/н 1 ПАО 'Мегафон'"},
        {"id": "M-2", "description": "уст. муфта М-2 на опоре ВЛ-10кВ №382"},
        {"id": "M-3", "description": "уст. муфта М-3 на опоре ВЛ-10кВ №383"},
        {"id": "M-4", "description": "уст. муфта М-4 в уст. колодце типа КОТ"}
    ],
    "cables": [
        {"start": "M-1", "end": "M-2", "physical_length": 1789, "optical_length": 1825, "type": "ОКСНМ-10-01-0,22-48-(7,0)", "fiber_count": 48},
        {"start": "M-2", "end": "M-3", "physical_length": 102, "optical_length": 104, "type": "ОКСНМ-10-01-0,22-48-(7,0)", "fiber_count": 48},
        {"start": "M-3", "end": "M-4", "physical_length": 379, "optical_length": 387, "type": "ОКСНМ-10-01-0,22-48-(7,0)", "fiber_count": 48}
    ]
}
"""

data = json.loads(data_json)

class CableDiagram(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setWindowTitle("Схема кабелей")
        self.resize(800, 300)
        self.scale_factor = 1.0
        self.x_offset = 0
        self.y_offset = 0
        self.setMouseTracking(True)
        self.last_mouse_pos = None

        self.save_button = QPushButton("Сохранить изображение", self)
        self.save_button.clicked.connect(self.save_image)
        self.save_button.move(10, 10)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_diagram(painter)
    
    def draw_diagram(self, painter):
        painter.translate(self.x_offset, self.y_offset)
        painter.scale(self.scale_factor, self.scale_factor)
        
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Constants for layout
        start_x = 50
        start_y = 150
        junction_radius = 20
        spacing = 200
        
        # Draw junctions
        junction_positions = {}
        for i, junction in enumerate(self.data['junctions']):
            x = start_x + i * spacing
            y = start_y
            junction_positions[junction['id']] = QPoint(x, y)
            
            # Draw junction as a circle
            painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
            painter.drawEllipse(QPoint(x, y), junction_radius, junction_radius)
            
            # Draw description
            painter.drawText(QRectF(x - 80, y - 60, 160, 50), Qt.AlignCenter, junction['description'])

        # Draw cables
        for cable in self.data['cables']:
            start_point = junction_positions[cable['start']]
            end_point = junction_positions[cable['end']]
            painter.setPen(QPen(Qt.blue, 3))
            painter.drawLine(start_point, end_point)

            # Draw physical and optical lengths
            mid_x = (start_point.x() + end_point.x()) / 2
            painter.setPen(QPen(Qt.black, 2))
            painter.drawText(mid_x - 30, start_y + 40, f"Физ. длина - {cable['physical_length']} м")
            painter.drawText(mid_x - 30, start_y + 60, f"Опт. длина - {cable['optical_length']} м")
            painter.drawText(mid_x - 30, start_y + 80, f"{cable['type']}")
    
    def wheelEvent(self, event: QWheelEvent):
        angle_delta = event.angleDelta().y()
        scale_factor = 1.1 if angle_delta > 0 else 0.9
        self.scale_factor *= scale_factor
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.x_offset += delta.x()
            self.y_offset += delta.y()
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None

    def save_image(self):
        # Calculate the size of the entire diagram
        spacing = 200
        junction_radius = 20
        width = spacing * (len(self.data['junctions']) - 1) + 2 * junction_radius + 100
        height = 300  # can be fixed depending on your vertical space needs
        
        # Create an image large enough to contain the entire diagram
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.white)
        painter = QPainter(image)

        # Render the entire diagram to the image
        self.draw_diagram(painter)
        
        painter.end()
        image.save("output_diagram.png", "PNG")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CableDiagram(data)
    window.show()
    sys.exit(app.exec())
