from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QBrush
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

    def paintEvent(self, event):
        painter = QPainter(self)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CableDiagram(data)
    window.show()
    sys.exit(app.exec())
