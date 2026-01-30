"""Инициализация приложения, менеджер объектов и запуск GUI."""

import sys

import resources_rc  # noqa: F401 — регистрация ресурсов Qt до использования иконки

from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtWidgets import QApplication

from package.components import mainwindow
from package.controllers import icons
from package.controllers import style
from package.modules import configs
from package.modules import dirpathmanager
from package.modules import project
from package.modules import settings
from package.modules import undojournal


class ObjectsManager:
    """Менеджер объектов приложения (окно, пути, конфиги, проект, настройки, стиль, иконки, undo)."""

    def __init__(self) -> None:
        self.obj_mw = None
        self.obj_dirpath = None
        self.obj_configs = None
        self.obj_project = None
        self.obj_settings = None
        self.obj_style = None
        self.obj_icons = None
        self.obj_undo_journal = None

    def initializing_objects(self) -> None:
        """Создаёт и инициализирует объекты: DirPathManager, Configs, Project, Settings, Style, Icons, UndoJournal."""
        self.obj_dirpath = dirpathmanager.DirPathManager()
        self.obj_configs = configs.Configs()
        self.obj_project = project.Project()
        self.obj_project.set_configs(self.obj_configs)
        self.obj_settings = settings.Settings()
        self.obj_settings.setting_osbm(self)
        self.obj_settings.initialize_default_settings()
        self.obj_style = style.Style()
        self.obj_style.setting_all_osbm(self)
        self.obj_icons = icons.Icons()
        self.obj_undo_journal = undojournal.UndoJournal(
            max_size=self.obj_settings.get_journal_limit()
        )

class App:
    """Главный класс приложения: инициализация, конфигурация, запуск GUI."""

    def __init__(self, current_directory: str) -> None:
        self.current_directory = current_directory
        #
        self.__obsm = ObjectsManager()
        self.__obsm.initializing_objects()
        #
        self.config_objects()
        self.start_app()

    def config_objects(self) -> None:
        """Устанавливает директорию приложения и загружает конфиги."""
        self.__obsm.obj_dirpath.set_dir_app(self.current_directory)
        self.__obsm.obj_configs.load_configs(self.current_directory)

    def start_app(self) -> None:
        """Запуск GUI: QApplication, шрифты, иконка, главное окно, стиль, exec."""
        try:
            self.app = QApplication(sys.argv)
            self.__font_main = QFontDatabase.addApplicationFont(
                ":/fonts/resources/fonts/OpenSans-VariableFont_wdth,wght.ttf"
            )
            QFontDatabase.addApplicationFont(
                ":/fonts/resources/fonts/OpenSans-Italic-VariableFont_wdth,wght.ttf"
            )
            try:
                font_families = QFontDatabase.applicationFontFamilies(self.__font_main)
                if font_families:
                    self.__size_font = 10
                    self.__custom_font = QFont(font_families[0], self.__size_font)
                    self.app.setFont(self.__custom_font)
            except (OSError, RuntimeError) as e:
                print(f"Error loading font: {e}")
            self.app.setWindowIcon(QIcon(":/app/resources/app-icon.svg"))
            self.window = mainwindow.MainWindow(self.__obsm)
            self.__obsm.obj_mw = self.window
            # Применяем стиль к главному окну
            saved_theme = self.__obsm.obj_settings.get_theme()
            self.__obsm.obj_style.set_style_for_mw_by_name(self.window, saved_theme)
            self.window.show()
            # Без sys.exit для корректного выхода из QApplication
            self.app.exec_()
        except (OSError, RuntimeError) as e:
            print(f"Error starting app: {e}")
