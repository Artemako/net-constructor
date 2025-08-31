import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

import package.components.mainwindow as mainwindow

import package.modules.dirpathmanager as dirpathmanager
import package.modules.configs as configs
import package.modules.project as project
import package.controllers.style as style

class ObjectsManager:
    """
    Мененджер объектов.
    """
    def __init__(self):
        self.obj_mw = None
        self.obj_dirpath = None
        self.obj_configs = None
        self.obj_project = None
        self.obj_style = None

    def initializing_objects(self):
        self.obj_dirpath = dirpathmanager.DirPathManager()
        self.obj_configs = configs.Configs()
        self.obj_project = project.Project()
        self.obj_style = style.Style()
        self.obj_style.setting_all_osbm(self)
   
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
            # Применяем стиль к главному окну
            self.__obsm.obj_style.set_style_for_mw_by_name(self.window, "dark")
            self.window.show()
            # sys.exit(self.app.exec())
            self.app.exec_()
        except Exception as e:
            print(f"Error: {e}")
