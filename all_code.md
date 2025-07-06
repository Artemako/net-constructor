### D:\projects\net-constructor\__init__.py
``python

``
### D:\projects\net-constructor\examples\example.py
``python
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

``
### D:\projects\net-constructor\examples\example_+.py
``python
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage
from PySide6.QtCore import Qt, QRectF, QPoint

import sys
import json

data_json = """
{
    "nodes": [
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
        self.image = self.create_image()

    def create_image(self):
        # Размер изображения по диаграмме
        spacing = 200
        junction_radius = 20
        width = spacing * (len(self.data['nodes']) - 1) + 2 * junction_radius
        height = 300

        # Создаем изображение и рисуем на нем диаграмму
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        self.draw_diagram(painter)
        painter.end()

        # Сохраняем изображение, если нужно
        image.save("output_diagram.png", "PNG")

        return image

    def paintEvent(self, event):
        # Рисуем изображение на виджете
        widget_painter = QPainter(self)
        widget_painter.drawImage(0, 0, self.image)

    def draw_diagram(self, painter):
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        start_x = 50
        start_y = 150
        junction_radius = 20
        spacing = 200

        junction_positions = {}
        for i, junction in enumerate(self.data['nodes']):
            x = start_x + i * spacing
            y = start_y
            junction_positions[junction['id']] = QPoint(x, y)

            painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
            painter.drawEllipse(QPoint(x, y), junction_radius, junction_radius)

            painter.drawText(QRectF(x - 80, y - 60, 160, 50), Qt.AlignCenter, junction['description'])

        for cable in self.data['cables']:
            start_point = junction_positions[cable['start']]
            end_point = junction_positions[cable['end']]
            painter.setPen(QPen(Qt.blue, 3))
            painter.drawLine(start_point, end_point)

            mid_x = (start_point.x() + end_point.x()) / 2
            painter.setPen(QPen(Qt.black, 2))
            painter.drawText(mid_x - 30, start_y + 40, f"Физ. длина - {cable['physical_length']} м")
            painter.drawText(mid_x - 30, start_y + 60, f"Опт. длина - {cable['optical_length']} м")
            painter.drawText(mid_x - 30, start_y + 80, f"{cable['type']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CableDiagram(data)
    window.resize(800, 300)
    window.show()
    sys.exit(app.exec())

``
### D:\projects\net-constructor\examples\example_qimage.py
``python
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

``
### D:\projects\net-constructor\examples\example_qpaintner.py
``python
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

``
### D:\projects\net-constructor\package\app.py
``python
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

import package.components.mainwindow as mainwindow

import package.modules.dirpathmanager as dirpathmanager
import package.modules.configs as configs
import package.modules.project as project

class ObjectsManager:
    """
    Мененджер объектов.
    """
    def __init__(self):
        self.obj_mw = None
        self.obj_dirpath = None
        self.obj_configs = None
        self.obj_project = None

    def initializing_objects(self):
        self.obj_dirpath = dirpathmanager.DirPathManager()
        self.obj_configs = configs.Configs()
        self.obj_project = project.Project()
   
class App:
    def __init__(self, current_directory):
        self.current_directory = current_directory
        #
        self.__obsm = ObjectsManager()
        self.__obsm.initializing_objects()
        #
        self.config_objects()
        self.start_app()

    def config_objects(self):
        self.__obsm.obj_dirpath.set_dir_app(self.current_directory)
        self.__obsm.obj_configs.load_configs(self.current_directory)


    def start_app(self):
        """
        Запуск фронта.
        """
        try:
            self.app = QApplication(sys.argv)
            # настройка шрифтов
            self.__font_main = QFontDatabase.addApplicationFont(
                ":/fonts/resources/fonts/OpenSans-VariableFont_wdth,wght.ttf"
            )
            self.__font_italic = QFontDatabase.addApplicationFont(
                ":/fonts/resources/fonts/OpenSans-Italic-VariableFont_wdth,wght.ttf"
            )
            # Получаем название шрифта
            try:
                font_families = QFontDatabase.applicationFontFamilies(self.__font_main)
                if font_families:
                    self.__size_font = 10
                    self.__custom_font = QFont(font_families[0], self.__size_font)
                    self.app.setFont(self.__custom_font)
            except Exception as e:
                print(f"Error: {e}")
            # создание окна
            self.window = mainwindow.MainWindow(self.__obsm)
            self.__obsm.obj_mw = self.window
            self.window.show()
            # sys.exit(self.app.exec())
            self.app.exec_()
        except Exception as e:
            print(f"Error: {e}")

``
### D:\projects\net-constructor\package\constants.py
``python
# constants.py

from PySide6.QtCore import Qt


class FillStyles:
    def __init__(self):
        self.__fill_styles = {
            "NoBrush": Qt.NoBrush,
            "SolidPattern": Qt.SolidPattern,
            "Dense1Pattern": Qt.Dense1Pattern,
            "Dense2Pattern": Qt.Dense2Pattern,
            "Dense3Pattern": Qt.Dense3Pattern,
            "Dense4Pattern": Qt.Dense4Pattern,
            "Dense5Pattern": Qt.Dense5Pattern,
            "Dense6Pattern": Qt.Dense6Pattern,
            "Dense7Pattern": Qt.Dense7Pattern,
            "HorPattern": Qt.HorPattern,
            "VerPattern": Qt.VerPattern,
            "CrossPattern": Qt.CrossPattern,
            "BDiagPattern": Qt.BDiagPattern,
            "FDiagPattern": Qt.FDiagPattern,
            "DiagCrossPattern": Qt.DiagCrossPattern,
            "LinearGradientPattern": Qt.LinearGradientPattern,
            "RadialGradientPattern": Qt.RadialGradientPattern,
            "ConicalGradientPattern": Qt.ConicalGradientPattern,
            "TexturePattern": Qt.TexturePattern,
        }
    
    def keys(self):
        return self.__fill_styles.keys()

    def get(self, fill_pattern_name, default):
        return self.__fill_styles.get(fill_pattern_name, default)
    
class TextAlignments:
    def __init__(self):
        self.__text_alignments = {
            "LeftAlign": Qt.AlignLeft,
            "CenterAlign": Qt.AlignCenter,
            "RightAlign": Qt.AlignRight
        }
    
    def keys(self):
        return self.__text_alignments.keys()

    def get(self, text_alignment_name, default):
        return self.__text_alignments.get(text_alignment_name, default)


class LineStyles:
    def __init__(self):
        self.__line_styles = {
            # "NoPen": Qt.NoPen,
            "SolidLine": Qt.SolidLine,
            "DashLine": Qt.DashLine,
            "DotLine": Qt.DotLine,
            "DashDotLine": Qt.DashDotLine,
            "DashDotDotLine": Qt.DashDotDotLine,
            # "CustomDashLine": Qt.CustomDashLine,
        }
    
    def keys(self):
        return self.__line_styles.keys()

    def get(self, line_style_name, default):
        return self.__line_styles.get(line_style_name, default)


class DiagramToDiagram:
    def __init__(self):
        self.__nodes_mapping = {
            "0": {
                "50": "0",
                "51": "1",
                "100": "0",
                "101": "1",
                "150": "0",
                "151": "1"
            },
            "50": {
                "0": "50",
                "1": "51",
                "100": "50",
                "101": "51",
                "150": "50",
                "151": "51"
            },
            "100": {
                "0": "100",
                "1": "101",
                "50": "100",
                "51": "101",
                "150": "100",
                "151": "101"
            },
            "150" : {
                "0": "150",
                "1": "151",
                "50": "150",
                "51": "151",
                "100": "150",
                "101": "151"
            }
        }
        self.__connections_mapping = {
            "0": {
                "50": "0",
                "100": "0",
                "150": "0"
            },
            "50": {
                "0": "50",
                "100": "50",
                "150": "50"
            },
            "100": {
                "0": "100",
                "50": "100",
                "150": "100"
            }, 
            "150": {
                "0": "150",
                "50": "150",
                "100": "150"
            }   
        }

    def get_new_type_id(self, new_diagram_type_id, object_type_id, is_node=False):
        mapping = self.__nodes_mapping if is_node else self.__connections_mapping
        return mapping.get(new_diagram_type_id, {}).get(object_type_id, None)

``
### D:\projects\net-constructor\package\__init__.py
``python

``
### D:\projects\net-constructor\package\components\changeorderdialog.py
``python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

class ChangeOrderDialog(QDialog):

    def __init__(self, objects, type_objects, parent=None):
        super(ChangeOrderDialog, self).__init__(parent)
        self.__objects = objects
        self.__type_objects = type_objects
        self.__data = []
        
        if self.__type_objects == "nodes":
            self.setWindowTitle("Изменение порядка вершин")
        elif self.__type_objects == "connections":
            self.setWindowTitle("Изменение порядка соединений")
        elif self.__type_objects == "control_sectors":
            self.setWindowTitle("Изменение порядка контрольных точек")
        
        self.layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)  
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)
        self._populate_list()
        
        self.up_button = QPushButton("Вверх")
        self.down_button = QPushButton("Вниз")
        self.up_button.clicked.connect(self._move_item_up)
        self.down_button.clicked.connect(self._move_item_down)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.up_button)
        button_layout.addWidget(self.down_button)

        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(button_layout)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Отмена")

        button_ok_cancel_layout = QHBoxLayout()
        button_ok_cancel_layout.addWidget(self.ok_button)
        button_ok_cancel_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_ok_cancel_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _populate_list(self):
        for index, obj in enumerate(self.__objects):
            item_name = ""
            if self.__type_objects == "nodes":
                obj_name = obj.get("data", {}).get("название", {}).get("value", "")
                item_name = f"{index + 1}) {obj_name}"
            elif self.__type_objects == "connections":
                obj_name = obj.get("data", {}).get("название", {}).get("value", "")
                item_name = f"{index + 1}) {obj_name}"
            elif self.__type_objects == "control_sectors":
                obj_name = obj.get("data_pars", {}).get("cs_name", {}).get("value", "")
                item_name = f"{index + 1}) {obj_name}"
            
            item = QListWidgetItem(item_name)
            item.setData(Qt.UserRole, obj)
            self.list_widget.addItem(item)

    def _move_item_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentItem(item)

    def _move_item_down(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1: 
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, item)
            self.list_widget.setCurrentItem(item)

    def _get_ordered_objects(self):
        ordered_objects = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            ordered_objects.append(item.data(Qt.UserRole))
        return ordered_objects

    def accept(self):
        self.__data = self._get_ordered_objects()
        super().accept()

    def get_data(self):
        return self.__data

``
### D:\projects\net-constructor\package\components\controlsectordeletedialog.py
``python
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QListWidgetItem,
)
from PySide6.QtCore import Qt


class ControlSectorDeleteDialog(QDialog):
    def __init__(self, control_sectors, parent=None):
        super(ControlSectorDeleteDialog, self).__init__(parent)
        self.setWindowTitle("Удаление контрольной точки")
        #
        layout = QVBoxLayout(self)
        #
        self.list_widget = QListWidget(self)
        for index, cs in enumerate(control_sectors):
            text = f"""{index + 1}) {cs.get("data_pars", {}).get("cs_name", {}).get("value", "")}"""
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, cs)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)
        #
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Отмена", self)
        #
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        #
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        #
        self.setLayout(layout)

    def get_selected_control_sector(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            return selected_item.data(Qt.UserRole)
        return None

``
### D:\projects\net-constructor\package\components\diagramtypeselectdialog.py
``python
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QLabel, QDialogButtonBox, QHBoxLayout, QListWidgetItem
)
# from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

import resources_rc

class DiagramTypeSelectDialog(QDialog):
    def __init__(self, global_diagrams, parent=None):
        self.__data = None

        super().__init__(parent)
        
        self.setWindowTitle("Выбор типа диаграммы")
        self.setFixedSize(900, 400)
        
        main_layout = QVBoxLayout(self)
        
        layout = QHBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(200)
        
        # self.image_label = QLabel()
        # self.image_label.setAlignment(Qt.AlignCenter)
        # self.image_label.setFixedSize(600, 300) 
        
        for key, elem in global_diagrams.items():
            name = elem.get("name", "")
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, elem)
            self.list_widget.addItem(item)
        
        # self.list_widget.currentItemChanged.connect(self.load_image)
        
        layout.addWidget(self.list_widget)
        # layout.addWidget(self.image_label)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        main_layout.addLayout(layout)
        main_layout.addWidget(button_box)

    # def load_image(self, current, previous):
    #     if current:
    #         type_id = current.data(Qt.UserRole).get("type_id", "")
    #         image_path = f":/diagram_previews/resources/diagram_previews/{type_id}.png"
    #         pixmap = QPixmap(image_path)
    #         self.image_label.setPixmap(pixmap.scaled(
    #             self.image_label.size(), 
    #             Qt.KeepAspectRatio, 
    #             Qt.SmoothTransformation
    #         ))

    def get_data(self):
        return self.__data
    
    def accept(self):
        self.__data = self.list_widget.currentItem().data(Qt.UserRole)
        super().accept()

``
### D:\projects\net-constructor\package\components\mainwindow.py
``python
# mainwindow.py
from PySide6.QtWidgets import (
    QMainWindow,
    QMenu,
    QDialog,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QPushButton,
    QHeaderView,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QFontComboBox,
    QMessageBox,
    QApplication,
    QToolButton,
    QStyle,
    QHBoxLayout,
)
from PySide6.QtGui import QIntValidator, QFont, QColor, QFontMetrics, QKeySequence, QAction
from PySide6.QtCore import Qt, QModelIndex, QLocale

import package.controllers.style as style
import package.controllers.imagewidget as imagewidget

import package.components.nodeconnectionselectdialog as nodeconnectionselectdialog
import package.components.nodeconnectiondeletedialog as nodeconnectiondeletedialog
import package.components.diagramtypeselectdialog as diagramtypeselectdialog
import package.components.changeorderdialog as changeorderdialog
import package.components.controlsectordeletedialog as controlsectordeletedialog

import package.ui.mainwindow_ui as mainwindow_ui

import package.constants as constants

import json
from functools import partial


class MainWindow(QMainWindow):
    def __init__(self, obsm):
        self.__obsm = obsm
        #
        self.__current_object = None
        self.__current_is_node = None
        #
        self.__general_diagram_parameters_widgets = {}
        #
        self.__editor_object_data_widgets = {}
        self.__editor_type_object_data_widgets = {}
        self.__editor_objects_data_widgets = {}
        self.__editor_object_parameters_widgets = {}
        self.__editor_type_object_parameters_widgets = {}
        self.__editor_objects_parameters_widgets = {}
        self.__control_data_parameters_widgets = {}
        #
        # self.__text_format = "NCE (пока json) files (*.json)"]
        self.__text_format = "NCE files (*.nce)"
        #
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        #
        self.ui.imagewidget.set_obsm(self.__obsm)
        # config
        self.config()

    def _tab_right_changed(self, index):
        # Скрываем вкладки
        if index in [0, 1]:
            self.ui.tabw_right.tabBar().setTabVisible(2, False)
        elif index == 2:
            self.ui.tabw_right.tabBar().setTabVisible(3, False)
            self._clear_error_messages()
            self._validate_connection(self.__current_object, show_errors=True)
            

    def config(self):
        # СТИЛЬ
        self.__obj_style = style.Style()
        self.__obj_style.set_style_for_widget_by_name(self)
        
        #
        self.resize(1366, 768)
        self.ui.centralwidget_splitter.setSizes([806, 560])
        # QAction Ctrl S или Enter
        self.ui.action_save.setShortcuts(
            [
                QKeySequence("Return"),  # Enter (Return)
                QKeySequence("Ctrl+S"),  # Ctrl + S
            ]
        )

        #
        self.ui.tabw_right.tabBar().setTabVisible(2, False)
        self.ui.tabw_right.tabBar().setTabVisible(3, False)
        self.ui.tabw_right.currentChanged.connect(self._tab_right_changed)

        # self.update_menu_recent_projects()
        #
        self.ui.btn_addnode.clicked.connect(self._add_node)
        self.ui.btn_movenodes.clicked.connect(self._move_nodes)
        # self.ui.btn_deletenode.clicked.connect(self._delete_node)
        #
        self.ui.btn_moveconnections.clicked.connect(self._move_connections)
        #
        self.ui.combox_type_diagram.currentIndexChanged.connect(
            self._change_type_diagram
        )
        #
        # создание нового файла
        self.ui.action_new.triggered.connect(self.create_file_nce)
        # октрытие файла
        self.ui.action_open.triggered.connect(self.open_file_nce)
        # сохранение текущих данных
        self.ui.action_save.triggered.connect(self._save_changes_to_file_nce)
        #
        self.ui.action_saveas.triggered.connect(self._save_as_file_nce)
        # экспорт в картинку
        self.ui.action_export_to_image.triggered.connect(self._export_to_image)
        # видимость параметров
        self.ui.action_parameters.triggered.connect(self._toggle_parameters_visibility)
        # смены темы
        self.ui.dark_action.triggered.connect(lambda: self._change_theme("dark"))
        self.ui.light_action.triggered.connect(lambda: self._change_theme("light"))

    def _change_theme(self, theme_name):
        self.__obj_style.set_style_for_widget_by_name(self, theme_name)
        # self.setStyleSheet(style)
        # QApplication.instance().setStyleSheet(style)


    def _start_qt_actions(self):
        self.ui.action_new.setEnabled(True)
        self.ui.action_open.setEnabled(True)
        self.ui.action_save.setEnabled(True)
        self.ui.action_saveas.setEnabled(True)
        self.ui.action_export_to_image.setEnabled(True)

    def _update_status_bar_with_project_name(self, file_name):
        if file_name:
            self.statusBar().showMessage(f"Текущий проект: {file_name}")
        else:
            self.statusBar().showMessage("Проект не открыт")

    def _toggle_parameters_visibility(self):
        if self.ui.tabw_right.currentIndex() == 2:
            obj = self.__current_object
            is_node = self.__current_is_node
            # Обновляем виджеты параметров
            self._create_editor_parameters_widgets_by_object(obj, is_node)
        elif self.ui.tabw_right.currentIndex() == 3:
            self._create_control_sector_widgets(self.__current_control_sector)
        else:
            project_data = self.__obsm.obj_project.get_data()
            self._reset_widgets_by_data(project_data)


    def create_file_nce(self):
        file_name, _ = QFileDialog.getSaveFileName(self, " ", "", self.__text_format)
        if file_name:
            global_diagrams = self.__obsm.obj_configs.get_config_diagrams()
            dialog = diagramtypeselectdialog.DiagramTypeSelectDialog(
                global_diagrams, self
            )
            result = dialog.exec()
            if result == QDialog.Accepted:
                diagram_data = dialog.get_data()
                #
                self.ui.tabw_right.setCurrentIndex(0)
                #
                control_sectors_config = (
                    self.__obsm.obj_configs.get_config_control_sectors()
                )
                #
                self.__obsm.obj_project.create_new_project(
                    diagram_data, control_sectors_config, file_name
                )
                #
                project_data = self.__obsm.obj_project.get_data()
                #
                self.ui.imagewidget.run(project_data, is_new=True)
                self._reset_widgets_by_data(project_data)
                self._start_qt_actions()
                #
                self._update_status_bar_with_project_name(file_name)

    def open_file_nce(self):
        file_name, _ = QFileDialog.getOpenFileName(self, " ", "", self.__text_format)
        if file_name:
            #
            self.ui.tabw_right.setCurrentIndex(0)
            #
            self.__obsm.obj_project.open_project(file_name)
            #
            project_data = self.__obsm.obj_project.get_data()
            #
            self.ui.imagewidget.run(project_data, is_new=True)
            self._reset_widgets_by_data(project_data)
            self._start_qt_actions()
            #
            self._update_status_bar_with_project_name(file_name)

    def _save_as_file_nce(self):
        if self.__obsm.obj_project.is_active():
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Сохранить как", "", self.__text_format
            )
            if file_name:
                self._save_changes_to_file_nce()
                self.__obsm.obj_project.save_as_project(file_name)
                #
                self._update_status_bar_with_project_name(file_name)

    def _save_changes_to_file_nce(self):
        if self.__obsm.obj_project.is_active():
            diagram_type_id = str()
            diagram_name = str()
            new_diagram_parameters = {}

            new_data = {}
            new_parameters = {}

            is_general_tab = False
            is_editor_tab = False
            is_control_sector_tab = False

            if self.ui.tabw_right.currentIndex() == 0:
                is_general_tab = True
                diagram_type_id = self.ui.combox_type_diagram.currentData().get(
                    "type_id", ""
                )
                diagram_name = self.ui.combox_type_diagram.currentData().get("name", "")
                new_diagram_parameters = self._get_new_data_or_parameters(
                    self.__general_diagram_parameters_widgets, is_parameters=True
                )

            elif self.ui.tabw_right.currentIndex() == 2:
                is_editor_tab = True
                # Объединить дата с 3x разных форм
                object_data_widgets = self._get_new_data_or_parameters(
                    self.__editor_object_data_widgets, is_parameters=False
                )
                type_object_data_widgets = self._get_new_data_or_parameters(
                    self.__editor_type_object_data_widgets, is_parameters=False
                )
                objects_data_widgets = self._get_new_data_or_parameters(
                    self.__editor_objects_data_widgets, is_parameters=False
                )
                new_data = {
                    **object_data_widgets,
                    **type_object_data_widgets,
                    **objects_data_widgets,
                }

                # Объединить параметры с 3x форм
                object_parameters_widgets = self._get_new_data_or_parameters(
                    self.__editor_object_parameters_widgets, is_parameters=True
                )
                type_object_parameters_widgets = self._get_new_data_or_parameters(
                    self.__editor_type_object_parameters_widgets, is_parameters=True
                )
                objects_parameters_widgets = self._get_new_data_or_parameters(
                    self.__editor_objects_parameters_widgets, is_parameters=True
                )
                new_parameters = {
                    **object_parameters_widgets,
                    **type_object_parameters_widgets,
                    **objects_parameters_widgets,
                }

            elif self.ui.tabw_right.currentIndex() == 3:
                is_control_sector_tab = True
                # Получаем новые значения из виджетов
                new_control_sector_parameters = self._get_new_data_or_parameters(
                    self.__control_data_parameters_widgets, is_parameters=True
                )
                print(
                    f"new_control_sector_parameters = {new_control_sector_parameters}"
                )
                # Обновляем данные контрольного сектора
                if self.__current_control_sector is not None:
                    print(
                        f"self.__current_control_sector = {self.__current_control_sector}"
                    )
                    for key, value in new_control_sector_parameters.items():
                        self.__current_control_sector["data_pars"][key]["value"] = (
                            value.get("value")
                        )

            if is_editor_tab or is_general_tab or is_control_sector_tab:
                config_nodes = self.__obsm.obj_configs.get_nodes()
                config_connections = self.__obsm.obj_configs.get_connections()

                self.__obsm.obj_project.save_project(
                    self.__current_object,
                    self.__current_is_node,
                    is_general_tab,
                    is_editor_tab,
                    config_nodes,
                    config_connections,
                    diagram_type_id,
                    diagram_name,
                    new_diagram_parameters,
                    new_data,
                    new_parameters,
                )

            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_widgets_by_data(project_data)

            # Проверка оптической и физической длины соединения
            self._clear_error_messages()
            if is_editor_tab:
                self._validate_connection(self.__current_object, show_errors=True)

            # Обновляем таблицу контрольных секторов если мы на вкладке редактирования соединения
            # или редактирования контрольного сектора
            current_tab = self.ui.tabw_right.currentIndex()
            if (current_tab == 2 and not self.__current_is_node) or current_tab == 3:
                control_sectors = self.__current_object.get("control_sectors", [])
                self._reset_table_control_sectors(control_sectors)

    def _export_to_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, " ", "", "PNG images (*.png)")
        if file_name:
            print(f"save_image to {file_name}")
            self.ui.imagewidget.save_image(file_name)

    def _set_layout_widgets_visibility(self, layout, visible):
        """Helper function to set visibility for all widgets in a layout"""
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().setVisible(visible)
            elif item.layout():
                self._set_layout_widgets_visibility(item.layout(), visible)

    def _get_new_data_or_parameters(self, dict_widgets, is_parameters=True):
        new_data_or_parameters = {}
        for key, pair in dict_widgets.items():
            widget_type = pair[0]
            widget = pair[1]
            if widget_type == "title":
                new_data_or_parameters[key] = {"value": "заголовок"}
            elif widget_type == "font_name":
                new_data_or_parameters[key] = {"value": widget.currentFont().toString()}
            elif widget_type == "color":
                new_data_or_parameters[key] = {"value": widget.text()}
            elif widget_type == "string_line":
                new_data_or_parameters[key] = {"value": widget.text()}
            elif (
                widget_type == "fill_style"
                or widget_type == "text_align"
                or widget_type == "line_style"
            ):
                new_data_or_parameters[key] = {"value": widget.currentText()}
            elif widget_type == "bool":
                new_data_or_parameters[key] = {"value": widget.isChecked()}
            elif (
                widget_type == "number_int_signed"
                or widget_type == "number_int"
                or widget_type == "number_float"
            ):
                new_data_or_parameters[key] = {"value": widget.value()}
            else:
                if is_parameters:
                    new_data_or_parameters[key] = {"value": widget.value()}
                else:
                    new_data_or_parameters[key] = {"value": widget.toPlainText()}

        return new_data_or_parameters

    def _add_node(self):
        if self.__obsm.obj_project.is_active():
            diagram_type_id = self.__obsm.obj_project.get_data().get(
                "diagram_type_id", ""
            )
            #
            config_diagram_nodes = (
                self.__obsm.obj_configs.get_config_diagram_nodes_by_type_id(
                    diagram_type_id
                )
            )
            config_diagram_connections = (
                self.__obsm.obj_configs.get_config_diagram_connections_by_type_id(
                    diagram_type_id
                )
            )
            #
            dialog = nodeconnectionselectdialog.NodeConnectSelectDialog(
                config_diagram_nodes, config_diagram_connections, self
            )
            if dialog.exec():
                key_dict_node_and_key_dict_connection = (
                    dialog.get_selected_key_dict_node_and_key_dict_connection()
                )
                self.__obsm.obj_project.add_pair(key_dict_node_and_key_dict_connection)
                #
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

                # Если добавляем соединение, обновляем таблицу секторов
                if not key_dict_node_and_key_dict_connection.get("node"):
                    connections = project_data.get("connections", [])
                    if connections:
                        self._edit_object(
                            connections[-1], len(connections), is_node=False
                        )

    def _move_nodes(self):
        if self.__obsm.obj_project.is_active():
            nodes = self.__obsm.obj_project.get_data().get("nodes", [])
            dialog = changeorderdialog.ChangeOrderDialog(nodes, "nodes", self)
            if dialog.exec():
                new_order_nodes = dialog.get_data()
                self.__obsm.obj_project.set_new_order_nodes(new_order_nodes)
                #
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

    def _move_connections(self):
        if self.__obsm.obj_project.is_active():
            connections = self.__obsm.obj_project.get_data().get("connections", [])
            dialog = changeorderdialog.ChangeOrderDialog(
                connections, "connections", self
            )
            if dialog.exec():
                new_order_connections = dialog.get_data()
                self.__obsm.obj_project.set_new_order_connections(new_order_connections)
                #
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

    # def _delete_node(self, node):
    #     if self.__obsm.obj_project.is_active():
    #         nodes = self.__obsm.obj_project.get_data().get("nodes", [])
    #         connections = self.__obsm.obj_project.get_data().get("connections", [])
    #         dialog = nodeconnectiondeletedialog.NodeConnectionDeleteDialog(
    #             nodes, connections, self
    #         )
    #         if dialog.exec():
    #             selected_data = dialog.get_selected_node_and_connection()
    #             node = selected_data.get("node")
    #             connection = selected_data.get("connection")
    #             self.__obsm.obj_project.delete_pair(node, connection)
    #             #
    #             project_data = self.__obsm.obj_project.get_data()
    #             self.ui.imagewidget.run(project_data)
    #             self._reset_widgets_by_data(project_data)

    def _delete_node_with_connection(self, node, side="left"):
        """Удаление узла с указанным соединением"""
        connections = self.__obsm.obj_project.get_data().get("connections", [])
        nodes = self.__obsm.obj_project.get_data().get("nodes", [])

        # Получаем порядок выбранного узла
        selected_node_order = node.get("order", 0)

        # Определяем соединение для удаления
        connection_to_delete = None
        if len(nodes) > 1:  # Если узлов больше одного
            if side == "left" and selected_node_order > 0:
                connection_to_delete = next(
                    (
                        con
                        for con in connections
                        if con.get("order", 0) == selected_node_order - 1
                    ),
                    None,
                )
            elif side == "right" and selected_node_order < len(connections):
                connection_to_delete = next(
                    (
                        con
                        for con in connections
                        if con.get("order", 0) == selected_node_order
                    ),
                    None,
                )
        else:
            # Если это последний оставшийся узел, то просто удаляем его без соединения
            connection_to_delete = None

        # Удаляем пару (узел и соединение)
        self.__obsm.obj_project.delete_pair(node, connection_to_delete)

        project_data = self.__obsm.obj_project.get_data()
        self.ui.imagewidget.run(project_data)
        self._reset_widgets_by_data(project_data)

    def _reset_combobox_type_diagram(self, diagram_type_id):
        print("reset_combobox_type_diagram():\n")
        print(f"diagram_type_id={diagram_type_id}\n")
        combox_widget = self.ui.combox_type_diagram
        combox_widget.blockSignals(True)
        combox_widget.clear()
        #
        index = 0
        global_diagrams = self.__obsm.obj_configs.get_config_diagrams()
        for key, elem in global_diagrams.items():
            print(f"key={key}, elem={elem}")
            name = elem.get("name", "")
            type_id = elem.get("type_id", "0")
            combox_widget.addItem(name, elem)
            if type_id == diagram_type_id:
                combox_widget.setCurrentIndex(index)
            index += 1
        combox_widget.blockSignals(False)
        #

    def _change_type_diagram(self, index):
        new_diagram = self.ui.combox_type_diagram.currentData()
        new_type_id = new_diagram.get("type_id", "0")
        current_type_id = self.__obsm.obj_project.get_data().get(
            "diagram_type_id", None
        )
        #
        if self.__obsm.obj_project.is_active() and new_type_id != current_type_id:
            config_nodes = self.__obsm.obj_configs.get_nodes()
            config_connections = self.__obsm.obj_configs.get_connections()
            self.__obsm.obj_project.change_type_diagram(
                new_diagram, config_nodes, config_connections
            )
            #
            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_widgets_by_data(project_data)

    def reset_tab_general(self, diagram_type_id, diagram_parameters):
        print("reset_tab_general")
        # очистка типа диаграммы
        self._reset_combobox_type_diagram(diagram_type_id)
        # Параметры диаграммы
        config_diagram_parameters = (
            self.__obsm.obj_configs.get_config_diagram_parameters_by_type_id(
                diagram_type_id
            )
        )
        flag = self._create_parameters_widgets(
            self.__general_diagram_parameters_widgets,
            self.ui.fl_diagram_parameters,
            config_diagram_parameters,
            diagram_parameters,
        )
        self.ui.label_diagram_parameters.setVisible(flag)
        self.ui.line_p_dia.setVisible(flag)

    def _save_and_restore_scroll_position(self, table_widget, reset_function):
        scroll_position = table_widget.verticalScrollBar().value()
        reset_function()
        table_widget.verticalScrollBar().setValue(scroll_position)

    def reset_tab_elements(self, nodes, connections):
        nodes = sorted(nodes, key=lambda node: node.get("order", 0))
        connections = sorted(
            connections, key=lambda connection: connection.get("order", 0)
        )
        self._reset_table_nodes(nodes)
        self._reset_table_connections(connections)

    def _reset_table_nodes(self, nodes):
        def reset_nodes():
            table_widget = self.ui.tablew_nodes
            table_widget.blockSignals(True)
            table_widget.clearContents()
            table_widget.setRowCount(len(nodes))
            #
            headers = ["№", "Название", "Редактировать"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.verticalHeader().setVisible(False)
            #
            for index, node in enumerate(nodes):
                node_id = node.get("node_id", "")
                # Получаем конфигурацию узла по его ID
                node_config = self.__obsm.obj_configs.get_node(node_id)
                tooltip = (
                    node_config.get("info", "Неизвестный узел")
                    if node_config
                    else "Неизвестный узел"
                )

                item_number = QTableWidgetItem(str(index + 1))
                item_number.setToolTip(tooltip)
                table_widget.setItem(index, 0, item_number)
                #
                node_name = node.get("data", {}).get("название", {}).get("value", "")
                item = QTableWidgetItem(node_name)
                item.setToolTip(tooltip)
                table_widget.setItem(index, 1, item)
                #
                # is_wrap = node.get("is_wrap", False)
                # btn_wrap = QPushButton("Не переносить" if is_wrap else "Переносить")
                # table_widget.setCellWidget(index, 2, btn_wrap)
                # btn_wrap.clicked.connect(partial(self._wrap_node, node))
                #
                btn_edit = QPushButton("Редактировать")
                table_widget.setCellWidget(index, 2, btn_edit)
                btn_edit.clicked.connect(
                    partial(self._edit_object, node, index + 1, is_node=True)
                )
            #
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            # header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            #
            table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
            # контекстное меню
            table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            table_widget.customContextMenuRequested.connect(
                self.node_table_context_menu
            )
            #
            table_widget.blockSignals(False)

        self._save_and_restore_scroll_position(self.ui.tablew_nodes, reset_nodes)

    def _reset_table_connections(self, connections):
        def reset_connections():
            print("reset_table_connections")
            table_widget = self.ui.tablew_connections
            table_widget.blockSignals(True)
            table_widget.clearContents()
            table_widget.setRowCount(len(connections))

            headers = ["№", "Начало – Конец", "Редактировать"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.verticalHeader().setVisible(False)

            nodes = self.__obsm.obj_project.get_data().get("nodes", [])

            for index, connection in enumerate(connections):
                # Проверяем соединение на ошибки
                has_errors = self._validate_connection(connection, show_errors=False)

                item_number = QTableWidgetItem(str(index + 1))
                table_widget.setItem(index, 0, item_number)

                node1_name = ""
                node2_name = ""
                if index < len(nodes):
                    node1_name = (
                        nodes[index]
                        .get("data", {})
                        .get("название", {})
                        .get("value", "")
                    )
                if index + 1 < len(nodes):
                    node2_name = (
                        nodes[index + 1]
                        .get("data", {})
                        .get("название", {})
                        .get("value", "")
                    )
                connection_name = f"{node1_name} – {node2_name}"
                item = QTableWidgetItem(connection_name)
                table_widget.setItem(index, 1, item)

                btn_edit = QPushButton("Редактировать")
                table_widget.setCellWidget(index, 2, btn_edit)
                btn_edit.clicked.connect(
                    partial(self._edit_object, connection, index + 1, is_node=False)
                )

                # Подсвечиваем строку, если есть ошибки
                if has_errors:
                    for col in range(table_widget.columnCount()):
                        item = table_widget.item(index, col)
                        if item:
                            item.setBackground(QColor("#661111"))
                            item.setForeground(Qt.white)

            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

            table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            table_widget.customContextMenuRequested.connect(
                self.connection_table_context_menu
            )
            table_widget.blockSignals(False)

        self._save_and_restore_scroll_position(
            self.ui.tablew_connections, reset_connections
        )

    def _update_physical_length_header(self, table_widget, comparison_result):
        """Обновление заголовка столбца физической длины"""
        header_item = QTableWidgetItem("Физ. длина")
        if comparison_result == 2:
            header_item.setText("Нет секторов")
            header_item.setForeground(Qt.gray)
        elif comparison_result == 1:
            header_item.setText("sum > физ. длина")
            header_item.setForeground(Qt.red)
        elif comparison_result == -1:
            header_item.setText("sum < физ. длина")
            header_item.setForeground(Qt.red)
        table_widget.setHorizontalHeaderItem(2, header_item)

    def _reset_table_control_sectors(self, control_sectors):
        def reset_control_sectors():
            print("reset_table_control_sectors")
            table_widget = self.ui.tw_control_sectors
            table_widget.blockSignals(True)
            table_widget.clearContents()
            table_widget.setRowCount(len(control_sectors))

            headers = ["№", "Название", "Физ. длина", "Редактировать"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            # Устанавливаем стандартный заголовок для столбца физической длины
            table_widget.setHorizontalHeaderItem(2, QTableWidgetItem("Физ. длина"))

            table_widget.verticalHeader().setVisible(False)

            for index, cs in enumerate(control_sectors):
                item_number = QTableWidgetItem(str(index + 1))
                table_widget.setItem(index, 0, item_number)

                cs_name = cs.get("data_pars", {}).get("cs_name", {}).get("value", "")
                item = QTableWidgetItem(cs_name)
                table_widget.setItem(index, 1, item)

                physical_length = (
                    cs.get("data_pars", {})
                    .get("cs_physical_length", {})
                    .get("value", 0)
                )
                item_length = QTableWidgetItem(str(physical_length))
                table_widget.setItem(index, 2, item_length)

                # if index < len(control_sectors) - 1:
                    # is_wrap = cs.get("is_wrap", False)
                    # btn_wrap = QPushButton("Не переносить" if is_wrap else "Переносить")
                    # table_widget.setCellWidget(index, 3, btn_wrap)
                    # btn_wrap.clicked.connect(partial(self._wrap_control_sector, cs))
                # else:
                #     empty_item = QTableWidgetItem("")
                #     empty_item.setFlags(empty_item.flags() & ~Qt.ItemIsEditable)
                #     table_widget.setItem(index, 3, empty_item)

                btn_edit = QPushButton("Редактировать")
                table_widget.setCellWidget(index, 3, btn_edit)
                btn_edit.clicked.connect(partial(self._edit_control_sector, cs))

            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            # header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
            # Контекстное меню
            table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            table_widget.customContextMenuRequested.connect(
                self.control_sector_table_context_menu
            )
            #
            table_widget.blockSignals(False)

        self._save_and_restore_scroll_position(
            self.ui.tw_control_sectors, reset_control_sectors
        )

    def _reset_widgets_by_data(self, data):
        #
        diagram_type_id = data.get("diagram_type_id", "")
        diagram_parameters = data.get("diagram_parameters", {})
        # Сепаратор для виджета
        precision_separator, precision_number = (
            self._get_precision_separator_and_number()
        )
        #
        self.reset_tab_general(diagram_type_id, diagram_parameters)
        #
        nodes = data.get("nodes", [])
        connections = data.get("connections", [])
        self.reset_tab_elements(nodes, connections)

    def _edit_object(self, obj, index, is_node=False):
        self.__current_object = obj
        self.__current_is_node = is_node
        #
        self.ui.tabw_right.tabBar().setTabVisible(2, True)
        self.ui.tabw_right.setCurrentIndex(2)
        #
        self._change_name_tab_editor(index, is_node)
        #
        self._create_editor_control_sectors_by_object(obj, is_node)
        #
        self._create_editor_data_widgets_by_object(obj, is_node)
        self._create_editor_parameters_widgets_by_object(obj, is_node)
        # Очищаем сообщения об ошибках
        self._clear_error_messages()
        self._validate_connection(self.__current_object, show_errors=True)

    def _validate_connection(self, connection, show_errors=False):
        has_errors = False

        # Получаем конфиг соединения
        connection_id = connection.get("connection_id", "0")
        connection_config = self.__obsm.obj_configs.get_connection(connection_id)

        # Проверяем, есть ли в конфиге параметры для оптической и физической длины
        has_optical_length = "оптическая_длина" in connection_config.get(
            "object_data", {}
        )
        has_physical_length = "физическая_длина" in connection_config.get(
            "object_data", {}
        )

        # Проверка оптической и физической длины (только если они есть в конфиге)
        if has_optical_length and has_physical_length:
            optical_length = (
                connection.get("data", {}).get("оптическая_длина", {}).get("value")
            )
            physical_length = (
                connection.get("data", {}).get("физическая_длина", {}).get("value")
            )

            if optical_length is not None and physical_length is not None:
                try:
                    if float(optical_length) < float(physical_length):
                        has_errors = True
                        if show_errors:
                            difference = float(physical_length) - float(optical_length)
                            self._add_error_message(
                                f"Опт. длина < физ. длина на {difference:.3f}"
                            )
                except (ValueError, TypeError):
                    pass

        # Проверка контрольных секторов (только если есть физическая длина в конфиге)
        if has_physical_length:
            control_sectors = connection.get("control_sectors", [])
            if control_sectors:
                total_physical_length = sum(
                    cs.get("data_pars", {})
                    .get("cs_physical_length", {})
                    .get("value", 0)
                    for cs in control_sectors
                )
                physical_length = (
                    connection.get("data", {})
                    .get("физическая_длина", {})
                    .get("value", 0)
                )
                try:
                    physical_length = (
                        float(physical_length) if physical_length is not None else 0
                    )
                    if abs(total_physical_length - physical_length) > 0.001:
                        has_errors = True
                        if show_errors:
                            if total_physical_length > physical_length:
                                difference = total_physical_length - physical_length
                                self._add_error_message(
                                    f"Сумма физ. длин секторов ({total_physical_length}) > "
                                    f"физ. длины соединения ({physical_length}) на {difference:.3f}"
                                )
                            else:
                                difference = physical_length - total_physical_length
                                self._add_error_message(
                                    f"Сумма физ. длин секторов ({total_physical_length}) < "
                                    f"физ. длины соединения ({physical_length}) на {difference:.3f}"
                                )
                except (ValueError, TypeError):
                    pass
            elif show_errors and not self.__current_is_node:
                self._add_error_message("Нет контрольных секторов.")

        return has_errors
    


    def _edit_control_sector(self, cs):
        self.__current_control_sector = cs
        self.ui.tabw_right.tabBar().setTabVisible(3, True)
        self.ui.tabw_right.setCurrentIndex(3)
        self.ui.tabw_right.setTabText(
            3, f"Редактирование контрольного сектора {cs.get('order', 0) + 1}"
        )
        #
        self._clear_form_layout(self.ui.fl_control)
        self._create_control_sector_widgets(cs)

    def _create_control_sector_widgets(self, cs):
        self._clear_form_layout(self.ui.fl_control)
        # получаем precision_separator и precision_number из параметров диаграммы
        precision_separator, precision_number = (
            self._get_precision_separator_and_number()
        )
        #
        self.__control_data_parameters_widgets = {}
        # Получить именно через config
        control_sectors_config = self.__obsm.obj_configs.get_config_control_sectors()
        # Создаем словарь параметров для текущего контрольного сектора
        cs_data_pars = cs.get("data_pars", {})

        # {
        #     "cs_name": {"value": cs.get("cs_name", "")},
        #     "cs_physical_length": {"value": cs.get("cs_physical_length", 0)},
        #     "cs_lenght": {"value": cs.get("cs_lenght", 0)},
        #     "cs_delta_wrap_x": {"value": cs.get("cs_delta_wrap_x", 0)}
        # }

        # Используем _create_parameters_widgets для создания виджетов
        self._create_parameters_widgets(
            self.__control_data_parameters_widgets,
            self.ui.fl_control,
            control_sectors_config,
            cs_data_pars,
            precision_separator,
            precision_number,
            combined_data_parameters=True,
        )

    # def _wrap_node(self, node):
    #     self.__obsm.obj_project.wrap_node(node)
    #     #
    #     project_data = self.__obsm.obj_project.get_data()
    #     self.ui.imagewidget.run(project_data)
    #     self._reset_widgets_by_data(project_data)

    def _wrap_control_sector(self, control_sector):
        control_sector["is_wrap"] = not control_sector.get("is_wrap", False)
        self._reset_table_control_sectors(
            self.__current_object.get("control_sectors", [])
        )
        #
        project_data = self.__obsm.obj_project.get_data()
        self.ui.imagewidget.run(project_data)
        self._reset_widgets_by_data(project_data)

    def _clear_form_layout(self, form_layout):
        while form_layout.count():
            child = form_layout.takeAt(0)
            if child.widget():
                # child.widget().setParent(None)
                child.widget().deleteLater()

    def _change_name_tab_editor(self, index, is_node=False):
        text_name = str()
        if is_node:
            text_name = f"Редактирование вершины {index}"
        elif not is_node:
            text_name = f"Редактирование соединения {index}"
        self.ui.tabw_right.setTabText(2, text_name)

    def _get_precision_separator_and_number(self):
        diagram_parameters = self.__obsm.obj_project.get_data().get(
            "diagram_parameters", {}
        )
        precision_separator = diagram_parameters.get("precision_separator", True)
        precision_number = diagram_parameters.get("precision_number", {}).get(
            "value", 2
        )
        return precision_separator, precision_number

    def create_data_widgets(
        self,
        dict_widgets,
        form_layout,
        config_object_data,
        object_data,
    ) -> bool:
        print(
            "create_data_widgets():\n"
            f"dict_widgets={dict_widgets}\n"
            f"form_layout={form_layout}\n"
            f"config_object_data={config_object_data}\n"
            f"object_data={object_data}\n"
        )
        dict_widgets.clear()
        self._clear_form_layout(form_layout)

        precision_separator, precision_number = (
            self._get_precision_separator_and_number()
        )

        for config_parameter_key, config_parameter_data in config_object_data.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            widget_type = config_parameter_data.get("type", "")
            info = config_parameter_data.get(
                "info", ""
            )  # Получаем информацию для подсказки
            #
            label_text = config_parameter_data.get("name", "")
            value = object_data.get(config_parameter_key, {}).get("value", None)
            value = (
                value if value is not None else config_parameter_data.get("value", "")
            )
            arguments = config_parameter_data.get("arguments", {})
            is_hide = config_parameter_data.get("is_hide", False)

            if is_hide:
                continue

            # Создаем метку для параметра
            label = self._get_label_name(label_text, widget_type)

            # Создаем основной виджет
            new_widget = self._get_widget(
                widget_type,
                value,
                arguments,
                is_parameters=False,
                precision_separator=precision_separator,
                precision_number=precision_number,
            )

            widget_to_add = self._create_widget_with_info(new_widget, info)
            form_layout.addRow(label, widget_to_add)

            dict_widgets[config_parameter_key] = [widget_type, new_widget]

        print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _get_widget(
        self,
        widget_type,
        value,
        arguments,
        is_parameters=True,
        precision_separator=None,
        precision_number=None,
    ):
        if widget_type == "title":
            new_widget = QLabel()
            new_widget.setStyleSheet("margin-bottom: 10px;")
        #
        elif widget_type == "bool":
            new_widget = QCheckBox()
            new_widget.setChecked(bool(value))
        #
        elif widget_type == "font_name":
            new_widget = QFontComboBox()
            font = QFont()
            if font.fromString(value):
                new_widget.setCurrentFont(font)
        #
        elif widget_type == "color":

            def open_color_dialog():
                color = QColorDialog.getColor()
                if color.isValid():
                    new_widget.setStyleSheet(f"background-color: {color.name()};")
                    new_widget.setText(color.name())

            new_widget = QPushButton()
            new_widget.setStyleSheet(f"background-color: {value};")
            new_widget.setText(value)
            new_widget.clicked.connect(open_color_dialog)
        #
        elif widget_type == "string_line":
            new_widget = QLineEdit()
            new_widget.setText(value)
        #
        elif widget_type == "fill_style":
            new_widget = QComboBox()
            fill_styles = constants.FillStyles()
            for style_name in fill_styles.keys():
                new_widget.addItem(style_name)
                if style_name == value:
                    new_widget.setCurrentText(style_name)
        #
        elif widget_type == "text_align":
            new_widget = QComboBox()
            text_alignments = constants.TextAlignments()
            for align_name in text_alignments.keys():
                new_widget.addItem(align_name)
                if align_name == value:
                    new_widget.setCurrentText(align_name)
        #
        elif widget_type == "line_style":
            new_widget = QComboBox()
            line_styles = constants.LineStyles()
            for style_name in line_styles.keys():
                new_widget.addItem(style_name)
                if style_name == value:
                    new_widget.setCurrentText(style_name)
        #
        elif widget_type == "number_int_signed":
            new_widget = QSpinBox()
            min_value = arguments.get("min", -2147483647)
            max_value = arguments.get("max", 2147483647)
            new_widget.setRange(min_value, max_value)
            new_widget.setValue(value)
        #
        elif widget_type == "number_int":
            new_widget = QSpinBox()
            min_value = arguments.get("min", 0)
            max_value = arguments.get("max", 2147483647)
            new_widget.setRange(min_value, max_value)
            new_widget.setValue(value)
        #
        elif widget_type == "number_float":
            new_widget = QDoubleSpinBox()
            new_widget.setRange(0, 2147483647)
            new_widget.setValue(value)
            if precision_separator is not None:
                new_widget.setDecimals(precision_number)
            if precision_separator == 0:
                locale = QLocale(QLocale.Russian)
            else:
                locale = QLocale(QLocale.C)
            new_widget.setLocale(locale)

        #
        else:
            if is_parameters:
                new_widget = QSpinBox()
                new_widget.setRange(0, 2147483647)
                new_widget.setValue(value)
            else:
                new_widget = QTextEdit()
                new_widget.setText(str(value))
                new_widget.setFixedHeight(40)

        # Отключение колесика мыши для всех виджетов, которые могут его использовать
        if isinstance(new_widget, (QSpinBox, QDoubleSpinBox, QComboBox)):

            def ignore_wheel_event(event):
                event.ignore()

            new_widget.wheelEvent = ignore_wheel_event

        return new_widget

    def _get_label_name(self, label_text, widget_type):
        label = QLabel(label_text)
        if widget_type == "title":
            label.setStyleSheet("font-styleF italic; font-weight: bold; ")
        return label

    def _create_parameters_widgets(
        self,
        dict_widgets,
        form_layout,
        config_object_parameters,
        object_parameters,
        precision_separator=None,
        precision_number=None,
        combined_data_parameters=False,
    ) -> bool:
        print(
            "create_parameters_widgets():\n"
            f"dict_widgets={dict_widgets}\n"
            f"form_layout={form_layout}\n"
            f"config_object_parameters={config_object_parameters}\n"
            f"object_parameters={object_parameters}\n"
        )
        dict_widgets.clear()
        self._clear_form_layout(form_layout)
        # Проверка на наличие параметров (стоит ли галочка)
        is_action_parameters = self.ui.action_parameters.isChecked()
        if combined_data_parameters or is_action_parameters:
            precision_separator, precision_number = (
                self._get_precision_separator_and_number()
            )
            for (
                config_parameter_key,
                config_parameter_data,
            ) in config_object_parameters.items():
                print(
                    f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
                )
                widget_type = config_parameter_data.get("type", "")
                label_text = config_parameter_data.get("name", "")
                info = config_parameter_data.get(
                    "info", ""
                )  # Получаем информацию для подсказки
                value = object_parameters.get(config_parameter_key, {}).get(
                    "value", None
                )
                value = (
                    value
                    if value is not None
                    else config_parameter_data.get("value", "")
                )
                arguments = config_parameter_data.get("arguments", {})
                is_hide = config_parameter_data.get("is_hide", False)

                if is_hide:
                    continue

                # Создаем метку для параметра
                label = self._get_label_name(label_text, widget_type)

                # Создаем основной виджет
                new_widget = self._get_widget(
                    widget_type,
                    value,
                    arguments,
                    is_parameters=True,
                    precision_separator=precision_separator,
                    precision_number=precision_number,
                )

                # Для секторов
                is_parameter = config_parameter_data.get("is_parameter", False)
                if (
                    combined_data_parameters
                    and not is_action_parameters
                    and is_parameter
                ):
                    continue

                widget_to_add = self._create_widget_with_info(new_widget, info)
                form_layout.addRow(label, widget_to_add)

                if widget_type != "title":
                    dict_widgets[config_parameter_key] = [widget_type, new_widget]

        # print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _add_control_sector(self, obj):
        control_sectors = self.__obsm.obj_project.add_control_sector(
            obj, penultimate=True
        )
        #
        project_data = self.__obsm.obj_project.get_data()
        self.ui.imagewidget.run(project_data)
        self._reset_table_control_sectors(control_sectors)

    def _move_control_sectors(self, obj):
        control_sectors = obj.get("control_sectors", [])
        dialog = changeorderdialog.ChangeOrderDialog(
            control_sectors, "control_sectors", self
        )
        if dialog.exec():
            new_order_control_sectors = dialog.get_data()
            control_sectors = self.__obsm.obj_project.set_new_order_control_sectors(
                obj, new_order_control_sectors
            )
            #
            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_table_control_sectors(control_sectors)

    def _delete_control_sector(self, obj, selected_cs):
        control_sectors = self.__obsm.obj_project.delete_control_sector(
            obj, selected_cs
        )
        #
        project_data = self.__obsm.obj_project.get_data()
        self.ui.imagewidget.run(project_data)
        self._reset_table_control_sectors(control_sectors)

    def _create_editor_control_sectors_by_object(self, obj, is_node=False):
        self.ui.label_control_sectors.setVisible(not is_node)
        self.ui.line_cont_sect.setVisible(not is_node)
        #
        self.ui.tw_control_sectors.setVisible(not is_node)
        self.ui.btn_add_control_sector.setVisible(not is_node)
        self.ui.btn_move_control_sectors.setVisible(not is_node)
        # отключаем старые обработчики
        try:
            self.ui.btn_add_control_sector.clicked.disconnect()
            self.ui.btn_move_control_sectors.clicked.disconnect()
        except:
            pass
        #
        self.ui.btn_add_control_sector.clicked.connect(
            partial(self._add_control_sector, obj)
        )
        self.ui.btn_move_control_sectors.clicked.connect(
            partial(self._move_control_sectors, obj)
        )
        #
        if not is_node:
            control_sectors = obj.get("control_sectors", [])
            self._reset_table_control_sectors(control_sectors)

    def _create_editor_parameters_widgets_by_object(self, obj, is_node=False):
        if is_node:
            config_object_parameters = (
                self.__obsm.obj_configs.get_config_node_parameters_by_node(obj)
            )
            config_type_object_parameters = (
                self.__obsm.obj_configs.get_config_type_node_parameters_by_node(obj)
            )
            config_objects_parameters = (
                self.__obsm.obj_configs.get_config_objects_parameters_by_node(obj)
            )
        elif not is_node:
            config_object_parameters = (
                self.__obsm.obj_configs.get_config_connection_parameters_by_connection(
                    obj
                )
            )
            config_type_object_parameters = self.__obsm.obj_configs.get_config_type_connection_parameters_by_connection(
                obj
            )
            config_objects_parameters = (
                self.__obsm.obj_configs.get_config_objects_parameters_by_connection(obj)
            )
        #
        object_parameters = obj.get("parameters", {})
        flag = self._create_parameters_widgets(
            self.__editor_object_parameters_widgets,
            self.ui.fl_object_parameters,
            config_object_parameters,
            object_parameters,
        )
        self.ui.label_object_parameters.setVisible(flag)
        self.ui.line_pars.setVisible(flag)
        #
        flag = self._create_parameters_widgets(
            self.__editor_type_object_parameters_widgets,
            self.ui.fl_type_object_parameters,
            config_type_object_parameters,
            object_parameters,
        )
        self.ui.label_type_object_parameters.setVisible(flag)
        self.ui.line_type_pars.setVisible(flag)
        #
        flag = self._create_parameters_widgets(
            self.__editor_objects_parameters_widgets,
            self.ui.fl_objects_parameters,
            config_objects_parameters,
            object_parameters,
        )
        self.ui.label_objects_parameters.setVisible(flag)
        self.ui.line_global_pars.setVisible(flag)

    def _create_editor_data_widgets_by_object(self, obj, is_node=False):
        if is_node:
            config_object_data = self.__obsm.obj_configs.get_config_node_data_by_node(
                obj
            )
            config_type_object_data = (
                self.__obsm.obj_configs.get_config_type_node_data_by_node(obj)
            )
            config_objects_data = (
                self.__obsm.obj_configs.get_config_objects_data_by_node(obj)
            )
        elif not is_node:
            config_object_data = (
                self.__obsm.obj_configs.get_config_connection_data_by_connection(obj)
            )
            config_type_object_data = (
                self.__obsm.obj_configs.get_config_type_connection_data_by_connection(
                    obj
                )
            )
            config_objects_data = (
                self.__obsm.obj_configs.get_config_objects_data_by_connection(obj)
            )
        # именно только data
        object_data = obj.get("data", {})
        flag = self.create_data_widgets(
            self.__editor_object_data_widgets,
            self.ui.fl_object_data,
            config_object_data,
            object_data,
        )
        self.ui.label_object_data.setVisible(flag)
        self.ui.line_data.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_type_object_data_widgets,
            self.ui.fl_type_object_data,
            config_type_object_data,
            object_data,
        )
        self.ui.label_type_object_data.setVisible(flag)
        self.ui.line_type_data.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_objects_data_widgets,
            self.ui.fl_objects_data,
            config_objects_data,
            object_data,
        )
        self.ui.label_objects_data.setVisible(flag)
        self.ui.line_global_data.setVisible(flag)

    def node_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы узлов"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.ui.tablew_nodes.currentRow()
        if selected_row < 0:
            return

        nodes = self.__obsm.obj_project.get_data().get("nodes", [])
        selected_node = nodes[selected_row]
        node_count = len(nodes)

        # Добавляем новые действия
        copy_data_action = menu.addAction("Копировать данные вершины")
        paste_data_action = menu.addAction("Вставить данные вершины")
        menu.addSeparator()

        delete_with_left_action = menu.addAction("Удалить с левым соединением")
        delete_with_right_action = menu.addAction("Удалить с правым соединением")

        # Логика активации/деактивации действий
        if node_count == 1:  # Если это единственный узел
            delete_with_left_action.setEnabled(True)
            delete_with_right_action.setEnabled(True)
        else:
            if selected_row == 0:  # Первый узел
                delete_with_left_action.setEnabled(False)
                delete_with_right_action.setEnabled(True)
            elif selected_row == node_count - 1:  # Последний узел
                delete_with_left_action.setEnabled(True)
                delete_with_right_action.setEnabled(False)
            else:  # Промежуточные узлы
                delete_with_left_action.setEnabled(True)
                delete_with_right_action.setEnabled(True)

        # Проверяем, есть ли что в буфере обмена для вставки
        paste_data_action.setEnabled(self.__obsm.obj_project.has_copied_node_data())

        # Отображаем меню
        action = menu.exec_(self.ui.tablew_nodes.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if selected_row >= 0 and selected_node:
            if action == copy_data_action:
                self.__obsm.obj_project.copy_node_data(selected_node)
            elif action == paste_data_action:
                self.__obsm.obj_project.paste_node_data(selected_node)
                # Обновляем интерфейс
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)
            elif action == delete_with_left_action:
                self._delete_node_with_connection(selected_node, "left")
            elif action == delete_with_right_action:
                self._delete_node_with_connection(selected_node, "right")

    def connection_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы соединений"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.ui.tablew_connections.currentRow()
        if selected_row < 0:
            return

        connections = self.__obsm.obj_project.get_data().get("connections", [])
        selected_connection = connections[selected_row]

        # Добавляем новые действия
        copy_data_action = menu.addAction("Копировать данные соединения")
        paste_data_action = menu.addAction("Вставить данные соединения")

        # Проверяем, есть ли что в буфере обмена для вставки
        paste_data_action.setEnabled(
            self.__obsm.obj_project.has_copied_connection_data()
        )

        # Отображаем меню
        action = menu.exec_(self.ui.tablew_connections.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if selected_row >= 0 and selected_connection:
            if action == copy_data_action:
                self.__obsm.obj_project.copy_connection_data(selected_connection)
            elif action == paste_data_action:
                self.__obsm.obj_project.paste_connection_data(selected_connection)
                # Обновляем интерфейс
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

    def control_sector_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы контрольных секторов"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.ui.tw_control_sectors.currentRow()
        if selected_row < 0:
            return

        obj = self.__current_object
        control_sectors = obj.get("control_sectors", [])
        selected_cs = control_sectors[selected_row]

        # Добавляем новые действия
        copy_data_action = menu.addAction("Копировать данные сектора")
        paste_data_action = menu.addAction("Вставить данные сектора")
        menu.addSeparator()
        delete_action = menu.addAction("Удалить контрольный сектор")

        # Проверяем, есть ли что в буфере обмена для вставки
        paste_data_action.setEnabled(
            self.__obsm.obj_project.has_copied_control_sector_data()
        )

        # Отображаем меню
        action = menu.exec_(self.ui.tw_control_sectors.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if action == copy_data_action and selected_cs:
            self.__obsm.obj_project.copy_control_sector_data(selected_cs)
        elif action == paste_data_action and selected_cs:
            self.__obsm.obj_project.paste_control_sector_data(selected_cs)
            # Обновляем интерфейс
            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_table_control_sectors(control_sectors)
        elif action == delete_action and selected_cs:
            self._delete_control_sector(obj, selected_cs)

    def _clear_error_messages(self):
        """
        Очищает все сообщения об ошибках из контейнера vl_edit_errors.
        """
        while self.ui.vl_edit_errors.count():
            item = self.ui.vl_edit_errors.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.ui.label_edit_errors.setVisible(False)
        self.ui.line_errors.setVisible(False)

    def _check_lengths(self, optical_length=None, physical_length=None):
        """
        Проверяет и добавляет сообщения об ошибках, связанных с оптической и физической длиной.
        """
        if (
            optical_length is not None
            and physical_length is not None
            and optical_length < physical_length
        ):
            difference = physical_length - optical_length
            error_message = f"Опт. длина < физ. длина на {difference:.3f}"
            self._add_error_message(error_message)

    def _check_sum_control_sectors(self, control_sectors):
        total_physical_length = sum(
            cs.get("data_pars", {}).get("cs_physical_length", {}).get("value", 0)
            for cs in control_sectors
        )
        connection_physical_length = (
            self.__current_object.get("data", {})
            .get("физическая_длина", {})
            .get("value", 0)
        )
        try:
            connection_physical_length = float(connection_physical_length)
        except (ValueError, TypeError):
            connection_physical_length = 0

        comparison_result, total_length, connection_length = None, None, None
        if abs(total_physical_length - connection_physical_length) <= 0.001:
            comparison_result, total_length, connection_length = (
                0,
                total_physical_length,
                connection_physical_length,
            )
        elif total_physical_length > connection_physical_length:
            comparison_result, total_length, connection_length = (
                1,
                total_physical_length,
                connection_physical_length,
            )
        else:
            comparison_result, total_length, connection_length = (
                -1,
                total_physical_length,
                connection_physical_length,
            )

        error_message = ""
        if comparison_result == 2:
            error_message = "Нет контрольных секторов."
        elif comparison_result == 1:
            difference = total_length - connection_length
            error_message = (
                f"Сумма физ. длин секторов ({total_length}) > физ. длины соединения ({connection_length}) на {difference:.3f}"
            )
        elif comparison_result == -1:
            difference = connection_length - total_length
            error_message = (
                f"Сумма физ. длин секторов ({total_length}) < физ. длины соединения ({connection_length}) на {difference:.3f}"
            )

        if error_message:
            self._add_error_message(error_message)

    def _add_error_message(self, message):
        self.ui.label_edit_errors.setVisible(True)
        self.ui.line_errors.setVisible(True)

        # Используем QLabel вместо QTextEdit
        error_label = QLabel()
        error_label.setText(message)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("color: #FFA500;")

        self.ui.vl_edit_errors.addWidget(error_label)

    def _show_info_dialog(self, info):
        """Отображает диалоговое окно с информацией."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Информация")
        msg_box.setText(info)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec()

    def _create_widget_with_info(self, widget, info, button_first=True):
        if info:
            tool_button = QToolButton()
            tool_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
            tool_button.setToolTip("Нажмите для получения информации")
            tool_button.clicked.connect(lambda: self._show_info_dialog(info))

            h_layout = QHBoxLayout()
            if button_first:
                h_layout.addWidget(tool_button)
                h_layout.addWidget(widget)
            else:
                h_layout.addWidget(widget)
                h_layout.addWidget(tool_button)
            return h_layout

        return widget

``
### D:\projects\net-constructor\package\components\nodeconnectiondeletedialog.py
``python
# # nodeconnectiondeletedialog.py

# from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox

# class NodeConnectionDeleteDialog(QDialog):
#     def __init__(self, nodes, connections, parent=None):
#         super(NodeConnectionDeleteDialog, self).__init__(parent)
#         self.setWindowTitle("Удаление узла и соединения")
        
#         self.__nodes = nodes
#         self.__connections = connections

#         # Выпадающий список для выбора узла
#         label_node = QLabel("Выберите узел")
#         self.combo_box_nodes = QComboBox(self)
#         for index, node in enumerate(self.__nodes):
#             node_name = node.get("data", {}).get("название", {}).get("value", "")
#             self.combo_box_nodes.addItem(f"{index + 1}) {node_name}", node)

#         # Выпадающий список для выбора соединения
#         label_connection = QLabel("Выберите соединение")
#         self.combo_box_connections = QComboBox(self)
#         self.update_connections()

#         # Кнопки подтверждения и отмены
#         self.ok_button = QPushButton("OK", self)
#         self.cancel_button = QPushButton("Отмена", self)

#         # Организация компоновки
#         button_layout = QHBoxLayout()
#         button_layout.addWidget(self.ok_button)
#         button_layout.addWidget(self.cancel_button)

#         layout = QVBoxLayout(self)
#         layout.addWidget(label_node)
#         layout.addWidget(self.combo_box_nodes)
#         layout.addWidget(label_connection)
#         layout.addWidget(self.combo_box_connections)
#         layout.addLayout(button_layout)

#         # Связывание событий
#         self.ok_button.clicked.connect(self.accept)
#         self.cancel_button.clicked.connect(self.reject)
#         self.combo_box_nodes.currentIndexChanged.connect(self.update_connections)

#     def update_connections(self):
#         self.combo_box_connections.clear()
#         selected_node = self.combo_box_nodes.currentData()
#         if not selected_node:
#             return

#         selected_node_order = selected_node.get("order", 0)
#         available_connections = [
#             con for con in self.__connections
#             if con.get("order", 0) in [selected_node_order - 1, selected_node_order]
#         ]
#         if not available_connections:
#             QMessageBox.warning(self, "Внимание", "Нет доступных соединений для выбранного узла.")
#             return
#         for con in available_connections:
#             prefix = ""
#             if con.get("order", 0) == selected_node_order - 1:
#                 prefix = "Левое)"
#             elif con.get("order", 0) == selected_node_order:
#                 prefix = "Правое)"
#             connection_name = con["data"].get("название", {}).get("value", "")
#             self.combo_box_connections.addItem(f"{prefix} {connection_name}", con)

#     def get_selected_node_and_connection(self):
#         return {
#             "node": self.combo_box_nodes.currentData(),
#             "connection": self.combo_box_connections.currentData()
#         }

# # 

``
### D:\projects\net-constructor\package\components\nodeconnectionselectdialog.py
``python
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpacerItem,
    QSizePolicy
)
from PySide6.QtCore import QSize

class NodeConnectSelectDialog(QDialog):
    def __init__(
        self, config_diagram_nodes, config_diagram_connections, parent=None
    ):
        super(NodeConnectSelectDialog, self).__init__(parent)
        self.setWindowTitle("Выберите узел и соединение")
        self.config_diagram_nodes = config_diagram_nodes
        
        # Узел
        label_node = QLabel("Узел")
        self.combo_box_nodes = QComboBox(self)
        self.combo_box_nodes.currentIndexChanged.connect(self._update_node_fields)
        
        # Название узла
        label_node_name = QLabel("Название")
        self.line_edit_node_name = QLineEdit()
        
        # Местоположение узла
        self.label_node_place = QLabel("Местоположение") 
        self.line_edit_node_place = QLineEdit()
        
        # Соединение
        label_connection = QLabel("Соединение")
        self.combo_box_connections = QComboBox(self)
        
        # Кнопки
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Отмена", self)

        # Заполняем комбобокс узлов
        self._populate_nodes()
        
        # Заполняем комбобокс соединений
        self._populate_connections(config_diagram_connections)

        # Настройка layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        # Вертикальная пружина для прижатия содержимого вверх
        vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self)
        layout.addWidget(label_node)
        layout.addWidget(self.combo_box_nodes)
        layout.addWidget(label_node_name)
        layout.addWidget(self.line_edit_node_name)
        layout.addWidget(self.label_node_place)
        layout.addWidget(self.line_edit_node_place)
        layout.addWidget(label_connection)
        layout.addWidget(self.combo_box_connections)
        layout.addLayout(button_layout)
        layout.addItem(vertical_spacer)  # Добавляем пружину в конец

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self._update_node_fields()

    def _populate_nodes(self):
        """Заполняет комбобокс узлами"""
        self.combo_box_nodes.clear()
        for node_key, node_dict in self.config_diagram_nodes.items():
            node_name = node_dict.get("object_data", {}).get("название", {}).get("value", "")
            self.combo_box_nodes.addItem(
                node_name, ({"node_key": node_key, "node_dict": node_dict})
            )

    def _populate_connections(self, config_diagram_connections):
        """Заполняет комбобокс соединениями"""
        self.combo_box_connections.clear()
        for connection_key, connection_dict in config_diagram_connections.items():
            connection_name = (
                connection_dict.get("object_data", {}).get("название", {}).get("value", "")
            )
            self.combo_box_connections.addItem(
                connection_name,
                (
                    {
                        "connection_key": connection_key,
                        "connection_dict": connection_dict,
                    }
                ),
            )

    def _update_node_fields(self):
        """Обновляет поля узла при изменении выбора"""
        current_data = self.combo_box_nodes.currentData()
        if current_data:
            node_dict = current_data["node_dict"]
            object_data = node_dict.get("object_data", {})
            
            # Обновляем название
            node_name = object_data.get("название", {}).get("value", "")
            self.line_edit_node_name.setText(node_name)
            
            # Проверяем наличие поля "местоположение" в object_data (независимо от значения)
            has_place_field = "местоположение" in object_data
            self.label_node_place.setVisible(has_place_field)
            self.line_edit_node_place.setVisible(has_place_field)
            
            # Если поле есть - заполняем его текущим значением
            if has_place_field:
                node_place = object_data["местоположение"].get("value", "")
                self.line_edit_node_place.setText(node_place)
            
            # Подстраиваем размер окна
            self.adjustSize()

    def get_selected_key_dict_node_and_key_dict_connection(self):
        node_data = self.combo_box_nodes.currentData()
        node_dict = node_data["node_dict"].copy()
        object_data = node_dict.get("object_data", {}).copy()
        
        # Обновляем название
        node_name = self.line_edit_node_name.text()
        if "название" in object_data or node_name:
            if "название" not in object_data:
                object_data["название"] = {"value": node_name}
            else:
                object_data["название"]["value"] = node_name
        
        # Обновляем местоположение, если поле существует (независимо от видимости)
        if "местоположение" in object_data:
            node_place = self.line_edit_node_place.text()
            object_data["местоположение"]["value"] = node_place
        
        node_dict["object_data"] = object_data
        
        return {
            "node": {
                "node_key": node_data["node_key"],
                "node_dict": node_dict
            },
            "connection": self.combo_box_connections.currentData()
        }
``
### D:\projects\net-constructor\package\components\__init__.py
``python

``
### D:\projects\net-constructor\package\components\__pycache__\__init__.py
``python

``
### D:\projects\net-constructor\package\controllers\imagewidget.py
``python
# imagewidget.py

import math

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

    def run(self, data, is_new=False):
        self.__diagram_drawer = diagramdrawer.DiagramDrawer(self.__obsm, data)
        self.__image = self.create_image(data)

        if is_new:
            self._fit_image_to_widget()

        self.update()

    def _fit_image_to_widget(self):
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

    def save_image(self, file_name):
        self.__image.save(file_name, "PNG")

    def create_image(self, data):
        print("create_image")
        #
        # width = int(data.get("diagram_parameters", {}).get("width", {}).get("value", 0))
        # start_height = int(data.get("diagram_parameters", {}).get("start_height", {}).get("value", 0))
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

``
### D:\projects\net-constructor\package\controllers\style.py
``python
class Style:

    def __init__(self):
        self.__themes = {
            "dark": qss,
            "light": lqss 
        }
        self.__current_theme = "dark" 
        # Иконки по темам
        self.__icon_sets = {
            "dark": "white-icons",  
            "light": "black-icons"  
        }

    def set_style_for_widget_by_name(self, widget, theme_name = "dark"):
        widget.setStyleSheet(self.__themes.get(theme_name))



qss = """
/*!*************************************
    VS15 Dark
****************************************
    Author: chintsu_kun, holt59, MO2 Team
    Version: 2.5.0
    Licence: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)
    Source: https://github.com/nikolay-borzov/modorganizer-themes
****************************************
*/

/* For some reason applying background-color or border fixes paddings properties */
QListWidget::item {
    border-width: 0;
}

/* Don't override install label on download widget.
     MO2 assigns color depending on download state */
#installLabel {
    color: none;
}

/* Make `background-color` work for :hover, :focus and :pressed states */
QToolButton {
    border: none;
}

* {
    font-family: Open Sans;
}

/* Main Window */
QWidget {
    background-color: #2d2d30;
    color: #f1f1f1;
}

QWidget::disabled {
    color: #656565;
}

/* Common */
/* remove outline */
* {
    outline: 0;
}

*:disabled,
QListView::item:disabled,
*::item:selected:disabled {
    color: #656565;
}

/* line heights */
/* QTreeView#fileTree::item - currently have problem with size column vertical
     text align */
#bsaList::item,
#dataTree::item,
#modList::item,
#categoriesTree::item,
#savegameList::item,
#tabConflicts QTreeWidget::item {
    padding: 0.3em 0;
}

QListView::item,
QTreeView#espList::item {
    /*
    padding: 0.3em 0;
    */
}
QListView#lw_pages_template::item {
    padding: 0.2em 0;
}

/* to enable border color */
QTreeView,
QListView,
QTextEdit,
QWebView,
QTableView {
    border-style: solid;
    border-width: 1px;
}

QAbstractItemView {
    color: #dcdcdc;
    background-color: #1e1e1e;
    alternate-background-color: #262626;
    border-color: #3f3f46;
}

QAbstractItemView::item:selected,
QAbstractItemView::item:selected:hover,
QAbstractItemView::item:alternate:selected,
QAbstractItemView::item:alternate:selected:hover {
    color: #f1f1f1;
    background-color: #3399ff;
}

QAbstractItemView[filtered=true] {
    border: 2px solid #f00 !important;
}

QAbstractItemView,
QListView,
QTreeView {
    show-decoration-selected: 1;
}

QAbstractItemView::item:hover,
QAbstractItemView::item:alternate:hover,
QAbstractItemView::item:disabled:hover,
QAbstractItemView::item:alternate:disabled:hover QListView::item:hover,
QTreeView::branch:hover,
QTreeWidget::item:hover {
    background-color: rgba(51, 153, 255, 0.3);
}

QAbstractItemView::item:selected:disabled,
QAbstractItemView::item:alternate:selected:disabled,
QListView::item:selected:disabled,
QTreeView::branch:selected:disabled,
QTreeWidget::item:selected:disabled {
    background-color: rgba(51, 153, 255, 0.3);
}

QTreeView::branch:selected,
#bsaList::branch:selected {
    background-color: #3399ff;
}

QLabel {
    background-color: transparent;
}

LinkLabel {
    qproperty-linkColor: #3399ff;
}

/* Left Pane & File Trees #QTreeView, #QListView*/
QTreeView::branch:closed:has-children {
    image: url(:/png/resources/png/branch-closed.png);
}

QTreeView::branch:open:has-children {
    image: url(:/png/resources/png/branch-open.png);
}

QListView::item {
    color: #f1f1f1;
}

/* Text areas and text fields #QTextEdit, #QLineEdit, #QWebView */
QTextEdit,
QWebView,
QLineEdit,
QAbstractSpinBox,
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button,
QComboBox {
    background-color: #333337;
    border-color: #3f3f46;
}

QLineEdit:hover,
QAbstractSpinBox:hover,
QTextEdit:hover,
QComboBox:hover,
QComboBox:editable:hover {
    border-color: #007acc;
}

QLineEdit:focus,
QAbstractSpinBox::focus,
QTextEdit:focus,
QComboBox:focus,
QComboBox:editable:focus,
QComboBox:on {
    background-color: #3f3f46;
    border-color: #3399ff;
}

QComboBox:on {
    border-bottom-color: #3f3f46;
}

QLineEdit,
QAbstractSpinBox {
    min-height: 15px;
    padding: 2px;
    border-style: solid;
    border-width: 1px;
}

QLineEdit {
    margin-top: 0;
}

/* clear button */
QLineEdit QToolButton,
QLineEdit QToolButton:hover {
    background: none;
    margin-top: 1px;
}

QLineEdit#espFilterEdit QToolButton {
    margin-top: -2px;
    margin-bottom: 1px;
}

/* Drop-downs #QComboBox*/
QComboBox {
    min-height: 20px;
    padding-left: 5px;
    margin: 3px 0 1px 0;
    border-style: solid;
    border-width: 1px;
}

QComboBox:editable {
    padding-left: 3px;
    /* to enable hover styles */
    background-color: transparent;
}

QComboBox::drop-down {
    width: 20px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border: none;
}

QComboBox::down-arrow {
    image: url(:/png/resources/png/combobox-down.png);
}

QComboBox QAbstractItemView {
    background-color: #1b1b1c;
    selection-background-color: #3f3f46;
    border-color: #3399ff;
    border-style: solid;
    border-width: 0 1px 1px 1px;
}

/* Doesn't work http://stackoverflow.com/questions/13308341/qcombobox-abstractitemviewitem */
/* QComboBox QAbstractItemView:item {
    padding: 10px;
    margin: 10px;
} */
/* Toolbar */
QToolBar {
    border: none;
}

QToolBar::separator {
    border-left-color: #222222;
    border-right-color: #46464a;
    border-width: 0 1px 0 1px;
    border-style: solid;
    width: 0;
}

QToolButton {
    padding: 4px;
}

QToolButton:hover, QToolButton:focus {
    background-color: #3e3e40;
}

QToolButton:pressed {
    background-color: #3399ff;
}

QToolButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-top: 10%;
    padding-right: 5%;
}

/* Group Boxes #QGroupBox */
QGroupBox {
    border-color: #3f3f46;
    border-style: solid;
    border-width: 1px;
    /*
    padding: 1em 0.3em 0.3em 0.3em;
    margin-top: 0.65em;
    */
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px;
    left: 10px;
}

/* LCD Count */
QLCDNumber {
    border-color: #3f3f46;
    border-style: solid;
    border-width: 1px;
}

/* Buttons #QPushButton */
QPushButton {
    background-color: #333337;
    border-color: #3f3f46;
    min-height: 18px;
    padding: 2px 5px;
    border-style: solid;
    border-width: 1px;
}

QPushButton:hover,
QPushButton:checked,
QAbstractSpinBox::up-button:hover,
QAbstractSpinBox::down-button:hover {
    background-color: #007acc;
}

QPushButton:focus {
    border-color: #007acc;
}

QPushButton:pressed,
QPushButton:checked:hover,
QAbstractSpinBox::up-button:pressed,
QAbstractSpinBox::down-button:pressed {
    background-color: #1c97ea;
}

QPushButton:disabled,
QAbstractSpinBox::up-button:disabled,
QAbstractSpinBox::down-button:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}

QPushButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 5%;
}

/* Dialog buttons */
QSlider::handle:horizontal,
QSlider::handle:vertical {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}

QSlider::handle:horizontal:hover,
QSlider::handle:vertical:hover,
QSlider::handle:horizontal:pressed,
QSlider::handle:horizontal:focus:pressed,
QSlider::handle:vertical:pressed,
QSlider::handle:vertical:focus:pressed {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}

QSlider::handle:horizontal:focus,
QSlider::handle:vertical:focus {
    background-color: #dddddd;
    border-color: #3399ff;
}


QSlider::handle:horizontal:disabled,
QSlider::handle:vertical:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}


/* Check boxes and Radio buttons common #QCheckBox, #QRadioButton */
QListView::indicator,
QGroupBox::indicator,
QTreeView::indicator,
QCheckBox::indicator,
QRadioButton::indicator {
    background-color: #2d2d30;
    border-color: #3f3f46;
    width: 13px;
    height: 13px;
    border-style: solid;
    border-width: 1px;
}
QListView::indicator:hover,
QGroupBox::indicator:hover,
QTreeView::indicator:hover,
QCheckBox::indicator:hover,
QRadioButton::indicator:hover {
    background-color: #3f3f46;
    border-color: #007acc;
}
QListView::indicator:checked,
QGroupBox::indicator:checked,
QTreeView::indicator:checked,
QCheckBox::indicator:checked {
    image: url(:/png/resources/png/checkbox-check.png);
}
QListView::indicator:checked:disabled,
QGroupBox::indicator:disabled,
QTreeView::indicator:checked:disabled,
QCheckBox::indicator:checked:disabled {
    image: url(:/png/resources/png/checkbox-check-disabled.png);
}

/* Check boxes special */
QTreeView#modList::indicator {
    width: 15px;
    height: 15px;
}

/* Radio buttons #QRadioButton */
QRadioButton::indicator {
    border-node_radius: 7px;
}

QRadioButton::indicator::checked {
    background-color: #B9B9BA;
    border-width: 2px;
    width: 11px;
    height: 11px;
}

QRadioButton::indicator::checked:hover {
    border-color: #3f3f46;
}

/* Spinners #QSpinBox, #QDoubleSpinBox */
QAbstractSpinBox {
    margin: 1px;
}

QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button {
    border-style: solid;
    border-width: 1px;
    subcontrol-origin: padding;
}

QAbstractSpinBox::up-button {
    subcontrol-position: top right;
}

QAbstractSpinBox::up-arrow {
    image: url(:/png/resources/png/spinner-up.png);
}

QAbstractSpinBox::down-button {
    subcontrol-position: bottom right;
}

QAbstractSpinBox::down-arrow {
    image: url(:/png/resources/png/spinner-down.png);
}

/* Sliders #QSlider */
QSlider::groove:horizontal {
    background-color: #3f3f46;
    border: none;
    height: 8px;
    margin: 2px 0;
}

QSlider::handle:horizontal {
    width: 0.5em;
    height: 2em;
    margin: -7px 0;
    subcontrol-origin: margin;
}

/* Scroll Bars #QAbstractScrollArea, #QScrollBar*/
/* assigning background still leaves not filled area*/
QAbstractScrollArea::corner {
    background-color: transparent;
}

/* Horizontal */
QScrollBar:horizontal {
    height: 18px;
    border: none;
    margin: 0 23px 0 23px;
}

QScrollBar::handle:horizontal {
    min-width: 32px;
    margin: 4px 2px;
}

QScrollBar::add-line:horizontal {
    width: 23px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    width: 23px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

/* Vertical */
QScrollBar:vertical {
    width: 20px;
    border: none;
    margin: 23px 0 23px 0;
}

QScrollBar::handle:vertical {
    min-height: 32px;
    margin: 2px 4px;
}

QScrollBar::add-line:vertical {
    height: 23px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    height: 23px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

/* Combined */
QScrollBar {
    background-color: #3e3e42;
    border: none;
}

QScrollBar::handle {
    background-color: #686868;
}

QScrollBar::add-line,
QScrollBar::sub-line {
    background-color: #3e3e42;
    border: none;
}

/* QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::add-line:vertical:hover,
QScrollBar::sub-line:vertical:hover,
QScrollBar::add-line:horizontal:pressed,
QScrollBar::sub-line:horizontal:pressed,
QScrollBar::add-line:vertical:pressed,
QScrollBar::sub-line:vertical:pressed { } */
QScrollBar::handle:hover {
    background: #9e9e9e;
}

QScrollBar::handle:pressed {
    background: #efebef;
}

QScrollBar::handle:disabled {
    background: #555558;
}

QScrollBar::add-page,
QScrollBar::sub-page {
    background: transparent;
}

QScrollBar::up-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-up.png);
}

QScrollBar::up-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-up-hover.png);
}

QScrollBar::up-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-up-disabled.png);
}

QScrollBar::right-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-right.png);
}

QScrollBar::right-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}

QScrollBar::right-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-right-disabled.png);
}

QScrollBar::down-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-down.png);
}

QScrollBar::down-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-down-hover.png);
}

QScrollBar::down-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-down-disabled.png);
}

QScrollBar::left-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-left.png);
}

QScrollBar::left-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}

QScrollBar::left-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-left-disabled.png);
}

/* Header Rows and Tables (Configure Mod Categories) #QTableView, #QHeaderView */
QTableView {
    gridline-color: #3f3f46;
    selection-background-color: #3399ff;
    selection-color: #f1f1f1;
}

QTableView QTableCornerButton::section {
    background: #252526;
    border-color: #3f3f46;
    border-style: solid;
    border-width: 0 1px 1px 0;
}

QHeaderView {
    border: none;
}

QHeaderView::section {
    background: #252526;
    border-color: #3f3f46;
    padding: 3px 5px;
    border-style: solid;
    border-width: 0 1px 1px 0;
}

QHeaderView::section:hover {
    background: #3e3e40;
    color: #f6f6f6;
}

QHeaderView::section:last {
    border-right: 0;
}

QHeaderView::up-arrow {
    image: url(:/png/resources/png/sort-asc.png);
    width: 0px;
}


QHeaderView::down-arrow {
    image: url(:/png/resources/png/sort-desc.png);
    width: 0px;
}


/* Context menus, toolbar drop-downs #QMenu    */
QMenu {
    background-color: #1a1a1c;
    border-color: #333337;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}

QMenu::item {
    background: transparent;
    padding: 4px 20px;
}

QMenu::item:selected,
QMenuBar::item:selected {
    background-color: #333334;
}

QMenu::item:disabled {
    background-color: transparent;
}

QMenu::separator {
    background-color: #333337;
    height: 1px;
    margin: 1px 0;
}

QMenu::icon {
    margin: 1px;
}

QMenu::right-arrow {
    image: url(:/png/resources/png/sub-menu-arrow.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 0.5em;
}

QMenu QPushButton {
    background-color: transparent;
    border-color: #3f3f46;
    margin: 1px 0 1px 0;
}

QMenu QCheckBox,
QMenu QRadioButton {
    background-color: transparent;
    padding: 5px 2px;
}

/* Tool tips #QToolTip, #SaveGameInfoWidget */
QToolTip,
SaveGameInfoWidget {
    background-color: #424245;
    border-color: #4d4d50;
    color: #f1f1f1;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}

QStatusBar::item {
    border: None;
}

/* Progress Bars (Downloads) #QProgressBar */
QProgressBar {
    background-color: #e6e6e6;
    color: #000;
    border-color: #bcbcbc;
    text-align: center;
    border-style: solid;
    border-width: 1px;
    margin: 0px;
}

QProgressBar::chunk {
    background: #06b025;
}

DownloadListView[downloadView=standard]::item {
    padding: 16px;
}

DownloadListView[downloadView=compact]::item {
    padding: 4px;
}

/* Right Pane and Tab Bars #QTabWidget, #QTabBar */
QTabWidget::pane {
    border-color: #3f3f46;
    border-top-color: #007acc;
    top: 0;
    border-style: solid;
    border-width: 1px;
}

QTabWidget::pane:disabled {
    border-top-color: #3f3f46;
}

QTabBar::tab {
    background-color: transparent;
    padding: 4px 1em;
    border: none;
}

QTabBar::tab:hover {
    background-color: #1c97ea;
}

QTabBar::tab:selected,
QTabBar::tab:selected:hover {
    background-color: #007acc;
}

QTabBar::tab:disabled {
    background-color: transparent;
    color: #656565;
}

QTabBar::tab:selected:disabled {
    background-color: #3f3f46;
}

/* Scrollers */
QTabBar QToolButton {
    background-color: #333337;
    border-color: #3f3f46;
    padding: 1px;
    margin: 0;
    border-style: solid;
    border-width: 1px;
}

QTabBar QToolButton:hover {
    border-color: #007acc;
    border-width: 1px;
    border-style: solid;
}

QTabBar QToolButton:disabled,
QTabBar QToolButton:pressed:hover {
    background-color: #333337;
}

QTabBar::scroller {
    width: 23px;
    background-color: red;
}

QTabBar QToolButton::right-arrow {
    image: url(:/png/resources/png/scrollbar-right.png);
}

QTabBar QToolButton::right-arrow:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}

QTabBar QToolButton::left-arrow {
    image: url(:/png/resources/png/scrollbar-left.png);
}

QTabBar QToolButton::left-arrow:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}

/* Special styles */
QWidget#tabImages QPushButton {
    background-color: transparent;
    margin: 0 0.3em;
    padding: 0;
}

/* like dialog QPushButton*/
QWidget#tabESPs QToolButton {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}

QWidget#tabESPs QToolButton:hover {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}

QWidget#tabESPs QToolButton:focus {
    background-color: #dddddd;
    border-color: #3399ff;
}

QWidget#tabESPs QToolButton:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}

QTreeWidget#categoriesList {
    /* min-width: 225px; */
}

QTreeWidget#categoriesList::item {
    background-position: center left;
    background-repeat: no-repeat;
    padding: 0.35em 10px;
}

QTreeWidget#categoriesList::item:has-children {
    background-image: url(:/png/resources/png/branch-closed.png);
}

QTreeWidget#categoriesList::item:has-children:open {
    background-image: url(:/png/resources/png/branch-open.png);
}

QDialog#QueryOverwriteDialog QPushButton {
    margin-left: 0.5em;
}

QDialog#PyCfgDialog QPushButton:hover {
    background-color: #BEE6FD;
}

QLineEdit#modFilterEdit {
    margin-top: 2px;
}

/* highlight unchecked BSAs */
QWidget#bsaTab QTreeWidget::indicator:unchecked {
    background-color: #3399ff;
}

/* increase version text field */
QLineEdit#versionEdit {
    max-width: 100px;
}

/* Dialogs width changes */
/* increase width to prevent buttons cutting */
QDialog#QueryOverwriteDialog {
    min-width: 565px;
}

QDialog#ModInfoDialog {
    min-width: 850px;
}

QLineEdit[valid-filter=false] {
    background-color: #661111 !important;
}

/* собственное решение */
QToolBar QToolButton:disabled {
    background-color: #252526;
}

QToolBar QToolButton:checked {
    background-color: #3399ff;
}

"""


lqss = """
/*!*************************************
    VS15 Light
****************************************
    Author: chintsu_kun, holt59, MO2 Team
    Modified by: User
    Version: 2.5.0
    Licence: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)
    Source: https://github.com/nikolay-borzov/modorganizer-themes
****************************************
*/
/* For some reason applying background-color or border fixes paddings properties */
QListWidget::item {
    border-width: 0;
}
/* Don't override install label on download widget.
     MO2 assigns color depending on download state */
#installLabel {
    color: none;
}
/* Make `background-color` work for :hover, :focus and :pressed states */
QToolButton {
    border: none;
}
* {
    font-family: Open Sans;
}
/* Main Window */
QWidget {
    background-color: #f9f9f9;
    color: #333333;
}
QWidget::disabled {
    color: #999999;
}
/* Common */
/* remove outline */
* {
    outline: 0;
}
*:disabled,
QListView::item:disabled,
*::item:selected:disabled {
    color: #999999;
}
/* line heights */
/* QTreeView#fileTree::item - currently have problem with size column vertical
     text align */
#bsaList::item,
#dataTree::item,
#modList::item,
#categoriesTree::item,
#savegameList::item,
#tabConflicts QTreeWidget::item {
    padding: 0.3em 0;
}
QListView::item,
QTreeView#espList::item {
    /*
    padding: 0.3em 0;
    */
}
QListView#lw_pages_template::item {
    padding: 0.2em 0;
}
/* to enable border color */
QTreeView,
QListView,
QTextEdit,
QWebView,
QTableView {
    border-style: solid;
    border-width: 1px;
}
QAbstractItemView {
    color: #333333;
    background-color: #ffffff;
    alternate-background-color: #f0f0f0;
    border-color: #cccccc;
}
QAbstractItemView::item:selected,
QAbstractItemView::item:selected:hover,
QAbstractItemView::item:alternate:selected,
QAbstractItemView::item:alternate:selected:hover {
    color: #ffffff;
    background-color: #4a90e2;
}
QAbstractItemView[filtered=true] {
    border: 2px solid #ff0000 !important;
}
QAbstractItemView,
QListView,
QTreeView {
    show-decoration-selected: 1;
}
QAbstractItemView::item:hover,
QAbstractItemView::item:alternate:hover,
QAbstractItemView::item:disabled:hover,
QAbstractItemView::item:alternate:disabled:hover QListView::item:hover,
QTreeView::branch:hover,
QTreeWidget::item:hover {
    background-color: rgba(70, 140, 220, 0.2);
}
QAbstractItemView::item:selected:disabled,
QAbstractItemView::item:alternate:selected:disabled,
QListView::item:selected:disabled,
QTreeView::branch:selected:disabled,
QTreeWidget::item:selected:disabled {
    background-color: rgba(80, 150, 220, 0.2);
}
QTreeView::branch:selected,
#bsaList::branch:selected {
    background-color: #4a90e2;
}
QLabel {
    background-color: transparent;
}
LinkLabel {
    qproperty-linkColor: #4a90e2;
}
/* Left Pane & File Trees #QTreeView, #QListView*/
QTreeView::branch:closed:has-children {
    image: url(:/png/resources/png/branch-closed.png);
}
QTreeView::branch:open:has-children {
    image: url(:/png/resources/png/branch-open.png);
}
QListView::item {
    color: #333333;
}
/* Text areas and text fields #QTextEdit, #QLineEdit, #QWebView */
QTextEdit,
QWebView,
QLineEdit,
QAbstractSpinBox,
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button,
QComboBox {
    background-color: #ffffff;
    border-color: #cccccc;
}
QLineEdit:hover,
QAbstractSpinBox:hover,
QTextEdit:hover,
QComboBox:hover,
QComboBox:editable:hover {
    border-color: #4a90e2;
}
QLineEdit:focus,
QAbstractSpinBox::focus,
QTextEdit:focus,
QComboBox:focus,
QComboBox:editable:focus,
QComboBox:on {
    background-color: #f0f0f0;
    border-color: #4a90e2;
}
QComboBox:on {
    border-bottom-color: #cccccc;
}
QLineEdit,
QAbstractSpinBox {
    min-height: 15px;
    padding: 2px;
    border-style: solid;
    border-width: 1px;
}
QLineEdit {
    margin-top: 0;
}
/* clear button */
QLineEdit QToolButton,
QLineEdit QToolButton:hover {
    background: none;
    margin-top: 1px;
}
QLineEdit#espFilterEdit QToolButton {
    margin-top: -2px;
    margin-bottom: 1px;
}
/* Drop-downs #QComboBox*/
QComboBox {
    min-height: 20px;
    padding-left: 5px;
    margin: 3px 0 1px 0;
    border-style: solid;
    border-width: 1px;
}
QComboBox:editable {
    padding-left: 3px;
    /* to enable hover styles */
    background-color: transparent;
}
QComboBox::drop-down {
    width: 20px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border: none;
}
QComboBox::down-arrow {
    image: url(:/png/resources/png/combobox-down.png);
}
QComboBox QAbstractItemView {
    background-color: #fafafa;
    selection-background-color: #f0f0f0;
    border-color: #4a90e2;
    border-style: solid;
    border-width: 0 1px 1px 1px;
}
/* Doesn't work http://stackoverflow.com/questions/13308341/qcombobox-abstractitemviewitem */
/* QComboBox QAbstractItemView:item {
    padding: 10px;
    margin: 10px;
} */
/* Toolbar */
QToolBar {
    border: none;
}
QToolBar::separator {
    border-left-color: #dddddd;
    border-right-color: #bbbbbb;
    border-width: 0 1px 0 1px;
    border-style: solid;
    width: 0;
}
QToolButton {
    padding: 4px;
}
QToolButton:hover, QToolButton:focus {
    background-color: #e0e0e0;
}
QToolButton:pressed {
    background-color: #4a90e2;
}
QToolButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-top: 10%;
    padding-right: 5%;
}
/* Group Boxes #QGroupBox */
QGroupBox {
    border-color: #cccccc;
    border-style: solid;
    border-width: 1px;
    /*
    padding: 1em 0.3em 0.3em 0.3em;
    margin-top: 0.65em;
    */
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px;
    left: 10px;
}
/* LCD Count */
QLCDNumber {
    border-color: #cccccc;
    border-style: solid;
    border-width: 1px;
}
/* Buttons #QPushButton */
QPushButton {
    background-color: #f0f0f0;
    border-color: #cccccc;
    min-height: 18px;
    padding: 2px 5px;
    border-style: solid;
    border-width: 1px;
}
QPushButton:hover,
QPushButton:checked,
QAbstractSpinBox::up-button:hover,
QAbstractSpinBox::down-button:hover {
    background-color: #4a90e2;
}
QPushButton:focus {
    border-color: #4a90e2;
}
QPushButton:pressed,
QPushButton:checked:hover,
QAbstractSpinBox::up-button:pressed,
QAbstractSpinBox::down-button:pressed {
    background-color: #3c85d8;
}
QPushButton:disabled,
QAbstractSpinBox::up-button:disabled,
QAbstractSpinBox::down-button:disabled {
    background-color: #f0f0f0;
    border-color: #cccccc;
}
QPushButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 5%;
}
/* Dialog buttons */
QSlider::handle:horizontal,
QSlider::handle:vertical {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}
QSlider::handle:horizontal:hover,
QSlider::handle:vertical:hover,
QSlider::handle:horizontal:pressed,
QSlider::handle:horizontal:focus:pressed,
QSlider::handle:vertical:pressed,
QSlider::handle:vertical:focus:pressed {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}
QSlider::handle:horizontal:focus,
QSlider::handle:vertical:focus {
    background-color: #dddddd;
    border-color: #4a90e2;
}
QSlider::handle:horizontal:disabled,
QSlider::handle:vertical:disabled {
    background-color: #f0f0f0;
    border-color: #cccccc;
}
/* Check boxes and Radio buttons common #QCheckBox, #QRadioButton */
QListView::indicator,
QGroupBox::indicator,
QTreeView::indicator,
QCheckBox::indicator,
QRadioButton::indicator {
    background-color: #ffffff;
    border-color: #cccccc;
    width: 13px;
    height: 13px;
    border-style: solid;
    border-width: 1px;
}
QListView::indicator:hover,
QGroupBox::indicator:hover,
QTreeView::indicator:hover,
QCheckBox::indicator:hover,
QRadioButton::indicator:hover {
    background-color: #e0e0e0;
    border-color: #4a90e2;
}
QListView::indicator:checked,
QGroupBox::indicator:checked,
QTreeView::indicator:checked,
QCheckBox::indicator:checked {
    image: url(:/png/resources/png/checkbox-check.png);
}
QListView::indicator:checked:disabled,
QGroupBox::indicator:disabled,
QTreeView::indicator:checked:disabled,
QCheckBox::indicator:checked:disabled {
    image: url(:/png/resources/png/checkbox-check-disabled.png);
}
/* Check boxes special */
QTreeView#modList::indicator {
    width: 15px;
    height: 15px;
}
/* Radio buttons #QRadioButton */
QRadioButton::indicator {
    border-node_radius: 7px;
}
QRadioButton::indicator::checked {
    background-color: #dcdcdc;
    border-width: 2px;
    width: 11px;
    height: 11px;
}
QRadioButton::indicator::checked:hover {
    border-color: #cccccc;
}
/* Spinners #QSpinBox, #QDoubleSpinBox */
QAbstractSpinBox {
    margin: 1px;
}
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button {
    border-style: solid;
    border-width: 1px;
    subcontrol-origin: padding;
}
QAbstractSpinBox::up-button {
    subcontrol-position: top right;
}
QAbstractSpinBox::up-arrow {
    image: url(:/png/resources/png/spinner-up.png);
}
QAbstractSpinBox::down-button {
    subcontrol-position: bottom right;
}
QAbstractSpinBox::down-arrow {
    image: url(:/png/resources/png/spinner-down.png);
}
/* Sliders #QSlider */
QSlider::groove:horizontal {
    background-color: #cccccc;
    border: none;
    height: 8px;
    margin: 2px 0;
}
QSlider::handle:horizontal {
    width: 0.5em;
    height: 2em;
    margin: -7px 0;
    subcontrol-origin: margin;
}
/* Scroll Bars #QAbstractScrollArea, #QScrollBar*/
/* assigning background still leaves not filled area*/
QAbstractScrollArea::corner {
    background-color: transparent;
}
/* Horizontal */
QScrollBar:horizontal {
    height: 18px;
    border: none;
    margin: 0 23px 0 23px;
}
QScrollBar::handle:horizontal {
    min-width: 32px;
    margin: 4px 2px;
}
QScrollBar::add-line:horizontal {
    width: 23px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    width: 23px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
/* Vertical */
QScrollBar:vertical {
    width: 20px;
    border: none;
    margin: 23px 0 23px 0;
}
QScrollBar::handle:vertical {
    min-height: 32px;
    margin: 2px 4px;
}
QScrollBar::add-line:vertical {
    height: 23px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    height: 23px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
/* Combined */
QScrollBar {
    background-color: #e0e0e0;
    border: none;
}
QScrollBar::handle {
    background-color: #aaaaaa;
}
QScrollBar::add-line,
QScrollBar::sub-line {
    background-color: #e0e0e0;
    border: none;
}
/* QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::add-line:vertical:hover,
QScrollBar::sub-line:vertical:hover,
QScrollBar::add-line:horizontal:pressed,
QScrollBar::sub-line:horizontal:pressed,
QScrollBar::add-line:vertical:pressed,
QScrollBar::sub-line:vertical:pressed { } */
QScrollBar::handle:hover {
    background: #cccccc;
}
QScrollBar::handle:pressed {
    background: #eeeeee;
}
QScrollBar::handle:disabled {
    background: #bbbbbb;
}
QScrollBar::add-page,
QScrollBar::sub-page {
    background: transparent;
}
QScrollBar::up-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-up.png);
}
QScrollBar::up-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-up-hover.png);
}
QScrollBar::up-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-up-disabled.png);
}
QScrollBar::right-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-right.png);
}
QScrollBar::right-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}
QScrollBar::right-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-right-disabled.png);
}
QScrollBar::down-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-down.png);
}
QScrollBar::down-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-down-hover.png);
}
QScrollBar::down-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-down-disabled.png);
}
QScrollBar::left-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-left.png);
}
QScrollBar::left-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}
QScrollBar::left-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-left-disabled.png);
}
/* Header Rows and Tables (Configure Mod Categories) #QTableView, #QHeaderView */
QTableView {
    gridline-color: #cccccc;
    selection-background-color: #4a90e2;
    selection-color: #ffffff;
}
QTableView QTableCornerButton::section {
    background: #f5f5f5;
    border-color: #cccccc;
    border-style: solid;
    border-width: 0 1px 1px 0;
}
QHeaderView {
    border: none;
}
QHeaderView::section {
    background: #f5f5f5;
    border-color: #cccccc;
    padding: 3px 5px;
    border-style: solid;
    border-width: 0 1px 1px 0;
}
QHeaderView::section:hover {
    background: #e0e0e0;
    color: #111111;
}
QHeaderView::section:last {
    border-right: 0;
}
QHeaderView::up-arrow {
    image: url(:/png/resources/png/sort-asc.png);
    width: 0px;
}
QHeaderView::down-arrow {
    image: url(:/png/resources/png/sort-desc.png);
    width: 0px;
}
/* Context menus, toolbar drop-downs #QMenu    */
QMenu {
    background-color: #ffffff;
    border-color: #f0f0f0;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}
QMenu::item {
    background: transparent;
    padding: 4px 20px;
}
QMenu::item:selected,
QMenuBar::item:selected {
    background-color: #e0e0e0;
}
QMenu::item:disabled {
    background-color: transparent;
}
QMenu::separator {
    background-color: #f0f0f0;
    height: 1px;
    margin: 1px 0;
}
QMenu::icon {
    margin: 1px;
}
QMenu::right-arrow {
    image: url(:/png/resources/png/sub-menu-arrow.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 0.5em;
}
QMenu QPushButton {
    background-color: transparent;
    border-color: #cccccc;
    margin: 1px 0 1px 0;
}
QMenu QCheckBox,
QMenu QRadioButton {
    background-color: transparent;
    padding: 5px 2px;
}
/* Tool tips #QToolTip, #SaveGameInfoWidget */
QToolTip,
SaveGameInfoWidget {
    background-color: #f0f0f0;
    border-color: #dddddd;
    color: #333333;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}
QStatusBar::item {
    border: None;
}
/* Progress Bars (Downloads) #QProgressBar */
QProgressBar {
    background-color: #e6e6e6;
    color: #000;
    border-color: #bcbcbc;
    text-align: center;
    border-style: solid;
    border-width: 1px;
    margin: 0px;
}
QProgressBar::chunk {
    background: #06b025;
}
DownloadListView[downloadView=standard]::item {
    padding: 16px;
}
DownloadListView[downloadView=compact]::item {
    padding: 4px;
}
/* Right Pane and Tab Bars #QTabWidget, #QTabBar */
QTabWidget::pane {
    border-color: #cccccc;
    border-top-color: #4a90e2;
    top: 0;
    border-style: solid;
    border-width: 1px;
}
QTabWidget::pane:disabled {
    border-top-color: #cccccc;
}
QTabBar::tab {
    background-color: transparent;
    padding: 4px 1em;
    border: none;
}
QTabBar::tab:hover {
    background-color: #3c85d8;
}
QTabBar::tab:selected,
QTabBar::tab:selected:hover {
    background-color: #4a90e2;
}
QTabBar::tab:disabled {
    background-color: transparent;
    color: #999999;
}
QTabBar::tab:selected:disabled {
    background-color: #f0f0f0;
}
/* Scrollers */
QTabBar QToolButton {
    background-color: #f0f0f0;
    border-color: #cccccc;
    padding: 1px;
    margin: 0;
    border-style: solid;
    border-width: 1px;
}
QTabBar QToolButton:hover {
    border-color: #4a90e2;
    border-width: 1px;
    border-style: solid;
}
QTabBar QToolButton:disabled,
QTabBar QToolButton:pressed:hover {
    background-color: #f0f0f0;
}
QTabBar::scroller {
    width: 23px;
    background-color: red;
}
QTabBar QToolButton::right-arrow {
    image: url(:/png/resources/png/scrollbar-right.png);
}
QTabBar QToolButton::right-arrow:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}
QTabBar QToolButton::left-arrow {
    image: url(:/png/resources/png/scrollbar-left.png);
}
QTabBar QToolButton::left-arrow:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}
/* Special styles */
QWidget#tabImages QPushButton {
    background-color: transparent;
    margin: 0 0.3em;
    padding: 0;
}
/* like dialog QPushButton*/
QWidget#tabESPs QToolButton {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}
QWidget#tabESPs QToolButton:hover {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}
QWidget#tabESPs QToolButton:focus {
    background-color: #dddddd;
    border-color: #4a90e2;
}
QWidget#tabESPs QToolButton:disabled {
    background-color: #f0f0f0;
    border-color: #cccccc;
}
QTreeWidget#categoriesList {
    /* min-width: 225px; */
}
QTreeWidget#categoriesList::item {
    background-position: center left;
    background-repeat: no-repeat;
    padding: 0.35em 10px;
}
QTreeWidget#categoriesList::item:has-children {
    background-image: url(:/png/resources/png/branch-closed.png);
}
QTreeWidget#categoriesList::item:has-children:open {
    background-image: url(:/png/resources/png/branch-open.png);
}
QDialog#QueryOverwriteDialog QPushButton {
    margin-left: 0.5em;
}
QDialog#PyCfgDialog QPushButton:hover {
    background-color: #BEE6FD;
}
QLineEdit#modFilterEdit {
    margin-top: 2px;
}
/* highlight unchecked BSAs */
QWidget#bsaTab QTreeWidget::indicator:unchecked {
    background-color: #4a90e2;
}
/* increase version text field */
QLineEdit#versionEdit {
    max-width: 100px;
}
/* Dialogs width changes */
/* increase width to prevent buttons cutting */
QDialog#QueryOverwriteDialog {
    min-width: 565px;
}
QDialog#ModInfoDialog {
    min-width: 850px;
}
QLineEdit[valid-filter=false] {
    background-color: #ffdddd !important;
}
/* Ñ  Ð¾Ð±Ñ  Ñ  Ð²ÐµÐ½Ð½Ð¾Ðµ Ñ  ÐµÑ  ÐµÐ½Ð¸Ðµ */
QToolBar QToolButton:disabled {
    background-color: #f5f5f5;
}
QToolBar QToolButton:checked {
    background-color: #4a90e2;
}
"""

``
### D:\projects\net-constructor\package\modules\configs.py
``python
import json


class Configs:
    def __init__(self):
        self.__global = {}
        self.__nodes = {}
        self.__connections = {}

    def load_configs(self, dir_app):
        with open(dir_app + "/configs/config_global.json", "r", encoding="utf-8") as f:
            self.__global = json.load(f)
        with open(dir_app + "/configs/config_nodes.json", "r", encoding="utf-8") as f:
            self.__nodes = json.load(f)
        with open(
            dir_app + "/configs/config_connections.json", "r", encoding="utf-8"
        ) as f:
            self.__connections = json.load(f)

    def get_node(self, node_id: str) -> dict:
        return self.__nodes.get(node_id, {})

    def get_connection(self, connection_id: str) -> dict:
        return self.__connections.get(connection_id, {})

    def get_nodes(self) -> dict:
        return self.__nodes

    def get_connections(self) -> dict:
        return self.__connections

    def get_config_diagrams(self) -> dict:
        diagrams = self.__global.get("diagrams", {})
        return dict(sorted(diagrams.items(), key=lambda x: x[1].get("order", 0)))


    def get_config_control_sectors(self) -> dict:
        control_sectors_config = self.__global.get("control_sectors_config", {})
        return dict(
            sorted(control_sectors_config.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_diagram_parameters_by_type_id(self, diagram_type_id) -> dict:
        diagrams = self.__global.get("diagrams", {})
        parameters = diagrams.get(str(diagram_type_id), {}).get("parameters", {})
        return dict(sorted(parameters.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_diagram_nodes_by_type_id(self, diagram_type_id) -> dict:
        diagrams = self.__global.get("diagrams", {})
        id_nodes = diagrams.get(str(diagram_type_id), {}).get("id_nodes", [])
        config_diagram_nodes = {
            node_type_id: self.get_node(node_type_id) for node_type_id in id_nodes
        }
        return config_diagram_nodes

    def get_config_diagram_connections_by_type_id(self, diagram_type_id) -> dict:
        diagrams = self.__global.get("diagrams", {})
        id_connections = diagrams.get(str(diagram_type_id), {}).get(
            "id_connections", []
        )
        config_diagram_connections = {
            connection_type_id: self.get_connection(connection_type_id)
            for connection_type_id in id_connections
        }
        return config_diagram_connections

    def get_config_node_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        object_data = self.get_node(node_id).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_node_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        type_object_data = self.get_node(node_id).get("type_object_data", {})
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_node(self, node) -> dict:
        node_id = node.get("node_id", "0")
        objects_data = self.get_node(node_id).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_connection_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        object_data = self.get_connection(connection_id).get("object_data", {})
        return dict(sorted(object_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_type_connection_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        type_object_data = self.get_connection(connection_id).get(
            "type_object_data", {}
        )
        return dict(
            sorted(type_object_data.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_data_by_connection(self, connection) -> dict:
        connection_id = connection.get("connection_id", "0")
        objects_data = self.get_connection(connection_id).get("objects_data", {})
        return dict(sorted(objects_data.items(), key=lambda x: x[1].get("order", 0)))

    def get_config_node_parameters_by_node(self, node) -> dict:
        object_parameters = self.get_node(node.get("node_id", "0")).get(
            "object_parameters", {}
        )
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_node_parameters_by_node(self, node) -> dict:
        type_object_parameters = self.get_node(node.get("node_id", "0")).get(
            "type_object_parameters", {}
        )
        return dict(
            sorted(type_object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_parameters_by_node(self, node) -> dict:
        objects_parameters = self.get_node(node.get("node_id", "0")).get(
            "objects_parameters", {}
        )
        return dict(
            sorted(objects_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_connection_parameters_by_connection(self, connection) -> dict:
        object_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("object_parameters", {})
        return dict(
            sorted(object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_type_connection_parameters_by_connection(self, connection) -> dict:
        type_object_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("type_object_parameters", {})
        return dict(
            sorted(type_object_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

    def get_config_objects_parameters_by_connection(self, connection) -> dict:
        objects_parameters = self.get_connection(
            connection.get("connection_id", "0")
        ).get("objects_parameters", {})
        return dict(
            sorted(objects_parameters.items(), key=lambda x: x[1].get("order", 0))
        )

``
### D:\projects\net-constructor\package\modules\diagramdrawer.py
``python
# diagramdrawer.py

import package.modules.drawnode as drawnode
import package.modules.drawconnection as drawconnection


class Node:
    def __init__(
        self, node=None, config_node=None, before_wrap=False, after_wrap=False
    ):
        self.__type = "node"
        self.__node = node
        self.__config_node = config_node
        self.__before_wrap = before_wrap
        self.__after_wrap = after_wrap

    def get_type(self):
        return self.__type

    def get_node(self):
        return self.__node

    def get_id(self):
        return self.__node.get("id")

    def get_config_node(self):
        return self.__config_node

    def get_parameters(self):
        return self.__node.get("parameters", {})

    def get_config_parameters(self):
        return {
            **self.__config_node.get("object_parameters", {}),
            **self.__config_node.get("type_object_parameters", {}),
            **self.__config_node.get("objects_parameters", {}),
        }

    def get_node_id(self):
        return self.__node.get("node_id")

    def get_data(self):
        return self.__node.get("data", {})

    def get_is_wrap(self):
        return self.__before_wrap or self.__after_wrap

    def get_before_wrap(self):
        return self.__before_wrap

    def get_after_wrap(self):
        return self.__after_wrap


class Connection:
    def __init__(self, connection, config_connection):
        self.__type = "connection"
        self.__connection = connection
        self.__config_connection = config_connection

    def get_type(self):
        return self.__type

    def get_connection(self):
        return self.__connection

    def get_config_connection(self):
        return self.__config_connection

    def get_parameters(self):
        return self.__connection.get("parameters", {})

    def get_config_parameters(self):
        return {
            **self.__config_connection.get("object_parameters", {}),
            **self.__config_connection.get("type_object_parameters", {}),
            **self.__config_connection.get("objects_parameters", {}),
        }

    def get_connection_id(self):
        return self.__connection.get("connection_id")

    def get_data(self):
        return self.__connection.get("data", {})


class Diagram:
    def __init__(self, data, config_diagram_parameters):
        self.__type = "diagram"
        self.__diagram_type_id = data.get("diagram_type_id", 0)
        self.__diagram_name = data.get("diagram_name", "")
        self.__diagram_parameters = data.get("diagram_parameters", {})
        self.__config_diagram_parameters = config_diagram_parameters

    def get_type(self):
        return self.__type

    def get_diagram_type_id(self):
        return self.__diagram_type_id

    def get_diagram_name(self):
        return self.__diagram_name

    def get_parameters(self):
        return self.__diagram_parameters

    def get_config_parameters(self):
        return self.__config_diagram_parameters


class Rows:
    def __init__(self):
        self.__rows = []
        self.__current_row = None

    def append(self, row):
        self.__rows.append(row)

    def new_row(self, x, y):
        self.__current_row = {"x": x, "y": y, "length": None}

    def end_row(self, x):
        self.__current_row["length"] = x - self.__current_row.get("x")
        self.__rows.append(self.__current_row)

    def end_rows(self, x):
        if self.__current_row:
            self.end_row(x)

    def print_all(self):
        for index, row in enumerate(self.__rows):
            print(f"index={index}, row={row}")

    def get_rows(self):
        return self.__rows


class DiagramDrawer:
    """Класс для рисования диаграммы."""

    def __init__(self, obsm, data):
        self.__obsm = obsm
        self.__data = data
        #
        config_diagram_parameters = (
            self.__obsm.obj_configs.get_config_diagram_parameters_by_type_id(
                data.get("diagram_type_id", 0)
            )
        )
        self.__object_diagram = Diagram(data, config_diagram_parameters)
        #
        self.__nodes = self.__data.get("nodes", [])
        self.__connections = self.__data.get("connections", [])
        #
        self.__config_nodes = self.__obsm.obj_configs.get_nodes()
        self.__config_connections = self.__obsm.obj_configs.get_connections()

    def _get_delta_wrap_x(self, node):
        delta_wrap_x = (
            node.get("parameters", {}).get("delta_wrap_x", {}).get("value", 0)
        )
        return delta_wrap_x

    def _prepare_main_drawing_data(self, start_x, start_y, delta_wrap_y, max_nodes_in_row):
        """Подготавливает данные для рисования"""
        x = start_x
        y = start_y
        #
        to_right_optical_length = 0
        to_right_physical_length = 0
        #
        rows = Rows()
        #
        prepared_data = []
        current_row_node_count = 0
        #
        max_length = max(len(self.__nodes), len(self.__connections))
        # проход по всем узлам и соединениям по очереди
        for index in range(max_length):
            if index < len(self.__nodes):
                #
                current_row_node_count += 1
                #
                node = self.__nodes[index]
                # config
                node_id = node.get("node_id")

                if node_id is not None:
                    node_id_str = str(node_id)
                    config_node = self.__config_nodes.get(node_id_str, {})
                else:
                    config_node = {}
                #
                if index == 0:
                    x = start_x + self._get_delta_wrap_x(node)
                    rows.new_row(x, y)
                    #
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )
                elif not node.get("is_wrap") and (current_row_node_count < max_nodes_in_row or index == len(self.__nodes) - 1):
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )
                else:
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node, before_wrap=True),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )
                    #
                    rows.end_row(x)
                    #
                    x = start_x + self._get_delta_wrap_x(node)
                    y += delta_wrap_y
                    rows.new_row(x, y)
                    prepared_data.append(
                        {
                            "type": "node",
                            "object": Node(node, config_node, after_wrap=True),
                            "x": x,
                            "y": y,
                            "to_right_optical_length": to_right_optical_length,
                            "to_right_physical_length": to_right_physical_length,
                        }
                    )
                    #
                    current_row_node_count = 1
                    

            if index < len(self.__connections):
                connection = self.__connections[index]
                # config
                connection_id = connection.get("connection_id")
                if connection_id is not None:
                    connection_id_str = str(connection_id)
                    config_connection = self.__config_connections.get(
                        connection_id_str, {}
                    )
                else:
                    config_connection = {}
                # parameters соединения
                parameters = connection.get("parameters", {})
                # Так по идее не работает config_connection.get("parameters", {})
                config_parameters = config_connection.get("parameters", {})
                #
                connection_length = parameters.get(
                    "connection_length",
                    config_parameters.get("connection_length", {}),
                ).get("value", 0)
                # data соединения
                data = connection.get("data", {})
                # Так по идее не работает config_connection.get("data", {})
                config_data = config_connection.get("data", {})
                connection_optical_length = data.get(
                    "оптическая_длина", config_data.get("оптическая_длина", {})
                ).get("value", 0)
                connection_physical_length = data.get(
                    "физическая_длина", config_data.get("физическая_длина", {})
                ).get("value", 0)
                # сектора
                control_sectors = connection.get("control_sectors", [])
                # рисуем соединение
                # сектора
                control_sectors = connection.get("control_sectors", [])
                # рисуем соединение
                prepared_data.append(
                    {
                        "type": "connection",
                        "object": Connection(connection, config_connection),
                        "x": x,
                        "y": y,
                        "connection_optical_length": connection_optical_length,
                        "connection_physical_length": connection_physical_length,
                        "control_sectors": [],  # пустой список
                        "to_right_physical_length": to_right_physical_length,
                    }
                )
                # увеличиваем координаты по длине соединения
                if connection_id == "100" and len(control_sectors) > 0:
                    # current_row_node_count += 100
                    for index_cs, cs in enumerate(control_sectors):
                        # Проверяем последнее ли сектор (ибо в нем кт нет) 
                        is_last = index_cs == len(control_sectors) - 1
                        if not is_last:
                            current_row_node_count += 1
                        #
                        cs_copy = cs.copy()
                        x += (
                            cs.get("data_pars", {}).get("cs_lenght", {}).get("value", 0)
                        )
                        cs_copy["x"] = x
                        cs_copy["y"] = y
                        to_right_physical_length += (
                            cs.get("data_pars", {})
                            .get("cs_physical_length", {})
                            .get("value", 0)
                        )
                        #
                        # Если есть перенос и не последнее соединение
                        if cs.get("is_wrap", False) or (current_row_node_count >= max_nodes_in_row and not is_last):
                            rows.end_row(x)
                            y += delta_wrap_y
                            x = start_x + cs.get("data_pars", {}).get(
                                "cs_delta_wrap_x", {}
                            ).get("value", 0)
                            rows.new_row(x, y)
                            #
                            cs_copy["wrap_x"] = x
                            cs_copy["wrap_y"] = y
                            cs_copy["is_wrap"] = True
                            #
                            current_row_node_count = 1
                            
                        # добавляем изменённый сектор в prepared_data
                        prepared_data[-1]["control_sectors"].append(cs_copy)
                   
                    
                    

                else:
                    x += connection_length
                    # увеличиваем optical_length и physical_length
                    to_right_optical_length += connection_optical_length
                    to_right_physical_length += connection_physical_length
        #
        rows.end_rows(x)

        return prepared_data, to_right_optical_length, to_right_physical_length, rows

    def _set_to_left_lengths(
        self, prepared_data, to_right_optical_length, to_right_physical_length
    ):
        to_left_optical_length = to_right_optical_length
        to_left_physical_length = to_right_physical_length
        #
        for item in prepared_data:
            if item.get("type") == "node":
                item["to_left_optical_length"] = to_left_optical_length
                item["to_left_physical_length"] = to_left_physical_length
                print("_set_to_left_lengths item", item)
            #
            elif item.get("type") == "connection":
                to_left_optical_length -= item.get("connection_optical_length", 0)
                to_left_physical_length -= item.get("connection_physical_length", 0)

        return prepared_data

    def _center_rows(self, prepared_data, rows, width, is_center):
        #
        rows.print_all()
        if is_center:
            image_x = width // 2
            for row in rows.get_rows():
                row_x = row.get("x", 0)
                row_length = row.get("length", 0)
                delta_x = (row_x + row_x + row_length) // 2 - image_x
                print(f"""row_x={row_x}, row_length={row_length}, delta_x={delta_x}""")
                for item in prepared_data:
                    # меняем у вершин
                    if row.get("y") == item.get("y"):
                        # print(f"""ДО item['x']={item['x']} item['y']={item['y']}""")
                        item["x"] -= delta_x
                        # print(f"""ПОСЛЕ item['x']={item['x']} item['y']={item['y']}""")
                    # меняем у секторов
                    if item.get("type") == "connection":
                        for sector in item.get("control_sectors", []):
                            if row.get("y") == sector.get("y"):
                                # print(f"""ДО sector['x']={sector['x']} sector['y']={sector['y']}""")
                                sector["x"] -= delta_x
                            if row.get("y") == sector.get("wrap_y"):
                                sector["wrap_x"] -= delta_x
                                # print(f"""ПОСЛЕ sector['x']={sector['x']} sector['y']={sector['y']}""")

        return prepared_data

    def _preparation_draw(self, start_x, start_y, delta_wrap_y, indent_right, is_center, max_nodes_in_row):
        # подготавливаем данные
        prepared_data, to_right_optical_length, to_right_physical_length, rows = (
            self._prepare_main_drawing_data(start_x, start_y, delta_wrap_y, max_nodes_in_row)
        ) 
        #  
        rows_list = rows.get_rows()
        max_x = max(
            (row.get("x", 0) + row.get("length", 0) for row in rows_list),
            default=start_x
        )
        width = max_x + indent_right
        center_prepared_data = self._center_rows(prepared_data, rows, width, is_center)
        #
        self.prepared_data = self._set_to_left_lengths(
            center_prepared_data, to_right_optical_length, to_right_physical_length
        )
        return rows, width

    def draw(self, painter, start_x, delta_wrap_y):
        # сначала рисуем соединения
        for index, item in enumerate(self.prepared_data):
            if item.get("type") == "connection":
                # Кроме вершин ничего другого быть не может
                object_node_before = self.prepared_data[index - 1].get("object")
                object_node_after = self.prepared_data[index + 1].get("object")
                #
                object_connection = item.get("object")
                x = item.get("x")
                y = item.get("y")
                control_sectors = item.get("control_sectors")
                to_right_physical_length = item.get("to_right_physical_length")
                #
                self._draw_connection(
                    painter,
                    object_connection,
                    object_node_before,
                    object_node_after,
                    x,
                    y,
                    control_sectors,
                    to_right_physical_length,
                    start_x,
                    delta_wrap_y,
                )

        # Затем рисуем узлы
        node_index = 0
        for index, item in enumerate(self.prepared_data):
            if item.get("type") == "node":
                #
                object_before = None
                try:
                    if index > 0:
                        object_before = self.prepared_data[index - 1].get("object")
                except IndexError:
                    object_before = None
                #
                object_after = None
                try:
                    object_after = self.prepared_data[index + 1].get("object")
                except IndexError:
                    object_after = None
                #
                object_node = item.get("object")
                x = item.get("x")
                y = item.get("y")
                to_right_optical_length = item.get("to_right_optical_length")
                to_right_physical_length = item.get("to_right_physical_length")
                to_left_optical_length = item.get("to_left_optical_length")
                to_left_physical_length = item.get("to_left_physical_length")
                # рисуем
                self._draw_node(
                    painter,
                    object_node,
                    object_before,
                    object_after,
                    x,
                    y,
                    to_right_optical_length,
                    to_right_physical_length,
                    to_left_optical_length,
                    to_left_physical_length,
                    node_index,
                )
                # увеличиваем node_index
                node_index += 1

    def _draw_node(
        self,
        painter,
        object_node,
        object_before,
        object_after,
        x,
        y,
        to_right_optical_length,
        to_right_physical_length,
        to_left_optical_length,
        to_left_physical_length,
        node_index,
    ):
        node_obj = drawnode.DrawNode(
            painter,
            self.__object_diagram,
            object_node,
            object_before,
            object_after,
            x,
            y,
            to_right_optical_length,
            to_right_physical_length,
            to_left_optical_length,
            to_left_physical_length,
            node_index,
        )
        node_obj.draw()

    def _draw_connection(
        self,
        painter,
        object_connection,
        object_node_before,
        object_node_after,
        x,
        y,
        control_sectors,
        to_right_physical_length,
        start_x,
        delta_wrap_y,
    ):
        connection_obj = drawconnection.DrawConnection(
            painter,
            self.__object_diagram,
            object_connection,
            object_node_before,
            object_node_after,
            x,
            y,
            control_sectors,
            to_right_physical_length,
            start_x,
            delta_wrap_y,
        )
        connection_obj.draw()

``
### D:\projects\net-constructor\package\modules\dirpathmanager.py
``python


class DirPathManager:

    def __init__(self):
        self.__dir_app = None

    def set_dir_app(self, dir_app):
        self.__dir_app = dir_app

    def get_dir_app(self):
        return self.__dir_app
``
### D:\projects\net-constructor\package\modules\drawconnection.py
``python
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawdataparameters as drawdataparameters
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject
import package.modules.numberformatter as numberformatter


class DrawConnection:
    def __init__(
        self,
        painter,
        object_diagram,
        object_connection,
        object_node_before,
        object_node_after,
        x,
        y,
        control_sectors,
        to_right_physical_length,
        start_x,
        delta_wrap_y,
    ):
        self.__painter = painter
        self.__object_diagram = object_diagram
        self.__object_connection = object_connection
        self.__object_node_before = object_node_before
        self.__object_node_after = object_node_after
        self.__x = x
        self.__y = y
        self.__control_sectors = control_sectors
        self.__to_right_physical_length = to_right_physical_length
        self.__start_x = start_x
        self.__delta_wrap_y = delta_wrap_y
        print(
            f"LALALA self.__to_right_physical_length = {self.__to_right_physical_length}"
        )

    def draw(self):
        # Сначала выбор диграммы, а потом соединения
        pars = drawdataparameters.DrawParameters(
            self.__object_diagram,
            self.__object_connection,
            self.__object_node_before,
            self.__object_node_after,
        )
        data = drawdataparameters.DrawData(self.__object_connection)
        #
        diagram_type_id = self.__object_diagram.get_diagram_type_id()
        connection_id = self.__object_connection.get_connection_id()
        #
        nf = numberformatter.NumberFormatter()
        nf.set_precision_number(pars.get_sp("precision_number"))
        nf.set_precision_separator(pars.get_sp("precision_separator"))
        #
        if diagram_type_id == "0":
            if connection_id == "0":
                self._draw_connection_type_0(pars, data, nf)
        #
        elif diagram_type_id == "50":
            if connection_id == "50":
                self._draw_connection_type_50(pars, data, nf)
        #
        elif diagram_type_id == "100":
            if connection_id == "100":
                self._draw_connection_type_100(pars, data, nf)
        #
        elif diagram_type_id == "150":
            if connection_id == "150":
                self._draw_connection_type_150(pars, data, nf)

    def _draw_connection_type_0(self, pars, data, nf):
        # Функции для получения различных пейнтеров
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )

        def get_painter_text_name_and_location():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_name_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_name_pixel_size"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        #  Для LT и прочие
        before_delta_line_caption_and_node = 0
        after_delta_line_caption_and_node = 0
        #
        if self.__object_node_before.get_node_id() == "0":
            before_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + pars.get_bp("node_radius")
        elif self.__object_node_before.get_node_id() == "1":
            before_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + 2 * pars.get_bp("node_radius")
        #
        if self.__object_node_after.get_node_id() == "0":
            after_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + pars.get_ap("node_radius")
        elif self.__object_node_after.get_node_id() == "1":
            after_delta_line_caption_and_node = pars.get_sp(
                "connection_caption_margin_left_right"
            ) + 2 * pars.get_ap("node_radius")

        # ОСНОВНАЯ ЛИНИЯ
        # region
        self.__painter = get_painter_connection_line()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )
        # endregion

        # подписи к основной линии (LT и прочие)
        # region
        text = pars.get_sp("префикс_ВОК") + data.get_sd("ВОК")
        drawtext.DrawText().draw_singleline_text_by_hl_vb(
            get_painter_text_caption,
            text,
            self.__x + before_delta_line_caption_and_node,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
        )

        # LB
        text = pars.get_sp("префикс_количество_ОВ") + data.get_sd("количество_ОВ")
        drawtext.DrawText().draw_singleline_text_by_hl_vt(
            get_painter_text_caption,
            text,
            self.__x + before_delta_line_caption_and_node,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
        )

        # RT
        text = (
            pars.get_sp("префикс_физическая_длина")
            + nf.get(data.get_sd("физическая_длина"))
            + pars.get_sp("постфикс_расстояния")
        )
        drawtext.DrawText().draw_singleline_text_by_hr_vb(
            get_painter_text_caption,
            text,
            self.__x
            + pars.get_sp("connection_length")
            - after_delta_line_caption_and_node,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
        )

        # RB
        text = (
            pars.get_sp("префикс_оптическая_длина")
            + nf.get(data.get_sd("оптическая_длина"))
            + pars.get_sp("постфикс_расстояния")
        )
        drawtext.DrawText().draw_singleline_text_by_hr_vt(
            get_painter_text_caption,
            text,
            self.__x
            + pars.get_sp("connection_length")
            - after_delta_line_caption_and_node,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
        )
        # endregion

        # тонкие линии
        # region
        # (строительная_длина)
        # горизонтальная линия - название
        self.__painter = get_painter_thin_line()
        self.__painter.drawLine(
            QPoint(
                self.__x - pars.get_sp("distance_thin_line_after_connection_x"),
                self.__y + pars.get_sp("delta_node_and_thin_line"),
            ),
            QPoint(
                self.__x
                + pars.get_sp("connection_length")
                + pars.get_sp("distance_thin_line_after_connection_x"),
                self.__y + pars.get_sp("delta_node_and_thin_line"),
            ),
        )
        # стрелки
        drawobject.DrawObject().arrow(
            get_painter_arrow,
            self.__x + pars.get_sp("connection_length"),
            self.__y + pars.get_sp("delta_node_and_thin_line"),
            pars.get_sp("arrow_width"),
            pars.get_sp("arrow_height"),
            "right",
        )
        drawobject.DrawObject().arrow(
            get_painter_arrow,
            self.__x,
            self.__y + pars.get_sp("delta_node_and_thin_line"),
            pars.get_sp("arrow_width"),
            pars.get_sp("arrow_height"),
            "left",
        )

        # горизонтальная линия - местоположение
        if pars.get_bp("is_location"):
            self.__painter = get_painter_thin_line()
            self.__painter.drawLine(
                QPoint(
                    self.__x - pars.get_sp("distance_thin_line_after_connection_x"),
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                ),
                QPoint(
                    self.__x
                    + pars.get_sp("connection_length")
                    + pars.get_sp("distance_thin_line_after_connection_x"),
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                ),
            )
            # стрелки + проверка соседних узлов
            if pars.get_bp("node_is_connected_with_thin_line_location"):
                drawobject.DrawObject().arrow(
                    get_painter_arrow,
                    self.__x,
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    "left",
                )
            if pars.get_ap("node_is_connected_with_thin_line_location"):
                drawobject.DrawObject().arrow(
                    get_painter_arrow,
                    self.__x + pars.get_sp("connection_length"),
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("delta_thins_lines"),
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    "right",
                )
        # endregion

        # Тексты над/под название и название_доп и местоположение и местоположение_доп
        # region
        # Текст над/под с название и название_доп
        center_x = (self.__x + self.__x + pars.get_sp("connection_length")) // 2
        bottom_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            - pars.get_sp("connection_thin_caption_vertical_padding")
        )
        top_y = (
            self.__y
            + pars.get_sp("delta_node_and_thin_line")
            + pars.get_sp("connection_thin_caption_vertical_padding")
        )
        #
        text = data.get_sd("название")
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_name_and_location, text, center_x, bottom_y
        )
        #
        text = data.get_sd("название_доп")
        drawtext.DrawText().draw_multiline_text_by_hc_vt(
            get_painter_text_name_and_location, text, center_x, top_y
        )

        # Текст над/под с местоположение и местоположение_доп
        if pars.get_bp("is_location"):
            center_x_with_delta = (
                (self.__x + self.__x + pars.get_sp("connection_length")) // 2
            ) + pars.get_sp("connection_location_delta_x")
            bottom_y = (
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("delta_thins_lines")
                - pars.get_sp("connection_thin_caption_vertical_padding")
            )
            top_y = (
                self.__y
                + pars.get_sp("delta_node_and_thin_line")
                + pars.get_sp("delta_thins_lines")
                + pars.get_sp("connection_thin_caption_vertical_padding")
            )
            #
            text = data.get_sd("местоположение")
            drawtext.DrawText().draw_multiline_text_by_hc_vb(
                get_painter_text_name_and_location, text, center_x_with_delta, bottom_y
            )
            #
            text = data.get_sd("местоположение_доп")
            drawtext.DrawText().draw_multiline_text_by_hc_vt(
                get_painter_text_name_and_location, text, center_x_with_delta, top_y
            )

        # endregion

    def _draw_connection_type_50(self, pars, data, nf):
        # Функции для получения различных пейнтеров
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        # ОСНОВНАЯ ЛИНИЯ
        self.__painter = get_painter_connection_line()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )

        def draw_text_caption(text, center_x, y, is_top):
            func_text = (
                drawtext.DrawText().draw_multiline_text_by_hc_vt
                if is_top
                else drawtext.DrawText().draw_multiline_text_by_hc_vb
            )
            func_text(get_painter_text_caption, text, center_x, y)

        draw_text_caption(
            pars.get_sp("префикс_физическая_длина")
            + nf.get(data.get_sd("физическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            (2 * self.__x + pars.get_sp("connection_length")) // 2,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
            True,
        )

        draw_text_caption(
            pars.get_sp("префикс_оптическая_длина")
            + nf.get(data.get_sd("оптическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            (2 * self.__x + pars.get_sp("connection_length")) // 2,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
            False,
        )

    def _draw_connection_type_100(self, pars, data, nf):
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        def draw_main_line(
            cs_lenght, cs_name, cs_physical_length, is_first=False, is_last=False
        ):
            # ОСНОВНАЯ ЛИНИЯ
            self.__painter = get_painter_connection_line()
            self.__painter.drawLine(
                self.__x,
                self.__y,
                self.__x + cs_lenght,
                self.__y,
            )
            # Текст над/под с названием и физическая_длина
            before_half_width = 0
            after_half_width = 0
            #
            before_padding = 0
            after_padding = 0
            # Условия для первого и для последнего сектора
            if is_first and self.__object_node_before.get_node_id() == "101":
                before_half_width = pars.get_bp("node_width") // 2
                before_padding = before_half_width
            elif is_first and self.__object_node_before.get_node_id() == "100":
                before_half_width = pars.get_bp("node_radius")
                before_padding = before_half_width
            if is_last and self.__object_node_after.get_node_id() == "101":
                after_half_width = pars.get_ap("node_width") // 2
                after_padding = after_half_width
            elif is_last and self.__object_node_after.get_node_id() == "100":
                after_half_width = pars.get_ap("node_radius")
                after_padding = after_half_width
            #
            center_x = (
                (self.__x + before_half_width)
                + (self.__x - after_half_width + cs_lenght)
            ) // 2
            #
            print(f"cs_lenght = {cs_lenght}")
            #
            drawtext.DrawText().draw_multiline_text_by_hc_vb(
                get_painter_text_caption,
                cs_name,
                center_x,
                self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
                cs_lenght - before_padding - after_padding - 10,
            )
            #
            drawtext.DrawText().draw_multiline_text_by_hc_vt(
                get_painter_text_caption,
                nf.get(cs_physical_length) + pars.get_sp("постфикс_расстояния"),
                center_x,
                self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
                cs_lenght - before_padding - after_padding - 10,
            )

        def draw_control_point(is_before_wrap=False, is_after_wrap=False):
            def get_painter_figure_border():
                return painterconfigurator.PainterConfigurator(
                    self.__painter
                ).get_painter_figure_border(
                    pen_color=pars.get_sp("node_border_color"),
                    pen_weight=pars.get_sp("node_border_weight"),
                )

            def get_painter_text_caption():
                return painterconfigurator.PainterConfigurator(
                    self.__painter
                ).get_painter_text(
                    color=pars.get_sp("node_caption_physics_color"),
                    font_name=pars.get_sp("font_name"),
                    pixel_size=pars.get_sp("node_caption_physics_pixel_size"),
                )

            def get_painter_thin_line():
                return painterconfigurator.PainterConfigurator(
                    self.__painter
                ).get_painter_line(
                    color=pars.get_sp("thin_line_color"),
                    weight=pars.get_sp("thin_line_weight"),
                    style_name="SolidLine",
                )

            def get_painter_arrow():
                return painterconfigurator.PainterConfigurator(
                    self.__painter
                ).get_painter_figure_fill(
                    fill_color=pars.get_sp("thin_line_color"),
                    fill_pattern_name="SolidPattern",
                )

            # рисование wrap стрелки
            def draw_wrap_arrow(node_border_width):
                if pars.get_sp("is_wrap_arrow"):
                    if is_before_wrap:
                        drawobject.DrawObject().wrap_arrow(
                            get_painter_arrow,
                            get_painter_thin_line,
                            self.__x + node_border_width,
                            self.__y,
                            pars.get_sp("arrow_width"),
                            pars.get_sp("arrow_height"),
                            pars.get_sp("wrap_arrow_length"),
                            "before_wrap",
                        )
                    elif is_after_wrap:
                        drawobject.DrawObject().wrap_arrow(
                            get_painter_arrow,
                            get_painter_thin_line,
                            self.__x - node_border_width,
                            self.__y,
                            pars.get_sp("arrow_width"),
                            pars.get_sp("arrow_height"),
                            pars.get_sp("wrap_arrow_length"),
                            "after_wrap",
                        )

            # Рисование wrap стрелки
            draw_wrap_arrow(0)
            #
            self.__painter = get_painter_figure_border()
            self.__painter.drawLine(
                self.__x,
                self.__y - pars.get_sp("node_height"),
                self.__x,
                self.__y + pars.get_sp("node_height"),
            )

            # рисование значения физической длины
            x = self.__x
            # TODO Для первых и послдених вершин
            # if node_id == "101" and (not self.__object_before or self.__object_node.get_after_wrap()):
            #     x += pars.get_sp("node_width") // 2
            # elif node_id == "101" and (not self.__object_after or self.__object_node.get_before_wrap()):
            #     x -= pars.get_sp("node_width") // 2
            drawtext.DrawText().draw_singleline_text_rotated_by_hc_vt(
                get_painter_text_caption,
                nf.get(self.__to_right_physical_length)
                + pars.get_sp("постфикс_расстояния"),
                x,
                self.__y + pars.get_sp("node_caption_physics_vertical_padding"),
            )

        len_control_sectors = len(self.__control_sectors)
        if len_control_sectors > 0:
            total_len = 1 + (len_control_sectors - 1) * 2
            for index in range(total_len):
                cs = self.__control_sectors[index // 2]
                #
                is_last = index == total_len - 1
                #
                if index % 2 == 0:
                    # Сектор
                    draw_main_line(
                        cs.get("data_pars", {}).get("cs_lenght", {}).get("value", 0),
                        cs.get("data_pars", {}).get("cs_name", {}).get("value", ""),
                        cs.get("data_pars", {})
                        .get("cs_physical_length", {})
                        .get("value", 0),
                        index == 0,
                        index == total_len - 1,
                    )
                    # self.__x += (
                    #     cs.get("data_pars", {}).get("cs_lenght", {}).get("value", 0)
                    # )
                    self.__x = cs["x"]
                    self.__y = cs["y"]
                    self.__to_right_physical_length += (
                        cs.get("data_pars", {})
                        .get("cs_physical_length", {})
                        .get("value", 0)
                    )
                else:
                    # Контрольная точка
                    if cs.get("is_wrap", False) and not is_last:
                        draw_control_point(is_before_wrap=True)
                        # self.__x = self.__start_x + cs.get("data_pars", {}).get(
                        #     "cs_delta_wrap_x", {}
                        # ).get("value", 0)
                        # self.__y += self.__delta_wrap_y
                        self.__x = cs["wrap_x"]
                        self.__y = cs["wrap_y"]
                        draw_control_point(is_after_wrap=True)
                    else:
                        draw_control_point()

        else:
            draw_main_line(
                pars.get_sp("connection_length"),
                data.get_sd("название"),
                data.get_sd("физическая_длина"),
                True,
                True,
            )

    def _draw_connection_type_150(self, pars, data, nf):
        def get_painter_connection_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("connection_color"),
                weight=pars.get_sp("connection_width"),
                style_name=pars.get_sp("connection_style"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("connection_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("connection_caption_pixel_size"),
            )

        # ОСНОВНАЯ ЛИНИЯ
        self.__painter = get_painter_connection_line()
        self.__painter.drawLine(
            self.__x,
            self.__y,
            self.__x + pars.get_sp("connection_length"),
            self.__y,
        )

        # Текст над/под
        before_half_width = 0
        after_half_width = 0
        #
        if self.__object_node_before.get_node_id() == "151":
            before_half_width = pars.get_bp("node_width") // 2
            before_padding = before_half_width
        elif self.__object_node_before.get_node_id() == "150":
            before_padding = pars.get_bp("node_radius")
        if self.__object_node_after.get_node_id() == "151":
            after_half_width = pars.get_ap("node_width") // 2
            after_padding = after_half_width
        elif self.__object_node_after.get_node_id() == "150":
            after_padding = pars.get_ap("node_radius")
        #
        center_x = (
            (self.__x + before_half_width)
            + (self.__x - after_half_width + pars.get_sp("connection_length"))
        ) // 2
        #
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_caption,
            nf.get(data.get_sd("оптическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            center_x,
            self.__y - pars.get_sp("connection_main_caption_vertical_padding"),
            pars.get_sp("connection_length") - before_padding - after_padding - 10,
        )

        # МЕТКИ
        # Получаем значение начальной метки (если пустое или не число - используем 0)
        start_metka_str = data.get_sd("нач_метка")
        try:
            start_metka_value = int(float(start_metka_str)) if start_metka_str else 0
        except (ValueError, TypeError):
            start_metka_value = 0

        start_metka = str(start_metka_value).zfill(4)

        # Получаем значение физической длины (если пустое или не число - используем 0)
        physical_length_str = data.get_sd("физическая_длина")
        try:
            physical_length = (
                int(float(physical_length_str)) if physical_length_str else 0
            )
        except (ValueError, TypeError):
            physical_length = 0

        # Вычисляем конечную метку (начальная + длина)
        end_metka_value = start_metka_value + physical_length
        end_metka = str(end_metka_value).zfill(4)

        # Формируем текст метки с учетом направления
        direction_metka = (
            data.get_sd("direction_metka") == "True"
        )  # сравнение с строкой True ибо это дата, а не параметр
        text_metki = (
            f"{end_metka}-{start_metka}"
            if direction_metka
            else f"{start_metka}-{end_metka}"
        )
        # print(f"BLABLA {direction_metka, text_metki}")

        # Рисуем текст метки и физическую длину
        drawtext.DrawText().draw_multiline_text_by_hc_vt(
            get_painter_text_caption,
            text_metki
            + "\n"
            + nf.get(data.get_sd("физическая_длина"))
            + pars.get_sp("постфикс_расстояния"),
            center_x,
            self.__y + pars.get_sp("connection_main_caption_vertical_padding"),
            pars.get_sp("connection_length") - before_padding - after_padding - 10,
        )

``
### D:\projects\net-constructor\package\modules\drawdataparameters.py
``python

class DrawData:

    def __init__(self, object_target):
        self.__object_target = object_target
        #
        self.__self_data = self.__object_target.get_data()

    def get_sd(self, key) -> str:
        return str(self.__self_data.get(key, {}).get("value", ""))


class DrawParameters:
    def __init__(
        self,
        object_diagram,
        object_target,
        object_before=None,
        object_after=None
    ):
        self.__object_diagram = object_diagram
        self.__object_self = object_target
        self.__object_before = object_before
        self.__object_after = object_after

        self.__self_parameters = {}
        self.__before_parameters = {}
        self.__after_parameters = {}

        new_dict_diagram_parameters = self._get_dict(
            self.__object_diagram.get_parameters(),
            self.__object_diagram.get_config_parameters(),
        )
        self.__self_parameters = {
            **new_dict_diagram_parameters,
            **self._get_dict(
                self.__object_self.get_parameters(),
                self.__object_self.get_config_parameters(),
            ),
        }

        if self.__object_before:
            self.__before_parameters = {
                **new_dict_diagram_parameters,
                **self._get_dict(
                    self.__object_before.get_parameters(),
                    self.__object_before.get_config_parameters(),
                ),
            }
        if self.__object_after:
            self.__after_parameters = {
                **new_dict_diagram_parameters,
                **self._get_dict(
                    self.__object_after.get_parameters(),
                    self.__object_after.get_config_parameters(),
                ),
            }

    def _get_dict(self, parameters, config_parameters) -> dict:
        new_dict = {}
        for key, dict_value in config_parameters.items():
            new_dict[key] = dict_value.get("value", 0)
        for key in config_parameters.keys():
            value = parameters.get(key, {}).get("value", None)
            if value is not None:
                new_dict[key] = value
        return new_dict

    def get_sp(self, key):
        return self.__self_parameters.get(key, 0)

    def get_bp(self, key):
        return self.__before_parameters.get(key, 0)

    def get_ap(self, key):
        return self.__after_parameters.get(key, 0)
    

``
### D:\projects\net-constructor\package\modules\drawnode.py
``python
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPoint

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawdataparameters as drawdataparameters
import package.modules.drawtext as drawtext
import package.modules.drawobject as drawobject
import package.modules.numberformatter as numberformatter


class DrawNode:
    def __init__(
        self,
        painter,
        object_diagram,
        object_node,
        object_before,
        object_after,
        x,
        y,
        to_right_optical_length,
        to_right_physical_length,
        to_left_optical_length,
        to_left_physical_length,
        node_index
    ):
        self.__painter = painter
        self.__object_diagram = object_diagram
        self.__object_node = object_node
        self.__object_before = object_before
        self.__object_after = object_after
        self.__x = x
        self.__y = y
        self.__to_right_optical_length = to_right_optical_length
        self.__to_right_physical_length = to_right_physical_length
        self.__to_left_optical_length = to_left_optical_length
        self.__to_left_physical_length = to_left_physical_length
        self.__node_index = node_index

    def draw(self):
        # Сначала выбор диграммы, а потом узла
        data = drawdataparameters.DrawData(self.__object_node)
        pars = drawdataparameters.DrawParameters(
            self.__object_diagram,
            self.__object_node,
            self.__object_before,
            self.__object_after,
        )
        diagram_type_id = self.__object_diagram.get_diagram_type_id()
        node_id = self.__object_node.get_node_id()
        #
        nf = numberformatter.NumberFormatter()
        nf.set_precision_number(pars.get_sp("precision_number"))
        nf.set_precision_separator(pars.get_sp("precision_separator"))
        #
        # "Скелетная схема ВОЛП и основные данные цепей кабеля"

        if diagram_type_id == "0":
            if node_id == "0" or node_id == "1":
                self._draw_node_ids_0_1(pars, data, node_id, nf)
        # "Схема размещения строительных длин и смонтированных муфт на участках регенерации между оконечными пунктами ВОЛП"
        elif diagram_type_id == "50":
            if node_id == "50" or node_id == "51":
                self._draw_node_ids_50_51(pars, data, node_id, nf)
        # "Скелетная схема размещения строительных длин кабеля и смонтированных муфт на участке регенерации"
        elif diagram_type_id == "100":
            if node_id == "100" or node_id == "101":
                print("_draw_node_ids_100_101")
                self._draw_node_ids_100_101(pars, data, node_id, nf)
        # "Монтажная схема участка регенерации"
        elif diagram_type_id == "150":
            if node_id == "150" or node_id == "151":
                self._draw_node_ids_150_151(pars, data, node_id, nf)

    def _draw_node_ids_0_1(self, pars, data, node_id, nf):
        def get_painter_figure_border():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_border(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
            )

        def get_painter_figure_border_fill():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_figure_border_fill(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
                fill_color=pars.get_sp("node_fill_color"),
                fill_pattern_name=pars.get_sp("node_fill_style"),
            )

        def get_painter_text_name():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_pixel_size"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )

        # радиус вершины
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "1":
            node_border_radius *= 2

        # рисование wrap стрелки
        if pars.get_sp("is_wrap_arrow"):
            if self.__object_node.get_before_wrap():
                drawobject.DrawObject().wrap_arrow(
                    get_painter_arrow,
                    get_painter_thin_line,
                    self.__x + node_border_radius,
                    self.__y,
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    pars.get_sp("wrap_arrow_length"),
                    "before_wrap",
                )
            elif self.__object_node.get_after_wrap():
                drawobject.DrawObject().wrap_arrow(
                    get_painter_arrow,
                    get_painter_thin_line,
                    self.__x - node_border_radius,
                    self.__y,
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    pars.get_sp("wrap_arrow_length"),
                    "after_wrap",
                )

        # тонкая вертикальная линия
        def draw_vertical_thin_line():
            painter_thin_line = get_painter_thin_line()
            painter_thin_line.drawLine(
                QPoint(self.__x, self.__y),
                QPoint(
                    self.__x,
                    self.__y
                    + pars.get_sp("delta_node_and_thin_line")
                    + pars.get_sp("distance_thin_line_after_connection_y"),
                ),
            )
            # рисовать линию ЕСЛИ is_location И node_is_connected_with_thin_line_location
            if pars.get_sp("is_location") and pars.get_sp(
                "node_is_connected_with_thin_line_location"
            ):
                painter_thin_line.drawLine(
                    QPoint(
                        self.__x, self.__y + pars.get_sp("delta_node_and_thin_line")
                    ),
                    QPoint(
                        self.__x,
                        self.__y
                        + pars.get_sp("delta_node_and_thin_line")
                        + pars.get_sp("delta_thins_lines")
                        + pars.get_sp("distance_thin_line_after_connection_y"),
                    ),
                )

        # Проверяем наличие соединения
        if self.__object_before and self.__object_before.get_type() == "connection":
            draw_vertical_thin_line()
        elif self.__object_after and self.__object_after.get_type() == "connection":
            draw_vertical_thin_line()

        if node_id == "1":
            drawobject.DrawObject().node_big_circle_and_triangle(
                get_painter_figure_border,
                self.__x,
                self.__y,
                node_border_radius,
            )

        # Рисование вершины
        drawobject.DrawObject().node_circle(
            get_painter_figure_border,
            get_painter_figure_border_fill,
            self.__x,
            self.__y,
            pars.get_sp("node_radius"),
        )

        # Рисование названия
        text = data.get_sd("название") 
        if data.get_sd("местоположение"):
            text += '\n' + data.get_sd("местоположение")
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_name,
            text,
            self.__x,
            self.__y - pars.get_sp("node_name_height"),
            pars.get_sp("node_name_max_width")
        )

    def _draw_node_ids_50_51(self, pars, data, node_id, nf):
        def get_painter_figure_border():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_border(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
            )

        def get_painter_figure_border_fill():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_figure_border_fill(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
                fill_color=pars.get_sp("node_fill_color"),
                fill_pattern_name=pars.get_sp("node_fill_style"),
            )

        def get_painter_text_name():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_pixel_size"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("node_caption_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_caption_pixel_size"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )

        # радиус вершины
        node_border_radius = pars.get_sp("node_radius")
        if node_id == "51":
            node_border_radius *= 2

        # рисование wrap стрелки
        if pars.get_sp("is_wrap_arrow"):
            if self.__object_node.get_before_wrap():
                drawobject.DrawObject().wrap_arrow(
                    get_painter_arrow,
                    get_painter_thin_line,
                    self.__x + node_border_radius,
                    self.__y,
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    pars.get_sp("wrap_arrow_length"),
                    "before_wrap",
                )
            elif self.__object_node.get_after_wrap():
                drawobject.DrawObject().wrap_arrow(
                    get_painter_arrow,
                    get_painter_thin_line,
                    self.__x - node_border_radius,
                    self.__y,
                    pars.get_sp("arrow_width"),
                    pars.get_sp("arrow_height"),
                    pars.get_sp("wrap_arrow_length"),
                    "after_wrap",
                )

        # тонкая вертикальная линия
        painter_thin_line = get_painter_thin_line()
        delta_node_and_arrow_and_distance_thin_line_after_connection_y = max(
            pars.get_sp("delta_node_and_to_right_arrow"),
            pars.get_sp("delta_node_and_to_left_arrow"),
        ) + pars.get_sp("distance_thin_line_after_connection_y")
        #
        painter_thin_line.drawLine(
            QPoint(
                self.__x,
                self.__y
                - delta_node_and_arrow_and_distance_thin_line_after_connection_y,
            ),
            QPoint(
                self.__x,
                self.__y
                + delta_node_and_arrow_and_distance_thin_line_after_connection_y,
            ),
        )
        # рисование to_right to_left стрелок с линией и со значениями

        def draw_line_and_arrow(x, y, length, delta, direction):
            self.__painter = get_painter_thin_line()
            self.__painter.drawLine(QPoint(x + length, y - delta), QPoint(x, y - delta))
            self.__painter.drawLine(QPoint(x + length, y + delta), QPoint(x, y + delta))
            #
            drawobject.DrawObject().arrow(
                get_painter_arrow,
                x,
                y - delta,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                direction,
            )
            drawobject.DrawObject().arrow(
                get_painter_arrow,
                x,
                y + delta,
                pars.get_sp("arrow_width"),
                pars.get_sp("arrow_height"),
                direction,
            )

        def draw_text_caption(
            text,
            x,
            y,
            is_top_caption,
            horizontal_padding,
            vertical_padding,
            is_to_right=False,
        ):
            draw_func = None
            if is_to_right:
                draw_func = (
                    drawtext.DrawText().draw_singleline_text_by_hr_vb
                    if is_top_caption
                    else drawtext.DrawText().draw_singleline_text_by_hr_vt
                )
            else:
                draw_func = (
                    drawtext.DrawText().draw_singleline_text_by_hl_vb
                    if is_top_caption
                    else drawtext.DrawText().draw_singleline_text_by_hl_vt
                )
            #
            draw_func(
                get_painter_text_caption,
                text,
                x - horizontal_padding if is_to_right else x + horizontal_padding,
                y - vertical_padding if is_top_caption else y + vertical_padding,
            )

        def draw_to_right():
            length = pars.get_sp("to_left_and_to_right_arrow_length")
            delta = pars.get_sp("delta_node_and_to_right_arrow")
            #
            draw_line_and_arrow(self.__x, self.__y, -length, delta, "right")
            #
            text_physical = nf.get(self.__to_right_physical_length) + pars.get_sp(
                "постфикс_расстояния"
            )
            draw_text_caption(
                text_physical,
                self.__x,
                self.__y - delta,
                pars.get_sp("is_top_node_top_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=True,
            )
            #
            text_optical = nf.get(self.__to_right_optical_length) + pars.get_sp(
                "постфикс_расстояния"
            )
            draw_text_caption(
                text_optical,
                self.__x,
                self.__y + delta,
                pars.get_sp("is_top_node_bottom_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=True,
            )

        def draw_to_left():
            length = pars.get_sp("to_left_and_to_right_arrow_length")
            delta = pars.get_sp("delta_node_and_to_left_arrow")
            #
            draw_line_and_arrow(self.__x, self.__y, length, delta, "left")
            #
            text_physical = nf.get(self.__to_left_physical_length) + pars.get_sp(
                "постфикс_расстояния"
            )
            draw_text_caption(
                text_physical,
                self.__x,
                self.__y - delta,
                pars.get_sp("is_top_node_top_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=False,
            )
            #
            text_optical = nf.get(self.__to_left_optical_length) + pars.get_sp(
                "постфикс_расстояния"
            )

            draw_text_caption(
                text_optical,
                self.__x,
                self.__y + delta,
                pars.get_sp("is_top_node_bottom_caption"),
                pars.get_sp("node_caption_horizontal_padding"),
                pars.get_sp("node_caption_vertical_padding"),
                is_to_right=False,
            )

        def draw_tech_lengths():
            drawtext.DrawText().draw_singleline_text_by_hr_vc(
                get_painter_text_caption,
                pars.get_sp("text_cable_length"),
                self.__x - pars.get_sp("delta_x_text_lengths") * 2,
                self.__y - pars.get_sp("delta_y_text_lengths") * 2
            )
            drawtext.DrawText().draw_singleline_text_by_hr_vc(
                get_painter_text_caption,
                pars.get_sp("text_fiber_length"),
                self.__x - pars.get_sp("delta_x_text_lengths") * 2,
                self.__y + pars.get_sp("delta_y_text_lengths") * 2
            )
            

        #
        if not (self.__object_node.get_after_wrap() or not self.__object_before):
            draw_to_right()
        #
        if not (self.__object_node.get_before_wrap() or not self.__object_after):
            draw_to_left()

        if node_id == "51":
            drawobject.DrawObject().node_big_circle_and_triangle(
                get_painter_figure_border,
                self.__x,
                self.__y,
                node_border_radius,
            )

        # Рисование технических обозначений длин для первой вершины
        if self.__object_before is None:
            draw_tech_lengths()
        

        # Рисование вершины
        drawobject.DrawObject().node_circle(
            get_painter_figure_border,
            get_painter_figure_border_fill,
            self.__x,
            self.__y,
            pars.get_sp("node_radius"),
        )

        # Рисование названия
        text = data.get_sd("название")
        if data.get_sd("местоположение"):
            text += '\n' + data.get_sd("местоположение")
        drawtext.DrawText().draw_multiline_text_by_hc_vb(
            get_painter_text_name,
            text,
            self.__x,
            self.__y - pars.get_sp("node_name_height"),
            pars.get_sp("node_name_max_width")
        )






    def _draw_node_ids_100_101(self, pars, data, node_id, nf):


        def get_painter_figure_border():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_border(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
            )

        def get_painter_figure_border_fill():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_figure_border_fill(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
                fill_color=pars.get_sp("node_fill_color"),
                fill_pattern_name=pars.get_sp("node_fill_style"),
            )

        def get_painter_text_name():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_pixel_size"),
            )

        def get_painter_text_name_add():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_add_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_add_pixel_size"),
            )

        def get_painter_text_caption():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_text(
                color=pars.get_sp("node_caption_physics_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_caption_physics_pixel_size"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )

        # рисование wrap стрелки
        def draw_wrap_arrow(node_border_width):
            if pars.get_sp("is_wrap_arrow"):
                if self.__object_node.get_before_wrap():
                    drawobject.DrawObject().wrap_arrow(
                        get_painter_arrow,
                        get_painter_thin_line,
                        self.__x + node_border_width,
                        self.__y,
                        pars.get_sp("arrow_width"),
                        pars.get_sp("arrow_height"),
                        pars.get_sp("wrap_arrow_length"),
                        "before_wrap",
                    )
                elif self.__object_node.get_after_wrap():
                    drawobject.DrawObject().wrap_arrow(
                        get_painter_arrow,
                        get_painter_thin_line,
                        self.__x - node_border_width,
                        self.__y,
                        pars.get_sp("arrow_width"),
                        pars.get_sp("arrow_height"),
                        pars.get_sp("wrap_arrow_length"),
                        "after_wrap",
                    )

        def draw_node_id_100():
            # Рисование wrap стрелки
            draw_wrap_arrow(pars.get_sp("node_radius"))

            # Рисование вершины
            drawobject.DrawObject().node_circle(
                get_painter_figure_border,
                get_painter_figure_border_fill,
                self.__x,
                self.__y,
                pars.get_sp("node_radius"),
            )

            # Рисование названия
            text = data.get_sd("название")
            if data.get_sd("местоположение"):
                text += '\n' + data.get_sd("местоположение")
            drawtext.DrawText().draw_multiline_text_by_hc_vb(
                get_painter_text_name,
                text,
                self.__x,
                self.__y - pars.get_sp("node_name_height"),
                pars.get_sp("node_name_max_width")
            )

        def draw_node_id_101():
            # Рисование wrap стрелки
            draw_wrap_arrow(pars.get_sp("node_width") // 2)

            node_width = pars.get_sp("node_width")
            node_height = pars.get_sp("node_height")
            # Рисование вершины прямоугольника
            drawobject.DrawObject().node_reactangle(
                get_painter_figure_border,
                get_painter_figure_border_fill,
                self.__x,
                self.__y,
                node_width,
                node_height,
            )
            # Рисование названия
            text = data.get_sd("название")
            text_align_name = pars.get_sp("node_name_align")
            #
            if text_align_name == "LeftAlign":
                drawtext.DrawText().draw_multiline_text_by_hl_vb(
                    get_painter_text_name,
                    text,
                    self.__x - node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                    pars.get_sp("node_name_max_width")
                )
            elif text_align_name == "RightAlign":
                drawtext.DrawText().draw_multiline_text_by_hr_vb(
                    get_painter_text_name,
                    text,
                    self.__x + node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                    pars.get_sp("node_name_max_width")
                )
            else:
                drawtext.DrawText().draw_multiline_text_by_hc_vb(
                    get_painter_text_name,
                    text,
                    self.__x,
                    self.__y - pars.get_sp("node_name_height"),
                    pars.get_sp("node_name_max_width")
                )

            # Рисование диапазона c 24 по 48 (внутри прямоугольника)
            text = data.get_sd("название_доп")
            drawtext.DrawText().draw_multiline_text_by_hc_vc(
                get_painter_text_name_add, text, self.__x, self.__y
            )

        # рисование вершины
        if node_id == "100":
            draw_node_id_100()
        elif node_id == "101":
            draw_node_id_101()

        # рисование значения физической длины
        x = self.__x
        if node_id == "101" and (not self.__object_before or self.__object_node.get_after_wrap()):
            x += pars.get_sp("node_width") // 2
        elif node_id == "101" and (not self.__object_after or self.__object_node.get_before_wrap()):
            x -= pars.get_sp("node_width") // 2
        drawtext.DrawText().draw_singleline_text_rotated_by_hc_vt(
            get_painter_text_caption,
            nf.get(self.__to_right_physical_length) + pars.get_sp("постфикс_расстояния"),
            x,
            self.__y + pars.get_sp("node_caption_physics_vertical_padding"),
        )


    def _draw_node_ids_150_151(self, pars, data, node_id, nf):
    
        def get_painter_figure_border():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_border(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
            )

        def get_painter_figure_border_fill():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_figure_border_fill(
                pen_color=pars.get_sp("node_border_color"),
                pen_weight=pars.get_sp("node_border_weight"),
                fill_color=pars.get_sp("node_fill_color"),
                fill_pattern_name=pars.get_sp("node_fill_style"),
            )

        def get_painter_text_name():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_pixel_size"),
            )

        def get_painter_text_name_add():
            return painterconfigurator.PainterConfigurator(
                self.__painter,
            ).get_painter_text(
                color=pars.get_sp("node_name_add_color"),
                font_name=pars.get_sp("font_name"),
                pixel_size=pars.get_sp("node_name_add_pixel_size"),
            )

        def get_painter_thin_line():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_line(
                color=pars.get_sp("thin_line_color"),
                weight=pars.get_sp("thin_line_weight"),
                style_name="SolidLine",
            )

        def get_painter_arrow():
            return painterconfigurator.PainterConfigurator(
                self.__painter
            ).get_painter_figure_fill(
                fill_color=pars.get_sp("thin_line_color"),
                fill_pattern_name="SolidPattern",
            )
        

        
        # рисование wrap стрелки
        def draw_wrap_arrow(node_border_width):
            if pars.get_sp("is_wrap_arrow"):
                if self.__object_node.get_before_wrap():
                    drawobject.DrawObject().wrap_arrow(
                        get_painter_arrow,
                        get_painter_thin_line,
                        self.__x + node_border_width,
                        self.__y,
                        pars.get_sp("arrow_width"),
                        pars.get_sp("arrow_height"),
                        pars.get_sp("wrap_arrow_length"),
                        "before_wrap",
                    )
                elif self.__object_node.get_after_wrap():
                    drawobject.DrawObject().wrap_arrow(
                        get_painter_arrow,
                        get_painter_thin_line,
                        self.__x - node_border_width,
                        self.__y,
                        pars.get_sp("arrow_width"),
                        pars.get_sp("arrow_height"),
                        pars.get_sp("wrap_arrow_length"),
                        "after_wrap",
                    )

        def draw_node_id_150():
            # рисование wrap стрелки
            draw_wrap_arrow(pars.get_sp("node_radius"))
            # вершина
            drawobject.DrawObject().node_circle(
                get_painter_figure_border,
                get_painter_figure_border_fill,
                self.__x,
                self.__y,
                pars.get_sp("node_radius"),
            )
            # Рисование названия
            text = data.get_sd("название")
            if data.get_sd("местоположение"):
                text += '\n' + data.get_sd("местоположение")
            drawtext.DrawText().draw_multiline_text_by_hc_vb(
                get_painter_text_name,
                text,
                self.__x,
                self.__y - pars.get_sp("node_name_height"),
                pars.get_sp("node_name_max_width")
            )
            # УЖЕ НЕ НУЖНО Рисование номера (внутри круга)
            # text = str(self.__node_index + 1)
            # drawtext.DrawText().draw_multiline_text_by_hc_vc(
            #     get_painter_text_name_add, text, self.__x, self.__y
            # )

        
        def draw_node_id_151():
            node_width = pars.get_sp("node_width")
            # рисование wrap стрелки
            draw_wrap_arrow(node_width // 2)
            # вершина
            drawobject.DrawObject().node_reactangle(
                get_painter_figure_border,
                get_painter_figure_border_fill,
                self.__x,
                self.__y,
                node_width,
                pars.get_sp("node_height"),
            )
            # Рисование названия
            text = data.get_sd("название")

            text_align_name = pars.get_sp("node_name_align")
            #
            if text_align_name == "LeftAlign":
                drawtext.DrawText().draw_multiline_text_by_hl_vb(
                    get_painter_text_name,
                    text,
                    self.__x - node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                    pars.get_sp("node_name_max_width")
                )
            elif text_align_name == "RightAlign":
                drawtext.DrawText().draw_multiline_text_by_hr_vb(
                    get_painter_text_name,
                    text,
                    self.__x + node_width // 2,
                    self.__y - pars.get_sp("node_name_height"),
                    pars.get_sp("node_name_max_width")
                )
            else:
                drawtext.DrawText().draw_multiline_text_by_hc_vb(
                    get_painter_text_name,
                    text,
                    self.__x,
                    self.__y - pars.get_sp("node_name_height"),
                    pars.get_sp("node_name_max_width")
                )






        
        if node_id == "150":
            draw_node_id_150()
        elif node_id == "151":
            draw_node_id_151()


``
### D:\projects\net-constructor\package\modules\drawobject.py
``python
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QImage, QFont, QPolygon
from PySide6.QtCore import Qt, QPointF, QPoint, QRect

import package.modules.painterconfigurator as painterconfigurator
import package.modules.drawtext as drawtext


class DrawObject:
    def __init__(self):
        self.__painter = None

    def node_circle(
        self, painter_figure_border, painter_figure_border_fill, x, y, node_radius
    ):
        self.__painter = painter_figure_border()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)
        #
        self.__painter = painter_figure_border_fill()
        self.__painter.drawEllipse(QPoint(x, y), node_radius, node_radius)

    def node_big_circle_and_triangle(self, painter_figure_border, x, y, node_border_radius):
        # Рисуем круг и треугольник
        points = QPolygon(
            [
                QPoint(x, y - node_border_radius),
                QPoint(x - node_border_radius * 0.865, y + node_border_radius // 2),
                QPoint(x + node_border_radius * 0.865, y + node_border_radius // 2),
            ]
        )
        self.__painter = painter_figure_border()
        self.__painter.drawEllipse(
            QPoint(x, y), node_border_radius, node_border_radius
        )
        self.__painter.drawPolygon(points)

    def node_reactangle(self, painter_figure_border, painter_figure_border_fill, center_x, center_y, width, height):
        self.__painter = painter_figure_border()
        self.__painter.drawRect(QRect(center_x - width // 2, center_y - height // 2, width, height))
        #
        self.__painter = painter_figure_border_fill()
        self.__painter.drawRect(QRect(center_x - width // 2, center_y - height // 2, width, height))


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
            self.__painter.drawPolygon(points)
        #
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

    def wrap_arrow(
        self, painter_arrow, painter_line, x, y, width, height, length, type_wrap
    ):
        # only right direction
        if type_wrap == "before_wrap":
            # стрелка
            self.arrow(painter_arrow, x + length, y, width, height, "right")
            #
            self.__painter = painter_line()
            self.__painter.drawLine(QPoint(x, y), QPoint(x + length, y))

        elif type_wrap == "after_wrap":
            # стрелка
            self.arrow(painter_arrow, x, y, width, height, "right")
            # линия
            self.__painter = painter_line()
            self.__painter.drawLine(QPoint(x - length, y), QPoint(x, y))

``
### D:\projects\net-constructor\package\modules\drawtext.py
``python
class DrawText:
    def __init__(self):
        self.__painter = None

    def _wrap_text_to_width(self, text, max_width=None):
        if max_width is None or max_width <= 0:
            return text.split("\n")

        wrapped_lines = []
        for original_line in text.split("\n"):
            if not original_line.strip():
                wrapped_lines.append(original_line)
                continue

            words = original_line.split()
            current_line = []
            current_line_width = 0

            for word in words:
                word_width = self.__painter.fontMetrics().horizontalAdvance(word)

                # Если слово не помещается в текущую строку
                if current_line and (current_line_width + word_width) > max_width:
                    # Если слово слишком длинное для пустой строки - разбиваем посимвольно
                    if word_width > max_width:
                        # Добавляем текущую строку, если она не пустая
                        if current_line:
                            wrapped_lines.append(" ".join(current_line))
                            current_line = []
                            current_line_width = 0

                        # Разбиваем слово посимвольно
                        chars = list(word)
                        current_word_part = []
                        current_part_width = 0

                        for char in chars:
                            char_width = self.__painter.fontMetrics().horizontalAdvance(
                                char
                            )
                            if current_part_width + char_width > max_width:
                                wrapped_lines.append("".join(current_word_part))
                                current_word_part = [char]
                                current_part_width = char_width
                            else:
                                current_word_part.append(char)
                                current_part_width += char_width

                        if current_word_part:
                            wrapped_lines.append("".join(current_word_part))
                    else:
                        # Переносим слово на следующую строку
                        wrapped_lines.append(" ".join(current_line))
                        current_line = [word]
                        current_line_width = word_width
                else:
                    # Добавляем слово в текущую строку
                    current_line.append(word)
                    current_line_width += (
                        word_width + self.__painter.fontMetrics().horizontalAdvance(" ")
                    )  # добавляем пробел

            # Добавляем оставшиеся слова
            if current_line:
                wrapped_lines.append(" ".join(current_line))

        return wrapped_lines

    def draw_multiline_text_by_hl_vb(
        self, painter_text, text, left_x, bottom_y, max_width=None
    ):
        """По левому краю по горизонтали и по низу по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
        # Вычисляем начальную y-координату для рисования так, чтобы нижний край совпадал с bottom_y
        text_y = bottom_y
        # Рисуем каждую строку текста
        for line in reversed(lines):
            self.__painter.drawText(left_x, text_y, line)
            text_y -= self.__painter.fontMetrics().height()

    def draw_multiline_text_by_hr_vb(
        self, painter_text, text, right_x, bottom_y, max_width=None
    ):
        """По правому краю по горизонтали и по низу по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
        # Вычисляем начальную y-координату для рисования так, чтобы нижний край совпадал с bottom_y
        text_y = bottom_y
        # Рисуем каждую строку текста
        for line in reversed(lines):
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            text_x = right_x - text_width  # выравнивание по правому краю
            self.__painter.drawText(text_x, text_y, line)
            text_y -= self.__painter.fontMetrics().height()

    def draw_multiline_text_by_hc_vb(
        self, painter_text, text, center_x, bottom_y, max_width=None
    ):
        self.__painter = painter_text()
        """По центру по горизонтали и по низу по вертикали"""
        lines = self._wrap_text_to_width(text, max_width)
        # Вычисляем начальную y-координату для рисования так, чтобы нижний край совпадал с bottom_y
        start_y = bottom_y
        # Рисуем каждую строку текста
        text_y = start_y
        for line in reversed(lines):
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            # Центрируем каждую строку относительно center_x
            text_x = center_x - text_width // 2
            self.__painter.drawText(text_x, text_y, line)
            text_y -= self.__painter.fontMetrics().height()

    def draw_multiline_text_by_hc_vt(
        self, painter_text, text, center_x, top_y, max_width=None
    ):
        """По центру по горизонтали и по верху по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
        # Вычисляем начальную y-координату для рисования так, чтобы верхний край совпадал с top_y
        start_y = top_y + self.__painter.fontMetrics().height() * 0.618
        # Рисуем каждую строку текста
        text_y = start_y
        for line in lines:
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            # Центрируем каждую строку относительно center_x
            text_x = center_x - text_width // 2
            self.__painter.drawText(text_x, text_y, line)
            text_y += self.__painter.fontMetrics().height()

    def draw_multiline_text_by_hc_vc(
        self, painter_text, text, center_x, center_y, max_width=None
    ):
        """По центру по горизонтали и по центру по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
        total_text_height = len(lines) * self.__painter.fontMetrics().height()
        # * 0.618
        start_y = (
            center_y
            - (total_text_height // 2)
            + (self.__painter.fontMetrics().height() // 2)
        ) + self.__painter.fontMetrics().height() * 0.618 // 2
        # Рисуем каждую строку текста
        text_y = start_y
        for line in lines:
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            # Центрируем каждую строку относительно center_x
            text_x = center_x - text_width // 2
            self.__painter.drawText(text_x, text_y, line)
            text_y += self.__painter.fontMetrics().height()

    def draw_singleline_text_rotated_by_hc_vt(
        self, painter_text, text, center_x, top_y
    ):
        self.__painter = painter_text()
        self.__painter.save()
        self.__painter.translate(center_x, top_y)
        self.__painter.rotate(-90)
        #
        self.draw_singleline_text_by_hr_vc(painter_text, text, 0, 0)
        #
        self.__painter.restore()

    def draw_singleline_text_by_hr_vc(self, painter_text, text, right_x, center_y):
        self.__painter = painter_text()
        #
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        text_height = self.__painter.fontMetrics().height() * 0.618
        #
        text_x = right_x - text_width
        text_y = center_y + text_height // 2
        self.__painter.drawText(text_x, text_y, text)

    def draw_singleline_text_by_hl_vb(self, painter_text, text, left_x, bottom_y):
        self.__painter = painter_text()
        text_y = bottom_y
        self.__painter.drawText(left_x, text_y, text)

    def draw_singleline_text_by_hl_vt(self, painter_text, text, left_x, top_y):
        self.__painter = painter_text()
        text_y = top_y + self.__painter.fontMetrics().height() * 0.618
        self.__painter.drawText(left_x, text_y, text)

    def draw_singleline_text_by_hr_vb(self, painter_text, text, right_x, bottom_y):
        self.__painter = painter_text()
        # Вычисляем ширину текста
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        # Рассчитываем начальную x-координату для выравнивания по правому краю
        text_x = right_x - text_width
        text_y = bottom_y
        # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
        self.__painter.drawText(text_x, text_y, text)

    def draw_singleline_text_by_hr_vt(self, painter_text, text, right_x, top_y):
        self.__painter = painter_text()
        # Вычисляем ширину текста
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        # Рассчитываем начальную x-координату для выравнивания по правому краю
        text_x = right_x - text_width
        text_y = top_y + self.__painter.fontMetrics().height() * 0.618
        # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
        self.__painter.drawText(text_x, text_y, text)

``
### D:\projects\net-constructor\package\modules\numberformatter.py
``python
class NumberFormatter:

    def __init__(self):
        self.__precision_number = 0
        self.__precision_separator = 1
    
    def set_precision_number(self, precision_number):
        self.__precision_number = precision_number

    def set_precision_separator(self, precision_separator):
        self.__precision_separator = precision_separator

    def get(self, number_input):
        try:
            number_float = float(number_input)
        except ValueError:
            return ""

        format_string = f"{{:.{self.__precision_number}f}}"
        formatted_number = format_string.format(number_float)       
        separator = '.' if self.__precision_separator == 1 else ','
        formatted_number = formatted_number.replace('.', separator) if separator == ',' else formatted_number
        return formatted_number


``
### D:\projects\net-constructor\package\modules\painterconfigurator.py
``python
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

``
### D:\projects\net-constructor\package\modules\project.py
``python
# project.py

import json
import uuid
import copy

import package.constants as constants


class Project:
    def __init__(self) -> None:
        self.__file_name = None
        self.__data = None
        self.__copied_node_data = None
        self.__copied_connection_data = None
        self.__copied_control_sector_data = None

    def get_data(self):
        return self.__data

    def create_new_project(self, diagram_data, control_sectors_config, file_path):
        self.__file_name = file_path
        self.__data = {
            "diagram_type_id": diagram_data.get("type_id", "0"),
            "diagram_name": diagram_data.get("name", ""),
            "diagram_parameters": diagram_data.get("parameters", {}),
            "control_sectors_config": control_sectors_config,
            "nodes": [],
            "connections": [],
            "archived_parameters": {},
        }
        #
        self._write_project()

    def is_active(self):
        return self.__file_name

    def open_project(self, file_path):
        self.__file_name = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            self.__data = json.load(f)

    def save_as_project(self, file_path):
        self.__file_name = file_path
        self._write_project()

    def _write_project(self):
        if self.__file_name:
            with open(self.__file_name, "w", encoding="utf-8") as f:
                json.dump(self.__data, f, indent=4, ensure_ascii=False)

    def change_type_diagram(self, new_diagram, config_nodes, config_connections):
        # Сохраняем текущие параметры в архив
        current_type_id = self.__data["diagram_type_id"]

        # Инициализируем архив для текущего типа диаграммы, если его еще нет
        if current_type_id not in self.__data["archived_parameters"]:
            self.__data["archived_parameters"][current_type_id] = {
                "nodes": {},
                "connections": {},
                "diagram_parameters": {},  # Добавляем архив для diagram_parameters
            }

        # Сохраняем параметры узлов
        for node in self.__data["nodes"]:
            node_id = node["id"]
            self.__data["archived_parameters"][current_type_id]["nodes"][node_id] = {
                "parameters": node["parameters"]
            }

        # Сохраняем параметры соединений
        for connection in self.__data["connections"]:
            connection_id = connection["id"]
            self.__data["archived_parameters"][current_type_id]["connections"][
                connection_id
            ] = {"parameters": connection["parameters"]}

        # Сохраняем текущие diagram_parameters в архив
        self.__data["archived_parameters"][current_type_id]["diagram_parameters"] = (
            copy.deepcopy(self.__data["diagram_parameters"])
        )

        # Обновляем тип схемы и параметры
        new_diagram_type_id = new_diagram.get("type_id", "0")
        self._update_diagram_nodes(new_diagram_type_id, config_nodes)
        self._update_diagram_connections(new_diagram_type_id, config_connections)

        # Восстанавливаем параметры из архива, если они есть, иначе выбираем параметры из новой диаграммы
        if new_diagram_type_id in self.__data["archived_parameters"]:
            archived_params = self.__data["archived_parameters"][new_diagram_type_id]

            # Восстанавливаем параметры узлов / соединений
            for node in self.__data["nodes"]:
                node_id = node["id"]
                if node_id in archived_params["nodes"]:
                    node["parameters"] = archived_params["nodes"][node_id]["parameters"]

            for connection in self.__data["connections"]:
                connection_id = connection["id"]
                if connection_id in archived_params["connections"]:
                    connection["parameters"] = archived_params["connections"][
                        connection_id
                    ]["parameters"]

            # Восстанавливаем diagram_parameters из архива
            self.__data["diagram_parameters"] = archived_params.get(
                "diagram_parameters", {}
            )
        else:
            # Если нет архива для нового типа диаграммы, используем параметры из новой диаграммы
            self.__data["diagram_parameters"] = new_diagram.get("parameters", {})

        # Обновляем данные диаграммы
        self.__data["diagram_type_id"] = new_diagram_type_id
        self.__data["diagram_name"] = new_diagram.get("name", "")
        self._write_project()

    def set_new_order_nodes(self, new_order_nodes):
        print(f"set_new_order_nodes():\nnew_order_nodes={new_order_nodes}\n")
        nodes = []
        for index, node in enumerate(new_order_nodes):
            node["order"] = index
            nodes.append(node)
        # Это рискованно но ладно
        self.__data["nodes"] = new_order_nodes

    def set_new_order_connections(self, new_order_connections):
        print(
            "set_new_order_connections():\n"
            f"new_order_connections={new_order_connections}\n"
        )
        connections = []
        for index, connection in enumerate(new_order_connections):
            connection["order"] = index
            connections.append(connection)
        # Это рискованно но ладно
        self.__data["connections"] = new_order_connections

    def set_new_order_control_sectors(self, obj, new_order_control_sectors):
        # TODO set_new_order_control_sectors - проверить
        print(
            "set_new_order_control_sectors():\n"
            f"new_order_control_sectors={new_order_control_sectors}\n"
        )
        control_sectors = []
        for index, control_sector in enumerate(new_order_control_sectors):
            control_sector["order"] = index
            control_sectors.append(control_sector)
        #
        connection_id = obj.get("id")
        for connection in self.__data.get("connections", []):
            if connection["id"] == connection_id:
                connection["control_sectors"] = control_sectors
                break
        self._write_project()
        return control_sectors

    def add_pair(self, key_dict_node_and_key_dict_connection):
        key_dict_node = key_dict_node_and_key_dict_connection.get("node")
        #
        key_dict_connection = key_dict_node_and_key_dict_connection.get("connection")
        #
        if len(self.__data.get("nodes", [])) == 0:
            self._add_node(key_dict_node)
        else:
            self._add_node(key_dict_node)
            self._add_connection(key_dict_connection)
        self._write_project()

    def add_control_sector(
        self, obj, name=None, physical_length=None, length=None, penultimate=False
    ) -> list:
        """Добавляет контрольный сектор с возможностью указания параметров по умолчанию"""
        connection_id = obj.get("id")
        control_sectors_return = []

        for connection in self.__data.get("connections", []):
            if connection["id"] == connection_id:
                new_id = uuid.uuid4().hex
                new_order = len(connection.get("control_sectors", []))
                if penultimate:
                    new_order -= 1
                new_config = copy.deepcopy(
                    self.__data.get("control_sectors_config", {})
                )

                # Устанавливаем значения по умолчанию, если они переданы
                if name is not None:
                    new_config["cs_name"]["value"] = name
                if physical_length is not None:
                    new_config["cs_physical_length"]["value"] = physical_length
                if length is not None:
                    new_config["cs_lenght"]["value"] = length

                new_control_sector = {
                    "id": new_id,
                    "order": new_order,
                    "is_wrap": False,
                    "data_pars": new_config,
                }
                #
                # Если указана позиция вставки и она валидна
                if penultimate:
                    connection["control_sectors"].insert(new_order, new_control_sector)
                else:
                    # Иначе добавляем в конец
                    connection["control_sectors"].append(new_control_sector)

                # Обновляем порядок всех секторов
                for index, cs in enumerate(connection["control_sectors"]):
                    cs["order"] = index

                control_sectors_return = connection.get("control_sectors", [])
                break

        self._write_project()
        return control_sectors_return

    def _update_diagram_nodes(self, new_diagram_type_id, config_nodes):
        dtd = constants.DiagramToDiagram()
        for node in self.__data.get("nodes", []):
            old_node_id = node.get("node_id")
            new_node_id = dtd.get_new_type_id(
                new_diagram_type_id,
                old_node_id,
                is_node=True,
            )
            node["node_id"] = new_node_id if new_node_id else old_node_id
            node["parameters"] = self._get_combined_parameters(
                config_nodes.get(new_node_id, {})
            )

    def _update_diagram_connections(self, new_diagram_type_id, config_connections):
        dtd = constants.DiagramToDiagram()
        for connection in self.__data.get("connections", []):
            old_connection_id = connection.get("connection_id")
            new_connection_id = dtd.get_new_type_id(
                new_diagram_type_id,
                old_connection_id,
                is_node=False,
            )
            connection["connection_id"] = (
                new_connection_id if new_connection_id else old_connection_id
            )
            connection["parameters"] = self._get_combined_parameters(
                config_connections.get(new_connection_id, {})
            )

    def _get_combined_data(self, object_dict):
        return {
            **object_dict.get("object_data", {}),
            **object_dict.get("type_object_data", {}),
            **object_dict.get("objects_data", {}),
        }

    def _get_combined_parameters(self, object_dict):
        return {
            **object_dict.get("object_parameters", {}),
            **object_dict.get("type_object_parameters", {}),
            **object_dict.get("objects_parameters", {}),
        }

    def _add_node(self, key_dict_node):
        node_key = key_dict_node.get("node_key")
        node_dict = key_dict_node.get("node_dict")

        new_id = uuid.uuid4().hex
        new_order = len(self.__data.get("nodes", []))

        # Получаем данные и параметры по умолчанию из конфигурации
        default_data = self._get_combined_data(node_dict)
        default_parameters = self._get_combined_parameters(node_dict)

        # Для objects_data/objects_parameters берем значения из любого существующего объекта
        if self.__data.get("nodes"):
            first_existing_node = self.__data["nodes"][0]
            self._update_objects_values(
                first_existing_node, node_dict, default_data, default_parameters
            )

        # Для type_object_data/type_object_parameters берем значения из объектов с тем же node_id
        existing_nodes = [
            n for n in self.__data.get("nodes", []) if n["node_id"] == node_key
        ]
        if existing_nodes:
            self._update_type_values(
                existing_nodes[0], node_dict, default_data, default_parameters
            )

        new_is_wrap = node_dict.get("is_wrap", False)

        new_dict = {
            "id": new_id,
            "order": new_order,
            "node_id": node_key,
            "data": default_data,
            "is_wrap": new_is_wrap,
            "parameters": default_parameters,
        }
        self.__data["nodes"].append(new_dict)

    def _add_connection(self, key_dict_connection):
        connection_key = key_dict_connection.get("connection_key")
        connection_dict = key_dict_connection.get("connection_dict")

        new_id = uuid.uuid4().hex
        new_order = len(self.__data.get("connections", []))

        # Получаем данные и параметры по умолчанию из конфигурации
        default_data = self._get_combined_data(connection_dict)
        default_parameters = self._get_combined_parameters(connection_dict)

        # Для objects_data/objects_parameters берем значения из любого существующего объекта
        if self.__data.get("connections"):
            first_existing_connection = self.__data["connections"][0]
            self._update_objects_values(
                first_existing_connection,
                connection_dict,
                default_data,
                default_parameters,
            )

        # Для type_object_data/type_object_parameters берем значения из объектов с тем же connection_id
        existing_connections = [
            c
            for c in self.__data.get("connections", [])
            if c["connection_id"] == connection_key
        ]
        if existing_connections:
            self._update_type_values(
                existing_connections[0],
                connection_dict,
                default_data,
                default_parameters,
            )

        new_dict = {
            "id": new_id,
            "order": new_order,
            "connection_id": connection_key,
            "data": default_data,
            "parameters": default_parameters,
            "control_sectors": [],
        }
        self.__data["connections"].append(new_dict)

        # Добавляем 3 сектора по умолчанию
        self._add_default_control_sectors(new_dict)

        self._write_project()

    def _add_default_control_sectors(self, connection):
        """Добавляет 3 сектора по умолчанию для нового соединения"""
        # Получаем конфигурацию секторов
        config = self.__data.get("control_sectors_config", {})

        # Получаем ID узлов, к которым прилегает соединение
        nodes = self.__data.get("nodes", [])
        connection_order = connection.get("order", 0)

        # Определяем тип левого и правого узлов
        left_node = nodes[connection_order] if connection_order < len(nodes) else None
        right_node = (
            nodes[connection_order + 1] if connection_order + 1 < len(nodes) else None
        )

        # Добавляем первый сектор (тех. запас)
        tech_name = config.get("cs_tech_name_default", {}).get("value", "Тех. запас")
        tech_length = config.get("cs_tech_lenght_default", {}).get("value", 140)

        # Определяем физическую длину для первого тех. запаса
        if left_node and left_node.get("node_id") in ["1", "51", "101", "151"]:  # Кросс
            tech_phys_length = config.get("cs_tech_cross_lenght_default", {}).get(
                "value", 10
            )
        else:  # Муфта
            tech_phys_length = config.get(
                "cs_tech_mufta_physical_length_default", {}
            ).get("value", 15)

        # Создаем первый тех. запас
        self.add_control_sector(
            connection,
            name=tech_name,
            physical_length=tech_phys_length,
            length=tech_length,
        )

        # Добавляем средний сектор (основной)
        main_name = config.get("cs_name", {}).get("value", "Сектор")
        main_length = config.get("cs_lenght", {}).get("value", 200)
        self.add_control_sector(
            connection,
            name=main_name,
            physical_length=0,  # По умолчанию не заполнено
            length=main_length,
        )

        # Добавляем второй тех. запас
        if right_node and right_node.get("node_id") in [
            "1",
            "51",
            "101",
            "151",
        ]:  # Кросс
            tech_phys_length = config.get("cs_tech_cross_lenght_default", {}).get(
                "value", 10
            )
        else:  # Муфта
            tech_phys_length = config.get(
                "cs_tech_mufta_physical_length_default", {}
            ).get("value", 15)

        self.add_control_sector(
            connection,
            name=tech_name,
            physical_length=tech_phys_length,
            length=tech_length,
        )

    def _update_objects_values(
        self, existing_obj, config_dict, default_data, default_parameters
    ):
        """Обновляет objects_data и objects_parameters из любого существующего объекта"""
        # Обновляем objects_data
        objects_data = config_dict.get("objects_data", {})
        for key in objects_data:
            if key in existing_obj["data"]:
                default_data[key] = existing_obj["data"][key]

        # Обновляем objects_parameters
        objects_parameters = config_dict.get("objects_parameters", {})
        for key in objects_parameters:
            if key in existing_obj["parameters"]:
                default_parameters[key] = existing_obj["parameters"][key]

    def _update_type_values(
        self, existing_obj, config_dict, default_data, default_parameters
    ):
        """Обновляет type_object_data и type_object_parameters из объектов с тем же типом"""
        # Обновляем type_object_data
        type_object_data = config_dict.get("type_object_data", {})
        for key in type_object_data:
            if key in existing_obj["data"]:
                default_data[key] = existing_obj["data"][key]

        # Обновляем type_object_parameters
        type_object_parameters = config_dict.get("type_object_parameters", {})
        for key in type_object_parameters:
            if key in existing_obj["parameters"]:
                default_parameters[key] = existing_obj["parameters"][key]

    def delete_pair(self, node, connection):
        if node:
            delete_id = node.get("id", "")
            if delete_id:
                self.__data["nodes"] = list(
                    filter(lambda x: x.get("id", "") != delete_id, self.__data["nodes"])
                )
                sorted_nodes = sorted(
                    self.__data["nodes"], key=lambda x: x.get("order", 0)
                )
                self.__data["nodes"] = []
                for index, node in enumerate(sorted_nodes):
                    node["order"] = index
                    self.__data["nodes"].append(node)
        if connection:
            delete_id = connection.get("id", "")
            if delete_id:
                self.__data["connections"] = list(
                    filter(
                        lambda x: x.get("id", "") != delete_id,
                        self.__data["connections"],
                    )
                )
                sorted_connections = sorted(
                    self.__data["connections"], key=lambda x: x.get("order", 0)
                )
                self.__data["connections"] = []
                for index, connection in enumerate(sorted_connections):
                    connection["order"] = index
                    self.__data["connections"].append(connection)
        self._write_project()

    def delete_control_sector(self, obj, selected_cs) -> list:
        connection_id = obj.get("id")
        control_sectors_return = []
        for connection in self.__data.get("connections", []):
            if connection["id"] == connection_id:
                # удаляем кт
                control_sectors = connection.get("control_sectors", [])
                control_sectors = [
                    cs for cs in control_sectors if cs["id"] != selected_cs["id"]
                ]
                # обновляем порядок оставшихся кт
                for index, cs in enumerate(control_sectors):
                    cs["order"] = index
                # обновляем список кт
                connection["control_sectors"] = control_sectors
                control_sectors_return = control_sectors
                break
        self._write_project()
        return control_sectors_return

    def wrap_node(self, node):
        _id = node.get("id", "")
        for node in self.__data["nodes"]:
            if node["id"] == _id:
                node["is_wrap"] = not node.get("is_wrap", True)
                break
        self._write_project()

    def save_project(
        self,
        obj,
        is_node,
        is_general_tab,
        is_editor_tab,
        config_nodes,
        config_connections,
        diagram_type_id,
        diagram_name,
        new_diagram_parameters,
        new_data,
        new_parameters,
    ):
        # Проверка на вкладку
        if is_general_tab:
            self.__data["diagram_type_id"] = diagram_type_id
            self.__data["diagram_name"] = diagram_name
            #
            for key, value in new_diagram_parameters.items():
                self.__data["diagram_parameters"][key] = value
        elif is_editor_tab:
            if is_node:
                _id = obj.get("id", "")
                for node in self.__data.get("nodes", []):
                    if node["id"] == _id:
                        for key, value in new_data.items():
                            self._check_empty_data_key(node, key)
                            node["data"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=False,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=False,
                            )
                        for key, value in new_parameters.items():
                            self._check_empty_parameters_key(node, key)
                            node["parameters"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=True,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=True,
                                is_parameter=True,
                            )
                        break
            else:
                _id = obj.get("id", "")
                for connection in self.__data.get("connections", []):
                    if connection["id"] == _id:
                        for key, value in new_data.items():
                            self._check_empty_data_key(connection, key)
                            connection["data"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=False,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=False,
                            )
                        for key, value in new_parameters.items():
                            self._check_empty_parameters_key(connection, key)
                            connection["parameters"][key] = value
                            self._check_type_object_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=True,
                            )
                            self._check_objects_key(
                                config_nodes,
                                config_connections,
                                obj,
                                key,
                                is_node=False,
                                is_parameter=True,
                            )
                        break
        self._write_project()

    def _check_empty_parameters_key(self, object, key):
        if key not in object["parameters"]:
            object["parameters"][key] = {}

    def _check_empty_data_key(self, object, key):
        if key not in object["data"]:
            object["data"][key] = {}

    def _check_type_object_key(
        self,
        config_nodes,
        config_connections,
        obj,
        key,
        is_node=False,
        is_parameter=True,
    ):
        obj_id = obj.get("node_id" if is_node else "connection_id", "")
        #
        config_dict = config_nodes if is_node else config_connections
        obj_dict = config_dict.get(obj_id, {})
        #
        type_object_key = (
            "type_object_parameters" if is_parameter else "type_object_data"
        )
        is_type_object = obj_dict.get(type_object_key, {}).get(key, {})
        if is_type_object:
            target_section = "parameters" if is_parameter else "data"
            value = obj[target_section].get(key, {}).get("value", None)
            if value is not None:
                data_section = "nodes" if is_node else "connections"
                for other_obj in self.__data.get(data_section, []):
                    if (
                        other_obj.get("node_id" if is_node else "connection_id", "")
                        == obj_id
                    ):
                        other_obj[target_section][key] = {"value": value}

    def _check_objects_key(
        self,
        config_nodes,
        config_connections,
        obj,
        key,
        is_node=False,
        is_parameter=True,
    ):
        print("_check_objects_key")
        obj_id = obj.get("node_id" if is_node else "connection_id", "")
        #
        config_dict = config_nodes if is_node else config_connections
        obj_dict = config_dict.get(obj_id, {})
        #
        objects_key = "objects_parameters" if is_parameter else "objects_data"
        is_objects = obj_dict.get(objects_key, {}).get(key, {})
        if is_objects:
            target_section = "parameters" if is_parameter else "data"
            value = obj[target_section].get(key, {}).get("value", None)
            if value is not None:
                data_section = "nodes" if is_node else "connections"
                print("data_section", data_section)
                print("key", key, "value", value)
                for other_obj in self.__data.get(data_section, []):
                    other_obj[target_section][key] = {"value": value}

    def copy_node_data(self, node):
        """Копирует данные вершины (только data)"""
        self.__copied_node_data = copy.deepcopy(node.get("data", {}))

    def paste_node_data(self, node):
        """Вставляет данные в вершину (только data)"""
        if self.__copied_node_data:
            node["data"] = copy.deepcopy(self.__copied_node_data)
            self._write_project()

    def has_copied_node_data(self):
        """Проверяет, есть ли скопированные данные вершины"""
        return self.__copied_node_data is not None

    def copy_connection_data(self, connection):
        """Копирует данные соединения (только data)"""
        self.__copied_connection_data = copy.deepcopy(connection.get("data", {}))

    def paste_connection_data(self, connection):
        """Вставляет данные в соединение (только data)"""
        if self.__copied_connection_data:
            connection["data"] = copy.deepcopy(self.__copied_connection_data)
            self._write_project()

    def has_copied_connection_data(self):
        """Проверяет, есть ли скопированные данные соединения"""
        return self.__copied_connection_data is not None

    def copy_control_sector_data(self, control_sector):
        """Копирует данные контрольного сектора (только data_pars)"""
        self.__copied_control_sector_data = copy.deepcopy(
            control_sector.get("data_pars", {})
        )

    def paste_control_sector_data(self, control_sector):
        """Вставляет данные в контрольный сектор (только data_pars)"""
        if self.__copied_control_sector_data:
            control_sector["data_pars"] = copy.deepcopy(
                self.__copied_control_sector_data
            )
            self._write_project()

    def has_copied_control_sector_data(self):
        """Проверяет, есть ли скопированные данные контрольного сектора"""
        return self.__copied_control_sector_data is not None

``
### D:\projects\net-constructor\package\ui\mainwindow_ui.py
``python
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from package.controllers.imagewidget import ImageWidget

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1144, 653)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setStyleSheet(u"")
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        icon = QIcon()
        iconThemeName = u"document-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u":/white-icons/resources/white-icons/add-file.svg", QSize(), QIcon.Normal, QIcon.Off)
        
        self.action_new.setIcon(icon)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        icon1 = QIcon()
        icon1.addFile(u":/white-icons/resources/white-icons/open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_open.setIcon(icon1)
        self.action_saveas = QAction(MainWindow)
        self.action_saveas.setObjectName(u"action_saveas")
        self.action_saveas.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u":/white-icons/resources/white-icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_saveas.setIcon(icon2)
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save.setEnabled(False)
        self.action_save.setIcon(icon2)
        self.action_zoomin = QAction(MainWindow)
        self.action_zoomin.setObjectName(u"action_zoomin")
        self.action_zoomin.setEnabled(False)
        icon3 = QIcon()
        icon3.addFile(u":/white-icons/resources/white-icons/zoom-in.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomin.setIcon(icon3)
        self.action_zoomin.setMenuRole(QAction.TextHeuristicRole)
        self.action_zoomout = QAction(MainWindow)
        self.action_zoomout.setObjectName(u"action_zoomout")
        self.action_zoomout.setEnabled(False)
        icon4 = QIcon()
        icon4.addFile(u":/white-icons/resources/white-icons/zoom-out.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomout.setIcon(icon4)
        self.action_zoomout.setMenuRole(QAction.TextHeuristicRole)
        self.action_edit_variables = QAction(MainWindow)
        self.action_edit_variables.setObjectName(u"action_edit_variables")
        self.action_edit_variables.setEnabled(False)
        icon5 = QIcon()
        icon5.addFile(u":/white-icons/resources/white-icons/text-editor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_variables.setIcon(icon5)
        self.action_zoomfitpage = QAction(MainWindow)
        self.action_zoomfitpage.setObjectName(u"action_zoomfitpage")
        self.action_zoomfitpage.setCheckable(True)
        self.action_zoomfitpage.setEnabled(False)
        icon6 = QIcon()
        icon6.addFile(u":/white-icons/resources/white-icons/zoom-fit-width.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_zoomfitpage.setIcon(icon6)
        self.action_zoomfitpage.setMenuRole(QAction.TextHeuristicRole)
        self.action_export_to_image = QAction(MainWindow)
        self.action_export_to_image.setObjectName(u"action_export_to_image")
        self.action_export_to_image.setEnabled(False)
        icon7 = QIcon()
        icon7.addFile(u":/white-icons/resources/white-icons/export.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_export_to_image.setIcon(icon7)
        self.action_edit_templates = QAction(MainWindow)
        self.action_edit_templates.setObjectName(u"action_edit_templates")
        self.action_edit_templates.setEnabled(False)
        icon8 = QIcon()
        icon8.addFile(u":/white-icons/resources/white-icons/template.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_templates.setIcon(icon8)
        self.action_edit_templates.setMenuRole(QAction.TextHeuristicRole)
        self.action_edit_composition = QAction(MainWindow)
        self.action_edit_composition.setObjectName(u"action_edit_composition")
        self.action_edit_composition.setEnabled(False)
        icon9 = QIcon()
        icon9.addFile(u":/white-icons/resources/white-icons/items-tree.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_edit_composition.setIcon(icon9)
        self.action_edit_composition.setMenuRole(QAction.TextHeuristicRole)
        self.action_clear_trash = QAction(MainWindow)
        self.action_clear_trash.setObjectName(u"action_clear_trash")
        icon10 = QIcon()
        icon10.addFile(u":/white-icons/resources/white-icons/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_clear_trash.setIcon(icon10)
        self.action_parameters = QAction(MainWindow)
        self.action_parameters.setObjectName(u"action_parameters")
        self.action_parameters.setCheckable(True)
        icon11 = QIcon()
        icon11.addFile(u":/white-icons/resources/white-icons/show-properties.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_parameters.setIcon(icon11)
        self.light_action = QAction(MainWindow)
        self.light_action.setObjectName(u"light_action")
        self.dark_action = QAction(MainWindow)
        self.dark_action.setObjectName(u"dark_action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 0, 4, 0)
        self.centralwidget_splitter = QSplitter(self.centralwidget)
        self.centralwidget_splitter.setObjectName(u"centralwidget_splitter")
        self.centralwidget_splitter.setOrientation(Qt.Horizontal)
        self.gb_center = QGroupBox(self.centralwidget_splitter)
        self.gb_center.setObjectName(u"gb_center")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gb_center.sizePolicy().hasHeightForWidth())
        self.gb_center.setSizePolicy(sizePolicy1)
        self.gb_center.setMinimumSize(QSize(350, 0))
        self.gb_center.setFlat(False)
        self.gb_center.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.gb_center)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.imagewidget = ImageWidget(self.gb_center)
        self.imagewidget.setObjectName(u"imagewidget")
        self.imagewidget.setEnabled(True)

        self.verticalLayout.addWidget(self.imagewidget)

        self.verticalLayout.setStretch(0, 1)
        self.centralwidget_splitter.addWidget(self.gb_center)
        self.gb_right = QGroupBox(self.centralwidget_splitter)
        self.gb_right.setObjectName(u"gb_right")
        sizePolicy1.setHeightForWidth(self.gb_right.sizePolicy().hasHeightForWidth())
        self.gb_right.setSizePolicy(sizePolicy1)
        self.gb_right.setMinimumSize(QSize(500, 0))
        self.verticalLayout_2 = QVBoxLayout(self.gb_right)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.tabw_right = QTabWidget(self.gb_right)
        self.tabw_right.setObjectName(u"tabw_right")
        self.tabw_right.setDocumentMode(False)
        self.tab_general = QWidget()
        self.tab_general.setObjectName(u"tab_general")
        self.verticalLayout_5 = QVBoxLayout(self.tab_general)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.sa_general = QScrollArea(self.tab_general)
        self.sa_general.setObjectName(u"sa_general")
        self.sa_general.setFrameShape(QFrame.NoFrame)
        self.sa_general.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sa_general.setWidgetResizable(True)
        self.sa_general_contents = QWidget()
        self.sa_general_contents.setObjectName(u"sa_general_contents")
        self.sa_general_contents.setGeometry(QRect(0, 0, 747, 519))
        self.verticalLayout_8 = QVBoxLayout(self.sa_general_contents)
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_type = QLabel(self.sa_general_contents)
        self.label_type.setObjectName(u"label_type")

        self.verticalLayout_8.addWidget(self.label_type)

        self.combox_type_diagram = QComboBox(self.sa_general_contents)
        self.combox_type_diagram.setObjectName(u"combox_type_diagram")

        self.verticalLayout_8.addWidget(self.combox_type_diagram)

        self.line_type_dia = QFrame(self.sa_general_contents)
        self.line_type_dia.setObjectName(u"line_type_dia")
        self.line_type_dia.setFrameShape(QFrame.HLine)
        self.line_type_dia.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_8.addWidget(self.line_type_dia)

        self.label_diagram_parameters = QLabel(self.sa_general_contents)
        self.label_diagram_parameters.setObjectName(u"label_diagram_parameters")

        self.verticalLayout_8.addWidget(self.label_diagram_parameters)

        self.fl_diagram_parameters = QFormLayout()
        self.fl_diagram_parameters.setObjectName(u"fl_diagram_parameters")
        self.fl_diagram_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)

        self.verticalLayout_8.addLayout(self.fl_diagram_parameters)

        self.line_p_dia = QFrame(self.sa_general_contents)
        self.line_p_dia.setObjectName(u"line_p_dia")
        self.line_p_dia.setFrameShape(QFrame.HLine)
        self.line_p_dia.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_8.addWidget(self.line_p_dia)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.sa_general.setWidget(self.sa_general_contents)

        self.verticalLayout_5.addWidget(self.sa_general)

        self.tabw_right.addTab(self.tab_general, "")
        self.tab_elements = QWidget()
        self.tab_elements.setObjectName(u"tab_elements")
        self.verticalLayout_3 = QVBoxLayout(self.tab_elements)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(self.tab_elements)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vl_nodes = QVBoxLayout(self.verticalLayoutWidget)
        self.vl_nodes.setSpacing(4)
        self.vl_nodes.setObjectName(u"vl_nodes")
        self.vl_nodes.setContentsMargins(0, 0, 0, 0)
        self.label_nodes = QLabel(self.verticalLayoutWidget)
        self.label_nodes.setObjectName(u"label_nodes")

        self.vl_nodes.addWidget(self.label_nodes)

        self.tablew_nodes = QTableWidget(self.verticalLayoutWidget)
        self.tablew_nodes.setObjectName(u"tablew_nodes")

        self.vl_nodes.addWidget(self.tablew_nodes)

        self.hl_btns = QHBoxLayout()
        self.hl_btns.setObjectName(u"hl_btns")
        self.btn_addnode = QPushButton(self.verticalLayoutWidget)
        self.btn_addnode.setObjectName(u"btn_addnode")

        self.hl_btns.addWidget(self.btn_addnode)

        self.btn_movenodes = QPushButton(self.verticalLayoutWidget)
        self.btn_movenodes.setObjectName(u"btn_movenodes")

        self.hl_btns.addWidget(self.btn_movenodes)


        self.vl_nodes.addLayout(self.hl_btns)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.vl_connections = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vl_connections.setSpacing(4)
        self.vl_connections.setObjectName(u"vl_connections")
        self.vl_connections.setContentsMargins(0, 0, 0, 0)
        self.line_3 = QFrame(self.verticalLayoutWidget_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.vl_connections.addWidget(self.line_3)

        self.label_connections = QLabel(self.verticalLayoutWidget_2)
        self.label_connections.setObjectName(u"label_connections")

        self.vl_connections.addWidget(self.label_connections)

        self.tablew_connections = QTableWidget(self.verticalLayoutWidget_2)
        self.tablew_connections.setObjectName(u"tablew_connections")

        self.vl_connections.addWidget(self.tablew_connections)

        self.btn_moveconnections = QPushButton(self.verticalLayoutWidget_2)
        self.btn_moveconnections.setObjectName(u"btn_moveconnections")

        self.vl_connections.addWidget(self.btn_moveconnections)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_3.addWidget(self.splitter)

        self.tabw_right.addTab(self.tab_elements, "")
        self.tab_editor = QWidget()
        self.tab_editor.setObjectName(u"tab_editor")
        self.verticalLayout_7 = QVBoxLayout(self.tab_editor)
        self.verticalLayout_7.setSpacing(9)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(9, 9, 9, 9)
        self.editor_scrollarea = QScrollArea(self.tab_editor)
        self.editor_scrollarea.setObjectName(u"editor_scrollarea")
        self.editor_scrollarea.setFrameShape(QFrame.NoFrame)
        self.editor_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor_scrollarea.setWidgetResizable(True)
        self.editor_scrollarea_contents = QWidget()
        self.editor_scrollarea_contents.setObjectName(u"editor_scrollarea_contents")
        self.editor_scrollarea_contents.setGeometry(QRect(0, 0, 274, 572))
        self.verticalLayout_4 = QVBoxLayout(self.editor_scrollarea_contents)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_edit_errors = QLabel(self.editor_scrollarea_contents)
        self.label_edit_errors.setObjectName(u"label_edit_errors")

        self.verticalLayout_4.addWidget(self.label_edit_errors)

        self.vl_edit_errors = QVBoxLayout()
        self.vl_edit_errors.setObjectName(u"vl_edit_errors")

        self.verticalLayout_4.addLayout(self.vl_edit_errors)

        self.line_errors = QFrame(self.editor_scrollarea_contents)
        self.line_errors.setObjectName(u"line_errors")
        self.line_errors.setFrameShape(QFrame.HLine)
        self.line_errors.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_errors)

        self.label_control_sectors = QLabel(self.editor_scrollarea_contents)
        self.label_control_sectors.setObjectName(u"label_control_sectors")

        self.verticalLayout_4.addWidget(self.label_control_sectors)

        self.vl_control_sectors = QVBoxLayout()
        self.vl_control_sectors.setSpacing(4)
        self.vl_control_sectors.setObjectName(u"vl_control_sectors")
        self.tw_control_sectors = QTableWidget(self.editor_scrollarea_contents)
        self.tw_control_sectors.setObjectName(u"tw_control_sectors")

        self.vl_control_sectors.addWidget(self.tw_control_sectors)

        self.hl_control_sectors_buttons = QHBoxLayout()
        self.hl_control_sectors_buttons.setObjectName(u"hl_control_sectors_buttons")
        self.btn_add_control_sector = QPushButton(self.editor_scrollarea_contents)
        self.btn_add_control_sector.setObjectName(u"btn_add_control_sector")

        self.hl_control_sectors_buttons.addWidget(self.btn_add_control_sector)

        self.btn_move_control_sectors = QPushButton(self.editor_scrollarea_contents)
        self.btn_move_control_sectors.setObjectName(u"btn_move_control_sectors")

        self.hl_control_sectors_buttons.addWidget(self.btn_move_control_sectors)


        self.vl_control_sectors.addLayout(self.hl_control_sectors_buttons)

        self.line_cont_sect = QFrame(self.editor_scrollarea_contents)
        self.line_cont_sect.setObjectName(u"line_cont_sect")
        self.line_cont_sect.setFrameShape(QFrame.HLine)
        self.line_cont_sect.setFrameShadow(QFrame.Sunken)

        self.vl_control_sectors.addWidget(self.line_cont_sect)


        self.verticalLayout_4.addLayout(self.vl_control_sectors)

        self.label_object_data = QLabel(self.editor_scrollarea_contents)
        self.label_object_data.setObjectName(u"label_object_data")

        self.verticalLayout_4.addWidget(self.label_object_data)

        self.fl_object_data = QFormLayout()
        self.fl_object_data.setObjectName(u"fl_object_data")
        self.fl_object_data.setRowWrapPolicy(QFormLayout.WrapLongRows)

        self.verticalLayout_4.addLayout(self.fl_object_data)

        self.line_data = QFrame(self.editor_scrollarea_contents)
        self.line_data.setObjectName(u"line_data")
        self.line_data.setFrameShape(QFrame.HLine)
        self.line_data.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_data)

        self.label_type_object_data = QLabel(self.editor_scrollarea_contents)
        self.label_type_object_data.setObjectName(u"label_type_object_data")

        self.verticalLayout_4.addWidget(self.label_type_object_data)

        self.fl_type_object_data = QFormLayout()
        self.fl_type_object_data.setObjectName(u"fl_type_object_data")
        self.fl_type_object_data.setRowWrapPolicy(QFormLayout.WrapLongRows)

        self.verticalLayout_4.addLayout(self.fl_type_object_data)

        self.line_type_data = QFrame(self.editor_scrollarea_contents)
        self.line_type_data.setObjectName(u"line_type_data")
        self.line_type_data.setFrameShape(QFrame.HLine)
        self.line_type_data.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_type_data)

        self.label_objects_data = QLabel(self.editor_scrollarea_contents)
        self.label_objects_data.setObjectName(u"label_objects_data")

        self.verticalLayout_4.addWidget(self.label_objects_data)

        self.fl_objects_data = QFormLayout()
        self.fl_objects_data.setObjectName(u"fl_objects_data")
        self.fl_objects_data.setRowWrapPolicy(QFormLayout.WrapLongRows)

        self.verticalLayout_4.addLayout(self.fl_objects_data)

        self.line_global_data = QFrame(self.editor_scrollarea_contents)
        self.line_global_data.setObjectName(u"line_global_data")
        self.line_global_data.setFrameShape(QFrame.HLine)
        self.line_global_data.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_global_data)

        self.label_object_parameters = QLabel(self.editor_scrollarea_contents)
        self.label_object_parameters.setObjectName(u"label_object_parameters")

        self.verticalLayout_4.addWidget(self.label_object_parameters)

        self.fl_object_parameters = QFormLayout()
        self.fl_object_parameters.setObjectName(u"fl_object_parameters")
        self.fl_object_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)

        self.verticalLayout_4.addLayout(self.fl_object_parameters)

        self.line_pars = QFrame(self.editor_scrollarea_contents)
        self.line_pars.setObjectName(u"line_pars")
        self.line_pars.setFrameShape(QFrame.HLine)
        self.line_pars.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_pars)

        self.label_type_object_parameters = QLabel(self.editor_scrollarea_contents)
        self.label_type_object_parameters.setObjectName(u"label_type_object_parameters")

        self.verticalLayout_4.addWidget(self.label_type_object_parameters)

        self.fl_type_object_parameters = QFormLayout()
        self.fl_type_object_parameters.setObjectName(u"fl_type_object_parameters")
        self.fl_type_object_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)

        self.verticalLayout_4.addLayout(self.fl_type_object_parameters)

        self.line_type_pars = QFrame(self.editor_scrollarea_contents)
        self.line_type_pars.setObjectName(u"line_type_pars")
        self.line_type_pars.setFrameShape(QFrame.HLine)
        self.line_type_pars.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_type_pars)

        self.label_objects_parameters = QLabel(self.editor_scrollarea_contents)
        self.label_objects_parameters.setObjectName(u"label_objects_parameters")

        self.verticalLayout_4.addWidget(self.label_objects_parameters)

        self.fl_objects_parameters = QFormLayout()
        self.fl_objects_parameters.setObjectName(u"fl_objects_parameters")
        self.fl_objects_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)

        self.verticalLayout_4.addLayout(self.fl_objects_parameters)

        self.line_global_pars = QFrame(self.editor_scrollarea_contents)
        self.line_global_pars.setObjectName(u"line_global_pars")
        self.line_global_pars.setFrameShape(QFrame.HLine)
        self.line_global_pars.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_global_pars)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.vertical_spacer)

        self.verticalLayout_4.setStretch(23, 1)
        self.editor_scrollarea.setWidget(self.editor_scrollarea_contents)

        self.verticalLayout_7.addWidget(self.editor_scrollarea)

        self.tabw_right.addTab(self.tab_editor, "")
        self.tab_control = QWidget()
        self.tab_control.setObjectName(u"tab_control")
        self.verticalLayout_6 = QVBoxLayout(self.tab_control)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.fl_control = QFormLayout()
        self.fl_control.setObjectName(u"fl_control")

        self.verticalLayout_6.addLayout(self.fl_control)

        self.tabw_right.addTab(self.tab_control, "")

        self.verticalLayout_2.addWidget(self.tabw_right)

        self.centralwidget_splitter.addWidget(self.gb_right)

        self.horizontalLayout.addWidget(self.centralwidget_splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1144, 22))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu = QMenu(self.menu_bar)
        self.menu.setObjectName(u"menu")
        self.menu_3 = QMenu(self.menu)
        self.menu_3.setObjectName(u"menu_3")
        MainWindow.setMenuBar(self.menu_bar)
        self.tb_main = QToolBar(MainWindow)
        self.tb_main.setObjectName(u"tb_main")
        self.tb_main.setEnabled(True)
        self.tb_main.setMovable(True)
        self.tb_main.setAllowedAreas(Qt.AllToolBarAreas)
        self.tb_main.setOrientation(Qt.Horizontal)
        self.tb_main.setIconSize(QSize(32, 24))
        self.tb_main.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_main.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.tb_main)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        self.status_bar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_export_to_image)
        self.menu.addAction(self.action_parameters)
        self.menu.addAction(self.menu_3.menuAction())
        self.menu_3.addAction(self.light_action)
        self.menu_3.addAction(self.dark_action)
        self.tb_main.addAction(self.action_new)
        self.tb_main.addAction(self.action_open)
        self.tb_main.addAction(self.action_save)
        self.tb_main.addAction(self.action_export_to_image)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_parameters)

        self.retranslateUi(MainWindow)

        self.tabw_right.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0437\u0430\u0446\u0438\u044f \u0418\u0414", None))
        self.action_new.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439", None))
#if QT_CONFIG(shortcut)
        self.action_new.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.action_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_saveas.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043a\u0430\u043a", None))
#if QT_CONFIG(shortcut)
        self.action_saveas.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.action_zoomin.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0432\u0435\u043b\u0438\u0447\u0438\u0442\u044c", None))
#if QT_CONFIG(shortcut)
        self.action_zoomin.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl++", None))
#endif // QT_CONFIG(shortcut)
        self.action_zoomout.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043c\u0435\u043d\u044c\u0448\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.action_zoomout.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u043c\u0435\u043d\u044c\u0448\u0438\u0442\u044c", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_zoomout.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+-", None))
#endif // QT_CONFIG(shortcut)
        self.action_edit_variables.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
        self.action_edit_variables.setIconText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
#if QT_CONFIG(tooltip)
        self.action_edit_variables.setToolTip(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445", None))
#endif // QT_CONFIG(tooltip)
        self.action_zoomfitpage.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e \u0448\u0438\u0440\u0438\u043d\u0435", None))
        self.action_export_to_image.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
        self.action_edit_templates.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u043e\u0432", None))
        self.action_edit_composition.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u0441\u043e\u0441\u0442\u0430\u0432\u0430 \u0418\u0414", None))
        self.action_clear_trash.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u043a\u0430 \u043e\u0442 \u043c\u0443\u0441\u043e\u0440\u0430", None))
        self.action_parameters.setText(QCoreApplication.translate("MainWindow", u"\u0411\u043b\u043e\u043a\u0438 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432", None))
        self.light_action.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0432\u0435\u0442\u043b\u0430\u044f", None))
        self.dark_action.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0451\u043c\u043d\u0430\u044f", None))
        self.label_type.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0438\u043f \u0441\u0445\u0435\u043c\u044b</span></p></body></html>", None))
        self.label_diagram_parameters.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0441\u0445\u0435\u043c\u044b</span></p></body></html>", None))
        self.tabw_right.setTabText(self.tabw_right.indexOf(self.tab_general), QCoreApplication.translate("MainWindow", u"\u041e\u0441\u043d\u043e\u0432\u043d\u044b\u0435 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.label_nodes.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u043e\u0447\u043a\u0438</span></p></body></html>", None))
        self.btn_addnode.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u043e\u0447\u043a\u0443", None))
        self.btn_movenodes.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u043e\u0440\u044f\u0434\u043e\u043a \u0442\u043e\u0447\u0435\u043a", None))
        self.label_connections.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0434\u043b\u0438\u043d\u044b</span></p></body></html>", None))
        self.btn_moveconnections.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0445 \u0434\u043b\u0438\u043d", None))
        self.tabw_right.setTabText(self.tabw_right.indexOf(self.tab_elements), QCoreApplication.translate("MainWindow", u"\u042d\u043b\u0435\u043c\u0435\u043d\u0442\u044b", None))
        self.label_edit_errors.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u041e\u0448\u0438\u0431\u043a\u0438</span></p></body></html>", None))
        self.label_control_sectors.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0421\u043f\u043e\u0441\u043e\u0431 \u043f\u0440\u043e\u043a\u043b\u0430\u0434\u043a\u0438 \u0412\u041e\u041a</span></p></body></html>", None))
        self.btn_add_control_sector.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0435\u043a\u0442\u043e\u0440", None))
        self.btn_move_control_sectors.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u0435\u043a\u0442\u043e\u0440\u043e\u0432", None))
        self.label_object_data.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0414\u0430\u043d\u043d\u044b\u0435</span></p></body></html>", None))
        self.label_type_object_data.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0438\u043f\u043e\u0432\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435</span></p></body></html>", None))
        self.label_objects_data.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0413\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435</span></p></body></html>", None))
        self.label_object_parameters.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b</span></p></body></html>", None))
        self.label_type_object_parameters.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0422\u0438\u043f\u043e\u0432\u044b\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b</span></p></body></html>", None))
        self.label_objects_parameters.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">\u0413\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b</span></p></body></html>", None))
        self.tabw_right.setTabText(self.tabw_right.indexOf(self.tab_editor), QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.tabw_right.setTabText(self.tabw_right.indexOf(self.tab_control), QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u044c\u043d\u043e\u0433\u043e \u0441\u0435\u043a\u0442\u043e\u0440\u0430", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0447\u0435\u0435", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043c\u0430", None))
        self.tb_main.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u0432", None))
    # retranslateUi


``
### D:\projects\net-constructor\package\ui\__init__.py
``python

``
