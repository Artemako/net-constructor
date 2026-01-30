"""Главное окно приложения: диаграммы, параметры, вкладки, меню, undo/redo."""

import copy
import json
import os
from functools import partial

from PySide6.QtCore import QLocale, QModelIndex, QRegularExpression, QSettings, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QIcon,
    QIntValidator,
    QKeySequence,
    QRegularExpressionValidator,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QFontComboBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStyledItemDelegate,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from package.components import cablelistsdialog
from package.components import changeorderdialog
from package.components import controlsectordeletedialog
from package.components import diagramtypeselectdialog
from package.components import nodeconnectiondeletedialog
from package.components import nodeconnectionselectdialog
from package.components import sectornamesdialog
from package.components import settingsdialog
import package.constants as constants
from package.controllers import imagewidget
from package.ui import mainwindow_ui


class CustomTableComboBox(QComboBox):
    """Кастомный QComboBox для использования в таблице, аналогичный list_with_custom"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Всегда редактируемый, как в list_with_custom
        self.setEditable(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def setCustomText(self, text):
        """Устанавливает текст в виджет без изменения списка элементов"""
        # Найдем индекс существующего элемента
        index = self.findText(str(text))
        if index >= 0:
            # Если элемент есть в списке - выбираем его
            self.setCurrentIndex(index)
        else:
            # Если элемента нет в списке - показываем кастомный текст
            self.setCurrentText(str(text))


class MainWindow(QMainWindow):
    """Главное окно: диаграммы, вкладки настроек/элементов/редактирования, меню, undo/redo."""

    def __init__(self, obsm) -> None:
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
        # Флаг для отслеживания несохранённых изменений
        self.__document_modified = False
        self.__current_file_path = None
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
        # тема - используем настройки из OSBM
        self.__theme_name = self.__obsm.obj_settings.get_theme()
        # СТИЛЬ - используем контроллер стилей из OSBM
        self.__obj_style = self.__obsm.obj_style
        self.__obj_style.set_style_for_mw_by_name(self, self.__theme_name)
        # + иконки - используем контроллер иконок из OSBM
        self.__obj_icons = self.__obsm.obj_icons
        self.__obj_icons.set_icons_for_mw_by_name(self, self.__theme_name)
        # иконка окна (фавикон)
        self.setWindowIcon(QIcon(":/app/resources/app-icon.svg"))
        #
        self.resize(1366, 768)
        self.ui.centralwidget_splitter.setSizes([806, 560])
        # QAction Ctrl S или Enter (с фильтром для текстовых полей)
        self.ui.action_save.setShortcuts(
            [
                QKeySequence("Ctrl+S"),  # Ctrl + S
            ]
        )
        
        # Устанавливаем фильтр событий для обработки Enter
        self.installEventFilter(self)

        #
        # Скрываем правый блок с вкладками при запуске
        self.ui.gb_right.setVisible(False)
        self.ui.tabw_right.tabBar().setTabVisible(2, False)
        self.ui.tabw_right.tabBar().setTabVisible(3, False)
        self.ui.tabw_right.currentChanged.connect(self._tab_right_changed)

        # self.update_menu_recent_projects()
        #
        # self.ui.btn_deletenode.clicked.connect(self._delete_node)
        #
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
        # Инициализируем состояние действия из настроек
        show_parameters = self.__obsm.obj_settings.get_show_parameters()
        self.ui.action_parameters.setChecked(show_parameters)
        # смены темы (убрано из меню, теперь в диалоге настроек)
        # self.ui.dark_action.triggered.connect(lambda: self._change_theme("dark"))
        # self.ui.light_action.triggered.connect(lambda: self._change_theme("light"))
        # управление списками кабелей
        self.ui.action_edit_cable_lists.triggered.connect(self._edit_cable_lists)
        self.ui.action_edit_sector_names.triggered.connect(self._edit_sector_names)
        # открытие диалога настроек
        self.ui.action_settings.triggered.connect(self._open_settings)
        #
        # Журнал отмены/повтора (Undo/Redo)
        self.__last_widget_values = {}
        self.__last_diagram_type_value = None
        self.__applying_undo_redo = False
        # Действия "Отмена" и "Повтор/Возврат" в меню "Правка" и на панели инструментов (из UI)
        self.ui.action_undo.setShortcutContext(Qt.ApplicationShortcut)
        self.ui.action_undo.triggered.connect(self._undo)
        self.ui.action_redo.setShortcutContext(Qt.ApplicationShortcut)
        self.ui.action_redo.triggered.connect(self._redo)
        self.addAction(self.ui.action_undo)
        self.addAction(self.ui.action_redo)
        edit_menu = QMenu("Правка", self)
        self.ui.menu_bar.insertMenu(self.ui.menu_other.menuAction(), edit_menu)
        edit_menu.addAction(self.ui.action_undo)
        edit_menu.addAction(self.ui.action_redo)
        self._update_undo_redo_actions()
        #
        # Генерируем виджеты для вкладок
        self._setup_general_tab_widgets()
        self._setup_elements_tab_widgets()
        self._setup_editor_tab_widgets()
        self._setup_control_tab_widgets()
        #
        # Устанавливаем заголовок окна при запуске
        self._update_window_title()

    def _setup_general_tab_widgets(self):
        """Генерирует виджеты для вкладки 'Основные настройки'"""
        # Очищаем содержимое вкладки
        self._clear_general_tab()
        
        # Создаем виджеты
        self._create_general_tab_widgets()
        
    def _clear_general_tab(self):
        """Очищает содержимое вкладки 'Основные настройки'"""
        # Очищаем все виджеты из layout
        while self.ui.sa_general_contents.layout().count():
            child = self.ui.sa_general_contents.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def _create_general_tab_widgets(self):
        """Создает виджеты для вкладки 'Основные настройки'"""
        layout = self.ui.sa_general_contents.layout()
        
        # Создаем группу "Тип схемы"
        self.type_group = QGroupBox("Тип схемы")
        type_layout = QVBoxLayout()
        type_layout.setContentsMargins(10, 10, 10, 10)
        type_layout.setSpacing(6)
        
        self.combox_type_diagram = QComboBox()
        type_layout.addWidget(self.combox_type_diagram)
        
        self.type_group.setLayout(type_layout)
        
        # Создаем группу "Параметры схемы"
        self.parameters_group = QGroupBox("Параметры схемы")
        parameters_layout = QVBoxLayout()
        parameters_layout.setContentsMargins(10, 10, 10, 10)
        parameters_layout.setSpacing(6)
        
        self.fl_diagram_parameters = QFormLayout()
        self.fl_diagram_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)
        parameters_layout.addLayout(self.fl_diagram_parameters)
        
        self.parameters_group.setLayout(parameters_layout)
        
        # Создаем вертикальный спейсер
        self.verticalSpacer = QWidget()
        self.verticalSpacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Добавляем виджеты в layout
        layout.addWidget(self.type_group)
        layout.addWidget(self.parameters_group)
        layout.addWidget(self.verticalSpacer)
        
        # Подключаем сигналы (журнал отмены + смена типа)
        self.combox_type_diagram.currentIndexChanged.connect(self._on_diagram_type_changed)
        
    def _setup_elements_tab_widgets(self):
        """Генерирует виджеты для вкладки 'Элементы'"""
        # Очищаем содержимое вкладки
        self._clear_elements_tab()
        
        # Создаем виджеты
        self._create_elements_tab_widgets()
        
    def _clear_elements_tab(self):
        """Очищает содержимое вкладки 'Элементы'"""
        # Очищаем все виджеты из главного layout вкладки элементов
        while self.ui.verticalLayout_3.count():
            child = self.ui.verticalLayout_3.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def _create_elements_tab_widgets(self):
        """Создает виджеты для вкладки 'Элементы'"""
        # Создаем группу "Точки"
        self.nodes_group = QGroupBox("Точки")
        self.nodes_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        nodes_layout = QVBoxLayout()
        nodes_layout.setContentsMargins(10, 10, 10, 10)
        nodes_layout.setSpacing(6)
        
        self.tablew_nodes = QTableWidget()
        nodes_layout.addWidget(self.tablew_nodes, 1)  # Растягивающий фактор 1
        
        self.hl_btns = QHBoxLayout()
        self.btn_addnode = QPushButton("Добавить точку")
        self.btn_movenodes = QPushButton("Изменить порядок точек")
        
        self.hl_btns.addWidget(self.btn_addnode)
        self.hl_btns.addWidget(self.btn_movenodes)
        nodes_layout.addLayout(self.hl_btns)
        
        self.nodes_group.setLayout(nodes_layout)
        
        # Создаем группу "Строительные длины"
        self.connections_group = QGroupBox("Строительные длины")
        self.connections_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        connections_layout = QVBoxLayout()
        connections_layout.setContentsMargins(10, 10, 10, 10)
        connections_layout.setSpacing(6)
        
        self.tablew_connections = QTableWidget()
        connections_layout.addWidget(self.tablew_connections, 1)  # Растягивающий фактор 1
        
        self.btn_moveconnections = QPushButton("Изменить порядок строительных длин")
        connections_layout.addWidget(self.btn_moveconnections)
        
        self.connections_group.setLayout(connections_layout)
        
        # Добавляем группы в основной layout с равными растягивающими факторами
        self.ui.verticalLayout_3.addWidget(self.nodes_group, 1)  # Равные пропорции 1:1
        self.ui.verticalLayout_3.addWidget(self.connections_group, 1)  # Равные пропорции 1:1
        
        # Подключаем сигналы
        self.btn_addnode.clicked.connect(self._add_node)
        self.btn_movenodes.clicked.connect(self._move_nodes)
        self.btn_moveconnections.clicked.connect(self._move_connections)
        
    def _setup_editor_tab_widgets(self):
        """Генерирует виджеты для вкладки 'Редактирование'"""
        # Очищаем содержимое вкладки
        self._clear_editor_tab()
        
        # Создаем виджеты
        self._create_editor_tab_widgets()
        
    def _clear_editor_tab(self):
        """Очищает содержимое вкладки 'Редактирование'"""
        # Очищаем все виджеты из layout
        while self.ui.editor_scrollarea_contents.layout().count():
            child = self.ui.editor_scrollarea_contents.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                # Если это layout, очищаем его содержимое
                while child.layout().count():
                    sub_child = child.layout().takeAt(0)
                    if sub_child.widget():
                        sub_child.widget().deleteLater()
                        
    def _create_editor_tab_widgets(self):
        """Создает виджеты для вкладки 'Редактирование'"""
        layout = self.ui.editor_scrollarea_contents.layout()
        
        # Создаем группу "Ошибки"
        self.errors_group = QGroupBox("Ошибки")
        errors_layout = QVBoxLayout()
        errors_layout.setContentsMargins(10, 10, 10, 10)
        errors_layout.setSpacing(6)
        
        self.vl_edit_errors = QVBoxLayout()
        errors_layout.addLayout(self.vl_edit_errors)
        
        self.errors_group.setLayout(errors_layout)
        
        # Создаем группу "Способ прокладки ВОК"
        self.control_sectors_group = QGroupBox("Способ прокладки ВОК")
        self.control_sectors_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        control_sectors_layout = QVBoxLayout()
        control_sectors_layout.setContentsMargins(10, 10, 10, 10)
        control_sectors_layout.setSpacing(6)
        
        self.tw_control_sectors = QTableWidget()
        control_sectors_layout.addWidget(self.tw_control_sectors)
        
        self.hl_control_sectors_buttons = QHBoxLayout()
        self.btn_add_control_sector = QPushButton("Добавить сектор")
        self.btn_move_control_sectors = QPushButton("Изменить порядок секторов")
        
        self.hl_control_sectors_buttons.addWidget(self.btn_add_control_sector)
        self.hl_control_sectors_buttons.addWidget(self.btn_move_control_sectors)
        control_sectors_layout.addLayout(self.hl_control_sectors_buttons)
        
        self.control_sectors_group.setLayout(control_sectors_layout)
        
        # Создаем группу "Данные"
        self.object_data_group = QGroupBox("Данные")
        self.object_data_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        object_data_layout = QVBoxLayout()
        object_data_layout.setContentsMargins(10, 10, 10, 10)
        object_data_layout.setSpacing(6)
        
        self.fl_object_data = QFormLayout()
        self.fl_object_data.setRowWrapPolicy(QFormLayout.WrapLongRows)
        object_data_layout.addLayout(self.fl_object_data)
        
        self.object_data_group.setLayout(object_data_layout)
        
        # Создаем группу "Типовые данные"
        self.type_object_data_group = QGroupBox("Типовые данные")
        self.type_object_data_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        type_object_data_layout = QVBoxLayout()
        type_object_data_layout.setContentsMargins(10, 10, 10, 10)
        type_object_data_layout.setSpacing(6)
        
        self.fl_type_object_data = QFormLayout()
        self.fl_type_object_data.setRowWrapPolicy(QFormLayout.WrapLongRows)
        type_object_data_layout.addLayout(self.fl_type_object_data)
        
        self.type_object_data_group.setLayout(type_object_data_layout)
        
        # Создаем группу "Глобальные данные"
        self.objects_data_group = QGroupBox("Глобальные данные")
        self.objects_data_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        objects_data_layout = QVBoxLayout()
        objects_data_layout.setContentsMargins(10, 10, 10, 10)
        objects_data_layout.setSpacing(6)
        
        self.fl_objects_data = QFormLayout()
        self.fl_objects_data.setRowWrapPolicy(QFormLayout.WrapLongRows)
        objects_data_layout.addLayout(self.fl_objects_data)
        
        self.objects_data_group.setLayout(objects_data_layout)
        
        # Создаем группу "Параметры"
        self.object_parameters_group = QGroupBox("Параметры")
        self.object_parameters_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        object_parameters_layout = QVBoxLayout()
        object_parameters_layout.setContentsMargins(10, 10, 10, 10)
        object_parameters_layout.setSpacing(6)
        
        self.fl_object_parameters = QFormLayout()
        self.fl_object_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)
        object_parameters_layout.addLayout(self.fl_object_parameters)
        
        self.object_parameters_group.setLayout(object_parameters_layout)
        
        # Создаем группу "Типовые параметры"
        self.type_object_parameters_group = QGroupBox("Типовые параметры")
        self.type_object_parameters_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        type_object_parameters_layout = QVBoxLayout()
        type_object_parameters_layout.setContentsMargins(10, 10, 10, 10)
        type_object_parameters_layout.setSpacing(6)
        
        self.fl_type_object_parameters = QFormLayout()
        self.fl_type_object_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)
        type_object_parameters_layout.addLayout(self.fl_type_object_parameters)
        
        self.type_object_parameters_group.setLayout(type_object_parameters_layout)
        
        # Создаем группу "Глобальные параметры"
        self.objects_parameters_group = QGroupBox("Глобальные параметры")
        self.objects_parameters_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        objects_parameters_layout = QVBoxLayout()
        objects_parameters_layout.setContentsMargins(10, 10, 10, 10)
        objects_parameters_layout.setSpacing(6)
        
        self.fl_objects_parameters = QFormLayout()
        self.fl_objects_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)
        objects_parameters_layout.addLayout(self.fl_objects_parameters)
        
        self.objects_parameters_group.setLayout(objects_parameters_layout)
        
        # Создаем вертикальный спейсер
        self.vertical_spacer = QWidget()
        self.vertical_spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Добавляем все группы в layout
        layout.addWidget(self.errors_group)
        layout.addWidget(self.control_sectors_group)
        layout.addWidget(self.object_data_group)
        layout.addWidget(self.type_object_data_group)
        layout.addWidget(self.objects_data_group)
        layout.addWidget(self.object_parameters_group)
        layout.addWidget(self.type_object_parameters_group)
        layout.addWidget(self.objects_parameters_group)
        layout.addWidget(self.vertical_spacer)
         
    def _setup_control_tab_widgets(self):
        """Генерирует виджеты для вкладки 'Редактирование контрольного сектора'"""
        # Очищаем содержимое вкладки
        self._clear_control_tab()
        
        # Создаем виджеты
        self._create_control_tab_widgets()
        
    def _clear_control_tab(self):
        """Очищает содержимое вкладки 'Редактирование контрольного сектора'"""
        # Очищаем данные контрольного сектора
        if hasattr(self, 'fl_control_data'):
            while self.fl_control_data.count():
                child = self.fl_control_data.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        
        # Очищаем параметры контрольного сектора
        if hasattr(self, 'fl_control_parameters'):
            while self.fl_control_parameters.count():
                child = self.fl_control_parameters.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                
    def _create_control_tab_widgets(self):
        """Создает виджеты для вкладки 'Редактирование контрольного сектора'"""
        # Создаем виджеты только один раз
        if not hasattr(self, 'control_data_group'):
            # Создаем группу "Данные контрольного сектора"
            self.control_data_group = QGroupBox("Данные")
            control_data_layout = QVBoxLayout()
            control_data_layout.setContentsMargins(10, 10, 10, 10)
            control_data_layout.setSpacing(6)
            
            self.fl_control_data = QFormLayout()
            self.fl_control_data.setRowWrapPolicy(QFormLayout.WrapLongRows)
            control_data_layout.addLayout(self.fl_control_data)
            
            self.control_data_group.setLayout(control_data_layout)
            
            # Создаем группу "Параметры контрольного сектора"
            self.control_parameters_group = QGroupBox("Параметры")
            control_parameters_layout = QVBoxLayout()
            control_parameters_layout.setContentsMargins(10, 10, 10, 10)
            control_parameters_layout.setSpacing(6)
            
            self.fl_control_parameters = QFormLayout()
            self.fl_control_parameters.setRowWrapPolicy(QFormLayout.WrapLongRows)
            control_parameters_layout.addLayout(self.fl_control_parameters)
            
            self.control_parameters_group.setLayout(control_parameters_layout)
            
            # Создаем вертикальный спейсер для прижатия к верху
            self.control_spacer = QWidget()
            self.control_spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            
            # Добавляем группы и спейсер в контейнер вкладки
            self.ui.verticalLayout_6.addWidget(self.control_data_group)
            self.ui.verticalLayout_6.addWidget(self.control_parameters_group)
            self.ui.verticalLayout_6.addWidget(self.control_spacer)

    def _change_theme(self, theme_name):
        self.__obsm.obj_settings.set_theme(theme_name)
        self.__theme_name = theme_name
        # Применяем тему ко всем окнам приложения
        self.__obj_style.apply_theme_to_all_windows(theme_name)
        # Обновляем иконки для главного окна
        self.__obsm.obj_icons.set_icons_for_mw_by_name(self, theme_name)

    def _start_qt_actions(self):
        self.ui.action_new.setEnabled(True)
        self.ui.action_open.setEnabled(True)
        self.ui.action_save.setEnabled(True)
        self.ui.action_saveas.setEnabled(True)
        self.ui.action_export_to_image.setEnabled(True)

    def _update_status_bar_with_project_name(self, file_name):
        self.__current_file_path = file_name
        self._update_window_title()
        self._update_status_bar()
    
    def _update_window_title(self):
        """Обновляет заголовок окна с учётом имени файла и статуса изменённости"""
        base_title = "Автоматизация ИД"
        
        if self.__current_file_path:
            # Получаем только имя файла без пути
            file_name = os.path.basename(self.__current_file_path)
            modified_marker = " *" if self.__document_modified else ""
            self.setWindowTitle(f"{base_title} — {file_name}{modified_marker}")
        else:
            self.setWindowTitle(base_title)
    
    def _update_status_bar(self):
        """Обновляет статус-бар с информацией о файле и изменённости"""
        if self.__current_file_path:
            modified_text = " • Не сохранён" if self.__document_modified else ""
            self.statusBar().showMessage(f"Текущий проект: {self.__current_file_path}{modified_text}")
        else:
            self.statusBar().showMessage("Проект не открыт")
    
    def _set_document_modified(self, modified=True):
        """Устанавливает флаг изменённости документа и обновляет UI"""
        if self.__document_modified != modified:
            self.__document_modified = modified
            self._update_window_title()
            self._update_status_bar()
    
    def _check_unsaved_changes(self):
        """Проверяет наличие несохранённых изменений и предлагает сохранить.
        
        Возвращает:
            True - если можно продолжить (сохранено, отклонено или нет изменений)
            False - если пользователь отменил действие
        """
        if not self.__document_modified or not self.__obsm.obj_project.is_active():
            return True
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Несохранённые изменения")
        msg_box.setText("В проекте есть несохранённые изменения.")
        msg_box.setInformativeText("Сохранить изменения перед продолжением?")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        msg_box.setDefaultButton(QMessageBox.Save)
        
        # Локализация кнопок
        msg_box.button(QMessageBox.Save).setText("Сохранить")
        msg_box.button(QMessageBox.Discard).setText("Не сохранять")
        msg_box.button(QMessageBox.Cancel).setText("Отмена")
        
        result = msg_box.exec()
        
        if result == QMessageBox.Save:
            # Сохраняем изменения
            self._save_changes_to_file_nce()
            return True
        elif result == QMessageBox.Discard:
            # Не сохраняем, продолжаем
            return True
        else:  # QMessageBox.Cancel
            # Отменяем действие
            return False

    def _toggle_parameters_visibility(self):
        # Проверяем, активен ли проект
        if not self.__obsm.obj_project.is_active():
            return

        # Синхронизируем состояние действия с настройкой
        is_checked = self.ui.action_parameters.isChecked()
        self.__obsm.obj_settings.set_show_parameters(is_checked)
        self.__obsm.obj_settings.sync()
            
        # Обновляем все вкладки при изменении видимости параметров
        project_data = self.__obsm.obj_project.get_data()
        if project_data is None:
            return

        # Обновляем главную вкладку (Основные настройки)
        self._reset_widgets_by_data(project_data)
        
        # Если находимся на вкладке редактирования объекта, обновляем её тоже
        if self.ui.tabw_right.currentIndex() == 2:
            obj = self.__current_object
            is_node = self.__current_is_node
            # Обновляем виджеты параметров
            self._create_editor_parameters_widgets_by_object(obj, is_node)
        elif self.ui.tabw_right.currentIndex() == 3:
            self._create_control_sector_widgets(self.__current_control_sector)

    def create_file_nce(self):
        # Проверяем несохранённые изменения перед созданием нового файла
        if not self._check_unsaved_changes():
            return  # Пользователь отменил действие
        
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
                # Показываем правый блок с вкладками
                self.ui.gb_right.setVisible(True)
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
                self._refresh_diagram(is_new=True)
                self._start_qt_actions()
                self._update_undo_redo_actions()
                #
                self._update_status_bar_with_project_name(file_name)
                # Новый файл считается сохранённым
                self._set_document_modified(False)

    def open_file_nce(self):
        # Проверяем несохранённые изменения перед открытием другого файла
        if not self._check_unsaved_changes():
            return  # Пользователь отменил действие
        
        file_name, _ = QFileDialog.getOpenFileName(self, " ", "", self.__text_format)
        if file_name:
            #
            # Показываем правый блок с вкладками
            self.ui.gb_right.setVisible(True)
            self.ui.tabw_right.setCurrentIndex(0)
            #
            self.__obsm.obj_project.open_project(file_name)
            #
            self._refresh_diagram(is_new=True)
            self._start_qt_actions()
            self._update_undo_redo_actions()
            #
            self._update_status_bar_with_project_name(file_name)
            # Открытый файл считается сохранённым
            self._set_document_modified(False)

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
                # После сохранения как - файл сохранён
                self._set_document_modified(False)

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
                diagram_type_id = self.combox_type_diagram.currentData().get(
                    "type_id", ""
                )
                diagram_name = self.combox_type_diagram.currentData().get("name", "")
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

                # Если соединение - то нужно получить значения Название и Физ. длина из таблицы
                if not self.__current_is_node and self.__current_object is not None:
                    control_sectors = self.__current_object.get("control_sectors", [])
                    for row, cs in enumerate(control_sectors):
                        # Получаем виджеты из таблицы
                        # Для названия сектора используем кастомный виджет
                        name_widget = self.tw_control_sectors.cellWidget(row, 1)
                        item_cs_physical_length = self.tw_control_sectors.item(
                            row, 2
                        )
                        if name_widget:
                            cs["data_pars"]["cs_name"]["value"] = (
                                name_widget.currentText().strip()
                            )
                        if item_cs_physical_length:
                            try:
                                length_val = float(
                                    item_cs_physical_length.text().replace(",", ".")
                                )
                                cs["data_pars"]["cs_physical_length"]["value"] = (
                                    length_val
                                )
                            except (ValueError, TypeError):
                                pass  # Оставить старое значение, если не число

            elif self.ui.tabw_right.currentIndex() == 3:
                is_control_sector_tab = True
                # Получаем новые значения из виджетов (данные + параметры)
                new_control_data = self._get_new_data_or_parameters(
                    self.__control_sector_data_widgets, is_parameters=False
                )
                new_control_parameters = self._get_new_data_or_parameters(
                    self.__control_sector_parameters_widgets, is_parameters=True
                )
                new_control_sector_parameters = {
                    **new_control_data,
                    **new_control_parameters,
                }
                # Обновляем данные контрольного сектора
                if self.__current_control_sector is not None:
                    for key, value in new_control_sector_parameters.items():
                        if key in self.__current_control_sector.get("data_pars", {}):
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

            self._refresh_diagram()

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
            
            # Сбрасываем журналы отмены/возврата после сохранения проекта
            self.__obsm.obj_undo_journal.clear()
            self._update_undo_redo_actions()
            
            # Сбрасываем флаг изменённости после сохранения
            self._set_document_modified(False)

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
            elif widget_type == "physical_length_calculator":
                try:
                    coeff = float(widget.coefficient_input.text().replace(",", "."))
                except (ValueError, TypeError):
                    coeff = 1.0  # Значение по умолчанию при ошибке
                    
                new_data_or_parameters[key] = {
                    "value": {
                        "од": widget.optical_length_input.value(),
                        "к": coeff,
                        "фд": widget.physical_length_input.value(),
                    }
                }
            elif widget_type == "list_with_custom":
                current_text = widget.currentText()
                new_data_or_parameters[key] = {"value": current_text}
            else:
                if is_parameters:
                    new_data_or_parameters[key] = {"value": widget.value()}
                else:
                    new_data_or_parameters[key] = {"value": widget.toPlainText()}

        return new_data_or_parameters

    def _get_value_from_widget(self, widget_type, widget):
        """Возвращает текущее значение одного виджета по типу (для журнала отмены)."""
        if widget_type == "title":
            return "заголовок"
        if widget_type == "font_name":
            return widget.currentFont().toString()
        if widget_type == "color":
            return widget.text()
        if widget_type == "string_line":
            return widget.text()
        if widget_type in ("fill_style", "text_align", "line_style"):
            return widget.currentText()
        if widget_type == "bool":
            return widget.isChecked()
        if widget_type in ("number_int_signed", "number_int", "number_float"):
            return widget.value()
        if widget_type == "physical_length_calculator":
            try:
                coeff = float(widget.coefficient_input.text().replace(",", "."))
            except (ValueError, TypeError):
                coeff = 1.0
            return {
                "од": widget.optical_length_input.value(),
                "к": coeff,
                "фд": widget.physical_length_input.value(),
            }
        if widget_type == "list_with_custom":
            return widget.currentText()
        if hasattr(widget, "value"):
            return widget.value()
        if hasattr(widget, "toPlainText"):
            return widget.toPlainText()
        return None

    def _set_value_to_widget(self, widget_type, widget, value):
        """Устанавливает значение в виджет по типу (для отмены/повтора)."""
        if widget_type == "title":
            return
        if widget_type == "font_name":
            font = QFont()
            if value and font.fromString(value):
                widget.setCurrentFont(font)
            return
        if widget_type == "color":
            if value is not None:
                widget.setStyleSheet(f"background-color: {value};")
                widget.setText(value)
            return
        if widget_type == "string_line":
            widget.setText(value if value is not None else "")
            return
        if widget_type in ("fill_style", "text_align", "line_style"):
            idx = widget.findText(value) if value else -1
            if idx >= 0:
                widget.setCurrentIndex(idx)
            else:
                widget.setCurrentText(value or "")
            return
        if widget_type == "bool":
            widget.setChecked(bool(value))
            return
        if widget_type in ("number_int_signed", "number_int", "number_float"):
            widget.setValue(value if value is not None else 0)
            return
        if widget_type == "physical_length_calculator":
            if isinstance(value, dict):
                widget.optical_length_input.setValue(value.get("од", 0))
                widget.coefficient_input.setText(str(value.get("к", 0.97)))
                widget.physical_length_input.setValue(value.get("фд", 0))
            return
        if widget_type == "list_with_custom":
            if hasattr(widget, "setCustomText"):
                widget.setCustomText(str(value) if value is not None else "")
            else:
                idx = widget.findText(str(value)) if value is not None else -1
                if idx >= 0:
                    widget.setCurrentIndex(idx)
                else:
                    widget.setCurrentText(str(value) if value is not None else "")
            return
        if hasattr(widget, "setValue"):
            widget.setValue(value if value is not None else 0)
            return
        if hasattr(widget, "setText"):
            widget.setText(str(value) if value is not None else "")
            return
        if hasattr(widget, "setPlainText"):
            widget.setPlainText(str(value) if value is not None else "")

    def _journal_context(self):
        """Текущий контекст для журнала: None (вкладка 0), (object_id, is_node) (вкладка 2), (object_id, is_node, cs_id) (вкладка 3)."""
        if self.ui.tabw_right.currentIndex() == 0:
            return None
        if self.ui.tabw_right.currentIndex() == 2:
            if self.__current_object:
                return (self.__current_object.get("id"), self.__current_is_node)
            return None
        if self.ui.tabw_right.currentIndex() == 3:
            if self.__current_object and self.__current_control_sector:
                return (
                    self.__current_object.get("id"),
                    self.__current_is_node,
                    self.__current_control_sector.get("id"),
                )
            return None
        return None

    def _apply_widget_change_to_project(self, tab_index, dict_name, key, value):
        """Применяет изменение виджета к данным проекта без сохранения в файл."""
        if not self.__obsm.obj_project.is_active():
            return
        
        data = self.__obsm.obj_project.get_data()
        
        # Для вкладки "Основные настройки" (tab 0)
        if tab_index == 0 and dict_name == '__general_diagram_parameters_widgets':
            if "diagram_parameters" not in data:
                data["diagram_parameters"] = {}
            data["diagram_parameters"][key] = {"value": value}
        
        # Для вкладки "Редактирование объекта" (tab 2)
        elif tab_index == 2 and self.__current_object:
            object_id = self.__current_object.get("id")
            is_node = self.__current_is_node
            
            # Найти объект в данных проекта
            target_obj = None
            if is_node:
                nodes = data.get("nodes", [])
                for node in nodes:
                    if node.get("id") == object_id:
                        target_obj = node
                        break
            else:
                connections = data.get("connections", [])
                for conn in connections:
                    if conn.get("id") == object_id:
                        target_obj = conn
                        break
            
            if target_obj:
                if dict_name in ('__editor_object_data_widgets', '__editor_type_object_data_widgets', '__editor_objects_data_widgets'):
                    if "data" not in target_obj:
                        target_obj["data"] = {}
                    target_obj["data"][key] = {"value": value}
                elif dict_name in ('__editor_object_parameters_widgets', '__editor_type_object_parameters_widgets', '__editor_objects_parameters_widgets'):
                    if "parameters" not in target_obj:
                        target_obj["parameters"] = {}
                    target_obj["parameters"][key] = {"value": value}
                # Также обновляем локальный объект
                self.__current_object = target_obj
        
        # Для вкладки "Контрольный сектор" (tab 3)
        elif tab_index == 3 and self.__current_control_sector:
            object_id = self.__current_object.get("id")
            cs_id = self.__current_control_sector.get("id")
            
            # Найти соединение в данных проекта
            connections = data.get("connections", [])
            for conn in connections:
                if conn.get("id") == object_id:
                    # Найти контрольный сектор
                    for cs in conn.get("control_sectors", []):
                        if cs.get("id") == cs_id:
                            if "data_pars" not in cs:
                                cs["data_pars"] = {}
                            if key not in cs["data_pars"]:
                                cs["data_pars"][key] = {}
                            cs["data_pars"][key]["value"] = value
                            # Также обновляем локальный объект
                            self.__current_control_sector = cs
                            break
                    break
        
        # Отмечаем документ как изменённый (только если не применяем undo/redo)
        if not self.__applying_undo_redo:
            self._set_document_modified(True)

    def _connect_widget_to_journal(
        self, tab_index, context, dict_name, key, widget_type, widget
    ):
        """Сохраняет начальное значение и подключает виджет к журналу отмены."""
        if widget_type == "title":
            return
        jkey = (tab_index, context, dict_name, key)
        self.__last_widget_values[jkey] = self._get_value_from_widget(widget_type, widget)

        def record_change():
            if self.__applying_undo_redo:
                return
            new_value = self._get_value_from_widget(widget_type, widget)
            old_value = self.__last_widget_values.get(jkey)
            if old_value == new_value:
                return
            self.__obsm.obj_undo_journal.record_form_change(
                tab_index, context, dict_name, key, widget_type, old_value, new_value
            )
            self.__last_widget_values[jkey] = new_value
            self._update_undo_redo_actions()
            # Обновляем схему при изменении виджета
            self._apply_widget_change_to_project(tab_index, dict_name, key, new_value)
            self._refresh_diagram(reset_widgets=False)

        if widget_type == "font_name":
            widget.currentFontChanged.connect(record_change)
        elif widget_type == "color":
            widget.clicked.connect(lambda: QTimer.singleShot(0, record_change))
        elif widget_type == "string_line":
            widget.textChanged.connect(record_change)
        elif widget_type in ("fill_style", "text_align", "line_style", "list_with_custom"):
            widget.currentTextChanged.connect(record_change)
        elif widget_type == "bool":
            widget.stateChanged.connect(record_change)
        elif widget_type in ("number_int_signed", "number_int", "number_float"):
            widget.valueChanged.connect(record_change)
        elif widget_type == "physical_length_calculator":
            widget.optical_length_input.valueChanged.connect(record_change)
            widget.coefficient_input.textChanged.connect(record_change)
            widget.physical_length_input.valueChanged.connect(record_change)
        elif hasattr(widget, "valueChanged"):
            widget.valueChanged.connect(record_change)
        elif hasattr(widget, "textChanged"):
            widget.textChanged.connect(record_change)
        elif hasattr(widget, "toPlainText"):
            widget.textChanged.connect(record_change)

    def _on_diagram_type_changed(self, index):
        """Обработчик смены типа схемы с записью в журнал отмены."""
        if self.__applying_undo_redo:
            return
        new_data = self.combox_type_diagram.currentData()
        old_data = self.__last_diagram_type_value
        if old_data is not None and new_data is not None:
            self.__obsm.obj_undo_journal.record_diagram_type_change(
                0, copy.deepcopy(old_data), copy.deepcopy(new_data)
            )
        self.__last_diagram_type_value = (
            copy.deepcopy(new_data) if new_data else None
        )
        self._update_undo_redo_actions()
        self._change_type_diagram(index)

    def _ensure_context_for_journal(self, tab_index, context):
        """Переключает на нужную вкладку и объект/контрольный сектор по контексту журнала."""
        self.ui.tabw_right.setCurrentIndex(tab_index)
        if tab_index == 2 and context and len(context) >= 2:
            object_id, is_node = context[0], context[1]
            data = self.__obsm.obj_project.get_data()
            if is_node:
                nodes = data.get("nodes", [])
                for i, node in enumerate(nodes):
                    if node.get("id") == object_id:
                        self._edit_object(node, i + 1, is_node=True)
                        return
            else:
                connections = data.get("connections", [])
                for i, conn in enumerate(connections):
                    if conn.get("id") == object_id:
                        self._edit_object(conn, i + 1, is_node=False)
                        return
        elif tab_index == 3 and context and len(context) >= 3:
            object_id, is_node, cs_id = context[0], context[1], context[2]
            data = self.__obsm.obj_project.get_data()
            connections = data.get("connections", [])
            for conn in connections:
                if conn.get("id") == object_id:
                    for cs in conn.get("control_sectors", []):
                        if cs.get("id") == cs_id:
                            self._edit_control_sector(cs)
                            return
                    break

    def _set_diagram_type_from_data(self, data):
        """Устанавливает тип схемы по данным (для отмены/повтора)."""
        if not data:
            return
        type_id = data.get("type_id")
        combox = self.combox_type_diagram
        for i in range(combox.count()):
            item_data = combox.itemData(i)
            if item_data and item_data.get("type_id") == type_id:
                combox.blockSignals(True)
                combox.setCurrentIndex(i)
                combox.blockSignals(False)
                self.__last_diagram_type_value = copy.deepcopy(data)
                return

    def _undo(self):
        """Отмена последнего изменения (Ctrl+Z)."""
        if not self.__obsm.obj_project.is_active() or not self.__obsm.obj_undo_journal.can_undo():
            return
        entry = self.__obsm.obj_undo_journal.pop_undo()
        if entry is None:
            return
        self.__applying_undo_redo = True
        try:
            # Сначала применяем изменения к данным проекта
            if entry.entry_type == "form":
                self._apply_widget_change_to_project(entry.tab_index, entry.dict_name, entry.key, entry.old_value)
            elif entry.entry_type == "table_row_add_pair":
                if entry.node_data:
                    self.__obsm.obj_project.delete_pair(entry.node_data, entry.connection_data)
            elif entry.entry_type == "table_row_delete_pair":
                if entry.node_data:
                    self.__obsm.obj_project.restore_pair(entry.node_data, entry.connection_data)
            elif entry.entry_type == "table_row_reorder":
                if getattr(entry, "table_id", None) == "tablew_nodes":
                    self.__obsm.obj_project.set_new_order_nodes(entry.old_value or [])
                elif getattr(entry, "table_id", None) == "tablew_connections":
                    self.__obsm.obj_project.set_new_order_connections(entry.old_value or [])
            
            # Затем переключаем контекст (это пересоздаст виджеты с новыми данными)
            self._ensure_context_for_journal(entry.tab_index, entry.context)
            QApplication.processEvents()
            
            if entry.entry_type == "form":
                # Обновляем last_widget_values для новых виджетов
                jkey = (entry.tab_index, entry.context, entry.dict_name, entry.key)
                self.__last_widget_values[jkey] = entry.old_value
            elif entry.entry_type == "diagram_type":
                self.combox_type_diagram.blockSignals(True)
                self._set_diagram_type_from_data(entry.old_value)
                self.combox_type_diagram.blockSignals(False)
                self.__last_diagram_type_value = copy.deepcopy(entry.old_value)
            elif entry.entry_type == "table_cell":
                table_w = getattr(self, entry.table_id, None)
                if table_w is not None:
                    row, col = entry.row, entry.col
                    table_w.blockSignals(True)
                    if col == 1:
                        w = table_w.cellWidget(row, 1)
                        if w and hasattr(w, "setCustomText"):
                            w.setCustomText(str(entry.old_value))
                        elif w:
                            w.setCurrentText(str(entry.old_value))
                    elif col == 2:
                        item = table_w.item(row, 2)
                        if item:
                            item.setText(str(entry.old_value))
                    table_w.blockSignals(False)
                    jkey = (entry.tab_index, entry.context, entry.table_id, (row, col))
                    self.__last_widget_values[jkey] = entry.old_value
            elif entry.entry_type in ("table_row_add_pair", "table_row_delete_pair", "table_row_reorder"):
                pass
            self.__obsm.obj_undo_journal.push_redo(entry)
            # УБРАНО: Сохранение при отмене. Изменения применяются сразу к схеме, сохранение только по Ctrl+S
            # self._save_changes_to_file_nce()
            self._refresh_diagram()  # Обновляем только визуализацию схемы
        finally:
            self.__applying_undo_redo = False
        self._update_undo_redo_actions()
        # Устанавливаем флаг изменённости после отмены
        self._set_document_modified(True)

    def _redo(self):
        """Повтор отменённого изменения (Ctrl+Y)."""
        if not self.__obsm.obj_project.is_active() or not self.__obsm.obj_undo_journal.can_redo():
            return
        entry = self.__obsm.obj_undo_journal.pop_redo()
        if entry is None:
            return
        self.__applying_undo_redo = True
        try:
            # Сначала применяем изменения к данным проекта
            if entry.entry_type == "form":
                self._apply_widget_change_to_project(entry.tab_index, entry.dict_name, entry.key, entry.new_value)
            elif entry.entry_type == "table_row_add_pair":
                if entry.node_data:
                    self.__obsm.obj_project.restore_pair(entry.node_data, entry.connection_data)
            elif entry.entry_type == "table_row_delete_pair":
                if entry.node_data:
                    self.__obsm.obj_project.delete_pair(entry.node_data, entry.connection_data)
            elif entry.entry_type == "table_row_reorder":
                if getattr(entry, "table_id", None) == "tablew_nodes":
                    self.__obsm.obj_project.set_new_order_nodes(entry.new_value or [])
                elif getattr(entry, "table_id", None) == "tablew_connections":
                    self.__obsm.obj_project.set_new_order_connections(entry.new_value or [])
            
            # Затем переключаем контекст (это пересоздаст виджеты с новыми данными)
            self._ensure_context_for_journal(entry.tab_index, entry.context)
            QApplication.processEvents()
            
            if entry.entry_type == "form":
                # Обновляем last_widget_values для новых виджетов
                jkey = (entry.tab_index, entry.context, entry.dict_name, entry.key)
                self.__last_widget_values[jkey] = entry.new_value
            elif entry.entry_type == "diagram_type":
                self.combox_type_diagram.blockSignals(True)
                self._set_diagram_type_from_data(entry.new_value)
                self.combox_type_diagram.blockSignals(False)
                self.__last_diagram_type_value = copy.deepcopy(entry.new_value)
            elif entry.entry_type == "table_cell":
                table_w = getattr(self, entry.table_id, None)
                if table_w is not None:
                    row, col = entry.row, entry.col
                    table_w.blockSignals(True)
                    if col == 1:
                        w = table_w.cellWidget(row, 1)
                        if w and hasattr(w, "setCustomText"):
                            w.setCustomText(str(entry.new_value))
                        elif w:
                            w.setCurrentText(str(entry.new_value))
                    elif col == 2:
                        item = table_w.item(row, 2)
                        if item:
                            item.setText(str(entry.new_value))
                    table_w.blockSignals(False)
                    jkey = (entry.tab_index, entry.context, entry.table_id, (row, col))
                    self.__last_widget_values[jkey] = entry.new_value
            elif entry.entry_type in ("table_row_add_pair", "table_row_delete_pair", "table_row_reorder"):
                pass
            self.__obsm.obj_undo_journal.push_undo(entry)
            # УБРАНО: Сохранение при повторе. Изменения применяются сразу к схеме, сохранение только по Ctrl+S
            # self._save_changes_to_file_nce()
            self._refresh_diagram()  # Обновляем только визуализацию схемы
        finally:
            self.__applying_undo_redo = False
        self._update_undo_redo_actions()
        # Устанавливаем флаг изменённости после повтора
        self._set_document_modified(True)

    def _update_undo_redo_actions(self):
        """Обновляет доступность действий Отмена и Повтор/Возврат по состоянию журнала."""
        active = self.__obsm.obj_project.is_active()
        self.ui.action_undo.setEnabled(bool(active and self.__obsm.obj_undo_journal.can_undo()))
        self.ui.action_redo.setEnabled(bool(active and self.__obsm.obj_undo_journal.can_redo()))

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
                nodes = self.__obsm.obj_project.get_data().get("nodes", [])
                connections = self.__obsm.obj_project.get_data().get("connections", [])
                node_data = copy.deepcopy(nodes[-1]) if nodes else None
                connection_data = copy.deepcopy(connections[-1]) if connections else None
                self.__obsm.obj_undo_journal.record_table_row_add_pair(
                    1, "elements", node_data, connection_data
                )
                self._update_undo_redo_actions()
                #
                self._refresh_diagram()
                # Устанавливаем флаг изменённости
                self._set_document_modified(True)

                # Если добавляем соединение, обновляем таблицу секторов
                if not key_dict_node_and_key_dict_connection.get("node"):
                    connections = self.__obsm.obj_project.get_data().get("connections", [])
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
                self.__obsm.obj_undo_journal.record_table_row_reorder(
                    1, "elements", "tablew_nodes", nodes, new_order_nodes
                )
                self._update_undo_redo_actions()
                self.__obsm.obj_project.set_new_order_nodes(new_order_nodes)
                #
                self._refresh_diagram()
                # Устанавливаем флаг изменённости
                self._set_document_modified(True)

    def _move_connections(self):
        if self.__obsm.obj_project.is_active():
            connections = self.__obsm.obj_project.get_data().get("connections", [])
            dialog = changeorderdialog.ChangeOrderDialog(
                connections, "connections", self
            )
            if dialog.exec():
                new_order_connections = dialog.get_data()
                self.__obsm.obj_undo_journal.record_table_row_reorder(
                    1, "elements", "tablew_connections", connections, new_order_connections
                )
                self._update_undo_redo_actions()
                self.__obsm.obj_project.set_new_order_connections(new_order_connections)
                #
                self._refresh_diagram()
                # Устанавливаем флаг изменённости
                self._set_document_modified(True)

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

        node_data = copy.deepcopy(node)
        connection_data = copy.deepcopy(connection_to_delete) if connection_to_delete else None
        self.__obsm.obj_undo_journal.record_table_row_delete_pair(
            1, "elements", node_data, connection_data
        )
        self._update_undo_redo_actions()
        # Удаляем пару (узел и соединение)
        self.__obsm.obj_project.delete_pair(node, connection_to_delete)

        self._refresh_diagram()
        # Устанавливаем флаг изменённости
        self._set_document_modified(True)

    def _reset_combobox_type_diagram(self, diagram_type_id):
        print("reset_combobox_type_diagram():\n")
        print(f"diagram_type_id={diagram_type_id}\n")
        combox_widget = self.combox_type_diagram
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
        new_diagram = self.combox_type_diagram.currentData()
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
            self._refresh_diagram()
            # Устанавливаем флаг изменённости
            self._set_document_modified(True)

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
            self.fl_diagram_parameters,
            config_diagram_parameters,
            diagram_parameters,
            combined_data_parameters=False,
            journal_tab_index=0,
            journal_dict_name="__general_diagram_parameters_widgets",
            journal_context=None,
        )
        self.parameters_group.setVisible(flag)
        self.__last_diagram_type_value = (
            copy.deepcopy(self.combox_type_diagram.currentData())
            if self.combox_type_diagram.currentData() else None
        )

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
            table_widget = self.tablew_nodes
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

        self._save_and_restore_scroll_position(self.tablew_nodes, reset_nodes)

    def _reset_table_connections(self, connections):
        def reset_connections():
            print("reset_table_connections")
            table_widget = self.tablew_connections
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
            self.tablew_connections, reset_connections
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
            table_widget = self.tw_control_sectors
            table_widget.blockSignals(True)
            table_widget.clearContents()
            table_widget.setRowCount(len(control_sectors))

            headers = ["№", "✎ Название", "✎ Физ. длина", "Редактировать"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)

            table_widget.verticalHeader().setVisible(False)

            for index, cs in enumerate(control_sectors):
                item_number = QTableWidgetItem(str(index + 1))
                item_number.setFlags(
                    item_number.flags() & ~Qt.ItemIsEditable
                )  # Только чтение
                table_widget.setItem(index, 0, item_number)

                # Создаем кастомный виджет list_with_custom для названия сектора
                cs_name = cs.get("data_pars", {}).get("cs_name", {}).get("value", "")
                
                # Создаем виджет list_with_custom с отключенной автоактивацией при наведении
                name_widget = CustomTableComboBox()
                
                # Получаем список названий секторов используя list_type
                predefined_values = self.__obsm.obj_configs.get_list_by_type("sector_names")
                
                # Добавляем значения в комбобокс
                for val in predefined_values:
                    name_widget.addItem(str(val))
                
                # Устанавливаем текущее значение
                if cs_name is not None:
                    name_widget.setCustomText(str(cs_name))
                elif predefined_values:
                    name_widget.setCurrentIndex(0)
                
                # Отключаем колесико мыши
                def ignore_wheel_event(event):
                    event.ignore()
                name_widget.wheelEvent = ignore_wheel_event
                
                # Устанавливаем виджет в ячейку
                table_widget.setCellWidget(index, 1, name_widget)

                physical_length = (
                    cs.get("data_pars", {})
                    .get("cs_physical_length", {})
                    .get("value", 0)
                )
                item_length = QTableWidgetItem(str(physical_length))
                item_length.setFlags(item_length.flags() | Qt.ItemIsEditable)

                # делегат для валидации ввода
                class FloatDelegate(QStyledItemDelegate):
                    def createEditor(self, parent, option, index):
                        editor = QLineEdit(parent)
                        validator = QRegularExpressionValidator(
                            QRegularExpression(
                                r"^\d*[,.]?\d*$"
                            ),  # Разрешены только цифры, точка или запятая
                            editor,
                        )
                        editor.setValidator(validator)
                        return editor

                table_widget.setItemDelegateForColumn(2, FloatDelegate(table_widget))
                table_widget.setItem(index, 2, item_length)

                btn_edit = QPushButton("Редактировать")
                table_widget.setCellWidget(index, 3, btn_edit)
                btn_edit.clicked.connect(partial(self._edit_control_sector, cs))

            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

            # Контекстное меню
            table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            table_widget.customContextMenuRequested.connect(
                self.control_sector_table_context_menu
            )

            self._connect_tw_control_sectors_to_journal(table_widget, control_sectors)
            table_widget.blockSignals(False)

        self._save_and_restore_scroll_position(
            self.tw_control_sectors, reset_control_sectors
        )

    def _connect_tw_control_sectors_to_journal(self, table_widget, control_sectors):
        """Подключает таблицу контрольных секторов к журналу отмены (ячейки: название, физ. длина)."""
        if not self.__current_object:
            return
        context = (self.__current_object.get("id"), self.__current_is_node)
        tab_index = 2
        table_id = "tw_control_sectors"

        handler = getattr(self, "_on_tw_control_sectors_item_changed", None)
        if handler is not None:
            try:
                table_widget.itemChanged.disconnect(handler)
            except (TypeError, RuntimeError):
                pass
        self._tw_control_sectors_journal_context = context

        for row in range(table_widget.rowCount()):
            name_widget = table_widget.cellWidget(row, 1)
            item_length = table_widget.item(row, 2)
            jkey_1 = (tab_index, context, table_id, (row, 1))
            jkey_2 = (tab_index, context, table_id, (row, 2))
            if name_widget:
                old_name = name_widget.currentText()
                self.__last_widget_values[jkey_1] = old_name

                def make_record_name(r, jk):
                    def record():
                        if self.__applying_undo_redo:
                            return
                        w = table_widget.cellWidget(r, 1)
                        new_val = w.currentText() if w else ""
                        old_val = self.__last_widget_values.get(jk)
                        if old_val == new_val:
                            return
                        self.__obsm.obj_undo_journal.record_table_cell_change(
                            tab_index, context, table_id, r, 1, old_val, new_val
                        )
                        self.__last_widget_values[jk] = new_val
                        self._update_undo_redo_actions()
                        # Устанавливаем флаг изменённости
                        self._set_document_modified(True)
                    return record

                name_widget.currentTextChanged.connect(make_record_name(row, jkey_1))
            if item_length:
                old_len = item_length.text()
                self.__last_widget_values[jkey_2] = old_len

        def on_item_changed(item):
            if self.__applying_undo_redo:
                return
            col = table_widget.column(item)
            if col != 2:
                return
            row = table_widget.row(item)
            new_val = item.text()
            jkey = (tab_index, self._tw_control_sectors_journal_context, table_id, (row, 2))
            old_val = self.__last_widget_values.get(jkey)
            if old_val == new_val:
                return
            self.__obsm.obj_undo_journal.record_table_cell_change(
                tab_index,
                self._tw_control_sectors_journal_context,
                table_id,
                row,
                2,
                old_val,
                new_val,
            )
            self.__last_widget_values[jkey] = new_val
            self._update_undo_redo_actions()
            # Устанавливаем флаг изменённости
            self._set_document_modified(True)

        self._on_tw_control_sectors_item_changed = on_item_changed
        table_widget.itemChanged.connect(on_item_changed)

    def _refresh_diagram(self, project_data=None, is_new=False, reset_widgets=True):
        """Обновить схему и синхронизировать правые виджеты с данными проекта.
        reset_widgets=False — только перерисовать схему, не пересоздавать виджеты (сохраняет фокус при редактировании).
        """
        if project_data is None:
            project_data = self.__obsm.obj_project.get_data()
        if project_data is None:
            return
        self.ui.imagewidget.run(project_data, is_new=is_new)
        if reset_widgets:
            self._reset_widgets_by_data(project_data)

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
        has_optical_length = "физ_и_опт_длины" in connection_config.get(
            "object_data", {}
        )
        has_physical_length = "физ_и_опт_длины" in connection_config.get(
            "object_data", {}
        )

        # Проверка оптической и физической длины (только если они есть в конфиге)
        if has_optical_length and has_physical_length:
            optical_length = (
                connection.get("data", {}).get("физ_и_опт_длины", {}).get("value", {}).get("од", 0)
            )
            physical_length = (
                connection.get("data", {}).get("физ_и_опт_длины", {}).get("value", {}).get("фд", 0)
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
                    .get("value", {})
                    for cs in control_sectors
                )
                physical_length = (
                    connection.get("data", {})
                    .get("физ_и_опт_длины", {})
                    .get("value", {}).get("фд", 0)
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
        # Убеждаемся, что layout создан перед его использованием
        self._create_control_tab_widgets()
        self._create_control_sector_widgets(cs)

    def _create_control_sector_widgets(self, cs):
        # Очищаем формы перед заполнением новыми виджетами
        if hasattr(self, 'fl_control_data'):
            self._clear_form_layout(self.fl_control_data)
        if hasattr(self, 'fl_control_parameters'):
            self._clear_form_layout(self.fl_control_parameters)
            
        # получаем precision_separator и precision_number из параметров диаграммы
        precision_separator, precision_number = (
            self._get_precision_separator_and_number()
        )
        
        # Получить именно через config
        control_sectors_config = self.__obsm.obj_configs.get_config_control_sectors()
        # Создаем словарь параметров для текущего контрольного сектора
        cs_data_pars = cs.get("data_pars", {})

        # Разделяем конфиг на данные и параметры
        data_config = {}
        parameters_config = {}
        
        for key, config in control_sectors_config.items():
            if config.get("is_data", False):
                data_config[key] = config
            elif config.get("is_parameter", False):
                parameters_config[key] = config
        
        # Создаем виджеты данных (всегда видимые)
        self.__control_sector_data_widgets = {}
        journal_ctx_cs = (
            (self.__current_object.get("id"), self.__current_is_node, cs.get("id"))
            if self.__current_object and cs else None
        )
        data_flag = self.create_data_widgets(
            self.__control_sector_data_widgets,
            self.fl_control_data,
            data_config,
            cs_data_pars,
            journal_tab_index=3,
            journal_dict_name="__control_sector_data_widgets",
            journal_context=journal_ctx_cs,
        )
        self.control_data_group.setVisible(data_flag)
        
        # Создаем виджеты параметров (видимость зависит от настройки)
        self.__control_sector_parameters_widgets = {}
        parameters_flag = self._create_parameters_widgets(
            self.__control_sector_parameters_widgets,
            self.fl_control_parameters,
            parameters_config,
            cs_data_pars,
            precision_separator,
            precision_number,
            combined_data_parameters=False,
            journal_tab_index=3,
            journal_dict_name="__control_sector_parameters_widgets",
            journal_context=journal_ctx_cs,
        )
        
        # Управляем видимостью параметров через action_parameters
        is_action_parameters = self.ui.action_parameters.isChecked()
        self.control_parameters_group.setVisible(parameters_flag and is_action_parameters)

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
        self._refresh_diagram()

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
        journal_tab_index=None,
        journal_dict_name=None,
        journal_context=None,
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
                config_parameter_key,  # Передаем имя поля
                is_parameters=False,
                precision_separator=precision_separator,
                precision_number=precision_number,
            )

            # Специальная обработка для поля "нач_метка" (начальная метка)
            if config_parameter_key == "нач_метка" and not self.__current_is_node:
                widget_to_add = self._create_start_mark_widget_with_continue_button(new_widget, info)
            else:
                widget_to_add = self._create_widget_with_info(new_widget, info)
            
            form_layout.addRow(label, widget_to_add)
            
            dict_widgets[config_parameter_key] = [widget_type, new_widget]
            if journal_tab_index is not None and journal_dict_name is not None:
                self._connect_widget_to_journal(
                    journal_tab_index,
                    journal_context,
                    journal_dict_name,
                    config_parameter_key,
                    widget_type,
                    new_widget,
                )

        print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _get_widget(
        self,
        widget_type,
        value,
        arguments,
        field_name=None,  # Имя поля для определения типа списка
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
            new_widget = self._create_double_spinbox(
                value, precision_separator, precision_number
            )
        #
        elif widget_type == "physical_length_calculator":
            new_widget = self._create_physical_length_calculator(
                value, precision_separator, precision_number
            )
            return new_widget
        #
        elif widget_type == "list_with_custom":
            new_widget = QComboBox()
            new_widget.setEditable(True)

            # Определяем, какой список использовать на основе параметра list_type
            list_type = arguments.get("list_type")
            if list_type:
                # Используем новый принцип присвоения на основе типа списка
                predefined_values = self.__obsm.obj_configs.get_list_by_type(list_type)
            else:
                # Fallback для обратной совместимости
                if field_name == "cs_name":
                    predefined_values = self.__obsm.obj_configs.get_sector_names_list()
                else:
                    predefined_values = self.__obsm.obj_configs.get_cable_list()
                
            if not predefined_values:
                # Если централизованный список пуст, используем локальный как fallback
                predefined_values = arguments.get("list", [])
                
            for val in predefined_values: 
                new_widget.addItem(str(val))
    
            if value is not None:  
                index = new_widget.findText(str(value))
                if index >= 0:
                    new_widget.setCurrentIndex(index)
                else:
                    new_widget.setCurrentText(str(value))
            elif predefined_values:
                new_widget.setCurrentIndex(0)
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

    def _create_double_spinbox(self, value, precision_separator, precision_number):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(0, 2147483647)
        spinbox.setValue(value)
        if precision_separator is not None:
            spinbox.setDecimals(precision_number)
        if precision_separator == 0:
            locale = QLocale(QLocale.Russian)
        else:
            locale = QLocale(QLocale.C)
        spinbox.setLocale(locale)
        return spinbox
    
    def _create_physical_length_calculator(self, value, precision_separator, precision_number):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Уменьшаем отступы между элементами
        
        # Создаем делегат для валидации ввода
        class FloatValidator(QRegularExpressionValidator):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setRegularExpression(QRegularExpression(r"^\d*[,.]?\d*$"))

        # Первая строка: Оптическая длина и Коэффициент
        first_row = QWidget()
        first_row_layout = QHBoxLayout(first_row)
        first_row_layout.setContentsMargins(0, 0, 0, 0)
        first_row_layout.setSpacing(10)
        
        # Оптическая длина
        optical_label = QLabel("Оптическая длина")
        optical_input = self._create_double_spinbox(
            value.get("од", 0), 
            precision_separator, 
            precision_number
        )
        optical_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Коэффициент
        coeff_label = QLabel("Коэф.")
        coefficient_input = QLineEdit()
        coefficient_input.setValidator(FloatValidator())
        coefficient_input.setText(str(value.get("к", 0.97)))
        coefficient_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        first_row_layout.addWidget(optical_label)
        first_row_layout.addWidget(optical_input, stretch=1)
        first_row_layout.addWidget(coeff_label)
        first_row_layout.addWidget(coefficient_input, stretch=1)
        
        # Вторая строка: Физическая длина и кнопка
        second_row = QWidget()
        second_row_layout = QHBoxLayout(second_row)
        second_row_layout.setContentsMargins(0, 0, 0, 0)
        second_row_layout.setSpacing(10)
        
        # Физическая длина
        physical_label = QLabel("Физическая длина")
        physical_input = self._create_double_spinbox(
            value.get("фд", 0), 
            precision_separator, 
            precision_number
        )
        physical_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Кнопка расчета
        calculate_btn = QPushButton("по Коэф.")
        calculate_btn.setFixedWidth(80)
        
        second_row_layout.addWidget(physical_label)
        second_row_layout.addWidget(physical_input, stretch=1)
        second_row_layout.addWidget(calculate_btn)
        
        # Добавляем строки в основной layout
        layout.addWidget(first_row)
        layout.addWidget(second_row)
        
        # Сохраняем ссылки на виджеты как атрибуты
        widget.optical_length_input = optical_input
        widget.coefficient_input = coefficient_input
        widget.physical_length_input = physical_input
        
        # Подключаем обработчик кнопки
        def calculate():
            optical = optical_input.value()
            try:
                coeff = float(coefficient_input.text().replace(",", "."))
            except (ValueError, TypeError):
                coeff = 0.97  # Значение по умолчанию при ошибке преобразования
            physical_input.setValue(optical * coeff)
        
        calculate_btn.clicked.connect(calculate)
        return widget

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
        journal_tab_index=None,
        journal_dict_name=None,
        journal_context=None,
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
        
        # Если action_parameters не отмечен, не показываем параметры
        if not is_action_parameters:
            return False
            
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
                config_parameter_key,  # Передаем имя поля
                is_parameters=True,
                precision_separator=precision_separator,
                precision_number=precision_number,
            )

            widget_to_add = self._create_widget_with_info(new_widget, info)
            form_layout.addRow(label, widget_to_add)

            if widget_type != "title":
                dict_widgets[config_parameter_key] = [widget_type, new_widget]
                if journal_tab_index is not None and journal_dict_name is not None:
                    self._connect_widget_to_journal(
                        journal_tab_index,
                        journal_context,
                        journal_dict_name,
                        config_parameter_key,
                        widget_type,
                        new_widget,
                    )

        # print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _add_control_sector(self, obj):
        control_sectors = self.__obsm.obj_project.add_control_sector(
            obj, penultimate=True
        )
        #
        self._refresh_diagram()
        self._reset_table_control_sectors(control_sectors)
        # Устанавливаем флаг изменённости
        self._set_document_modified(True)

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
            self._refresh_diagram()
            self._reset_table_control_sectors(control_sectors)
            # Устанавливаем флаг изменённости
            self._set_document_modified(True)

    def _delete_control_sector(self, obj, selected_cs):
        control_sectors = self.__obsm.obj_project.delete_control_sector(
            obj, selected_cs
        )
        #
        self._refresh_diagram()
        self._reset_table_control_sectors(control_sectors)
        # Устанавливаем флаг изменённости
        self._set_document_modified(True)

    def _create_editor_control_sectors_by_object(self, obj, is_node=False):
        self.control_sectors_group.setVisible(not is_node)
        
        # Перемещаем спейсер в конец после изменения видимости групп
        self._reposition_editor_spacer()
        #
        self.tw_control_sectors.setVisible(not is_node)
        self.btn_add_control_sector.setVisible(not is_node)
        self.btn_move_control_sectors.setVisible(not is_node)
        # отключаем старые обработчики
        try:
            self.btn_add_control_sector.clicked.disconnect()
            self.btn_move_control_sectors.clicked.disconnect()
        except:
            pass
        #
        self.btn_add_control_sector.clicked.connect(
            partial(self._add_control_sector, obj)
        )
        self.btn_move_control_sectors.clicked.connect(
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
        journal_ctx = (obj.get("id"), is_node)
        flag = self._create_parameters_widgets(
            self.__editor_object_parameters_widgets,
            self.fl_object_parameters,
            config_object_parameters,
            object_parameters,
            combined_data_parameters=False,
            journal_tab_index=2,
            journal_dict_name="__editor_object_parameters_widgets",
            journal_context=journal_ctx,
        )
        self.object_parameters_group.setVisible(flag)
        #
        flag = self._create_parameters_widgets(
            self.__editor_type_object_parameters_widgets,
            self.fl_type_object_parameters,
            config_type_object_parameters,
            object_parameters,
            combined_data_parameters=False,
            journal_tab_index=2,
            journal_dict_name="__editor_type_object_parameters_widgets",
            journal_context=journal_ctx,
        )
        self.type_object_parameters_group.setVisible(flag)
        #
        flag = self._create_parameters_widgets(
            self.__editor_objects_parameters_widgets,
            self.fl_objects_parameters,
            config_objects_parameters,
            object_parameters,
            combined_data_parameters=False,
            journal_tab_index=2,
            journal_dict_name="__editor_objects_parameters_widgets",
            journal_context=journal_ctx,
        )
        self.objects_parameters_group.setVisible(flag)
        
        # Перемещаем спейсер в конец после изменения видимости всех групп параметров
        self._reposition_editor_spacer()

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
        journal_ctx = (obj.get("id"), is_node)
        flag = self.create_data_widgets(
            self.__editor_object_data_widgets,
            self.fl_object_data,
            config_object_data,
            object_data,
            journal_tab_index=2,
            journal_dict_name="__editor_object_data_widgets",
            journal_context=journal_ctx,
        )
        self.object_data_group.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_type_object_data_widgets,
            self.fl_type_object_data,
            config_type_object_data,
            object_data,
            journal_tab_index=2,
            journal_dict_name="__editor_type_object_data_widgets",
            journal_context=journal_ctx,
        )
        self.type_object_data_group.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_objects_data_widgets,
            self.fl_objects_data,
            config_objects_data,
            object_data,
            journal_tab_index=2,
            journal_dict_name="__editor_objects_data_widgets",
            journal_context=journal_ctx,
        )
        self.objects_data_group.setVisible(flag)
        
        # Перемещаем спейсер в конец после изменения видимости всех групп данных
        self._reposition_editor_spacer()
    
    def _reposition_editor_spacer(self):
        """Перемещает вертикальный спейсер в конец layout'а для правильного позиционирования групп"""
        if hasattr(self, 'vertical_spacer'):
            layout = self.ui.editor_scrollarea_contents.layout()
            # Удаляем спейсер из текущей позиции
            layout.removeWidget(self.vertical_spacer)
            # Добавляем спейсер в конец с растягивающим фактором
            layout.addWidget(self.vertical_spacer, 1)

    def node_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы узлов"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.tablew_nodes.currentRow()
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
        action = menu.exec_(self.tablew_nodes.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if selected_row >= 0 and selected_node:
            if action == copy_data_action:
                self.__obsm.obj_project.copy_node_data(selected_node)
            elif action == paste_data_action:
                self.__obsm.obj_project.paste_node_data(selected_node)
                # Обновляем интерфейс
                self._refresh_diagram()
                # Устанавливаем флаг изменённости
                self._set_document_modified(True)
            elif action == delete_with_left_action:
                self._delete_node_with_connection(selected_node, "left")
            elif action == delete_with_right_action:
                self._delete_node_with_connection(selected_node, "right")

    def connection_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы соединений"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.tablew_connections.currentRow()
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
        action = menu.exec_(self.tablew_connections.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if selected_row >= 0 and selected_connection:
            if action == copy_data_action:
                self.__obsm.obj_project.copy_connection_data(selected_connection)
            elif action == paste_data_action:
                self.__obsm.obj_project.paste_connection_data(selected_connection)
                # Обновляем интерфейс
                self._refresh_diagram()
                # Устанавливаем флаг изменённости
                self._set_document_modified(True)

    def control_sector_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы контрольных секторов"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.tw_control_sectors.currentRow()
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
        action = menu.exec_(self.tw_control_sectors.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if action == copy_data_action and selected_cs:
            self.__obsm.obj_project.copy_control_sector_data(selected_cs)
        elif action == paste_data_action and selected_cs:
            self.__obsm.obj_project.paste_control_sector_data(selected_cs)
            # Обновляем интерфейс
            self._refresh_diagram()
            self._reset_table_control_sectors(control_sectors)
            # Устанавливаем флаг изменённости
            self._set_document_modified(True)
        elif action == delete_action and selected_cs:
            self._delete_control_sector(obj, selected_cs)

    def _clear_error_messages(self):
        """
        Очищает все сообщения об ошибках из контейнера vl_edit_errors.
        """
        while self.vl_edit_errors.count():
            item = self.vl_edit_errors.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.errors_group.setVisible(False)

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
            .get("физ_и_опт_длины", {}).get("value", {}).get("фд", 0)
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
            error_message = f"Сумма физ. длин секторов ({total_length}) > физ. длины соединения ({connection_length}) на {difference:.3f}"
        elif comparison_result == -1:
            difference = connection_length - total_length
            error_message = f"Сумма физ. длин секторов ({total_length}) < физ. длины соединения ({connection_length}) на {difference:.3f}"

        if error_message:
            self._add_error_message(error_message)

    def _add_error_message(self, message):
        self.errors_group.setVisible(True)

        # Используем QLabel вместо QTextEdit
        error_label = QLabel()
        error_label.setText(message)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("color: #e29c4a;")

        self.vl_edit_errors.addWidget(error_label)

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

    def _create_start_mark_widget_with_continue_button(self, widget, info):
        """
        Создает виджет для начальной метки с кнопкой "Продолжить метки"
        """
        # Создаем горизонтальный layout для виджета и кнопки
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(5)
        
        # Добавляем основной виджет (поле ввода начальной метки)
        h_layout.addWidget(widget)
        
        # Создаем кнопку "Продолжить метки"
        continue_button = QPushButton("Продолжить метки")
        continue_button.setToolTip("Установить начальную метку равной конечной метке предыдущего соединения")
        continue_button.clicked.connect(lambda: self._continue_mark_from_previous_connection(widget))
        h_layout.addWidget(continue_button)
        
        # Если есть информация, добавляем кнопку с информацией
        if info:
            info_button = QToolButton()
            info_button.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
            info_button.setToolTip("Нажмите для получения информации")
            info_button.clicked.connect(lambda: self._show_info_dialog(info))
            h_layout.addWidget(info_button)
        
        return h_layout

    def _continue_mark_from_previous_connection(self, widget):
        """
        Устанавливает начальную метку равной конечной метке предыдущего соединения
        """
        try:
            # Получаем текущее соединение
            current_connection = self.__current_object
            if not current_connection:
                return
            
            # Получаем все соединения из проекта
            project_data = self.__obsm.obj_project.get_data()
            connections = project_data.get("connections", [])
            
            # Находим индекс текущего соединения
            current_index = None
            for i, conn in enumerate(connections):
                if conn == current_connection:
                    current_index = i
                    break
            
            if current_index is None or current_index == 0:
                # Это первое соединение, нет предыдущего
                QMessageBox.information(self, "Информация", "Это первое соединение. Нет предыдущего соединения для продолжения метки.")
                return
            
            # Получаем предыдущее соединение
            previous_connection = connections[current_index - 1]
            
            # Получаем начальную метку и физическую длину предыдущего соединения
            prev_start_mark = previous_connection.get("data", {}).get("нач_метка", {}).get("value", 0)
            prev_physical_length = 0
            
            # Получаем физическую длину из поля "физ_и_опт_длины"
            prev_physical_length_data = previous_connection.get("data", {}).get("физ_и_опт_длины", {}).get("value", {})
            if isinstance(prev_physical_length_data, dict):
                prev_physical_length = prev_physical_length_data.get("фд", 0)
            else:
                prev_physical_length = prev_physical_length_data
            
            # Вычисляем конечную метку предыдущего соединения
            prev_end_mark = prev_start_mark + prev_physical_length
            
            # Устанавливаем значение в виджет
            if isinstance(widget, QSpinBox):
                widget.setValue(int(prev_end_mark))
            else:
                widget.setText(str(prev_end_mark))
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось продолжить метку: {str(e)}")

    def eventFilter(self, obj, event):
        """
        Фильтр событий для обработки нажатия Enter.
        ЗАКОММЕНТИРОВАНО: Сохранение по ENTER. Теперь сохранение только по Ctrl+S.
        """
        from PySide6.QtCore import QEvent
        # from PySide6.QtGui import QKeyEvent  # Закомментировано вместе с обработкой Enter
        
        if event.type() == QEvent.KeyPress:
            pass  # Обработка Enter закомментирована, сохранение только по Ctrl+S
            # key_event = QKeyEvent(event)  # Закомментировано вместе с обработкой Enter
            # ЗАКОММЕНТИРОВАНО: Сохранение по ENTER. Теперь сохранение только по Ctrl+S
            # if key_event.key() == Qt.Key_Return or key_event.key() == Qt.Key_Enter:
            #     # Получаем виджет с фокусом
            #     focused_widget = QApplication.focusWidget()
            #     
            #     # Проверяем, является ли виджет с фокусом текстовым полем
            #     if focused_widget is not None:
            #         widget_class_name = focused_widget.__class__.__name__
            #         if widget_class_name in ['QLineEdit', 'QTextEdit', 'QPlainTextEdit']:
            #             # Если фокус в текстовом поле, не выполняем сохранение
            #             return False
            #     
            #     # Если фокус не в текстовом поле, выполняем сохранение
            #     if self.__obsm.obj_project.is_active():
            #         self._save_changes_to_file_nce()
            #     return True
        
        return False

    def _edit_cable_lists(self):
        """Открывает диалог управления списками кабелей"""
        dialog = cablelistsdialog.CableListsDialog(self.__obsm, self)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            # Обновляем интерфейс после изменения списков кабелей
            self._refresh_cable_lists_in_ui()
            
    def _edit_sector_names(self):
        """Открывает диалог управления списками названий секторов"""
        dialog = sectornamesdialog.SectorNamesDialog(self.__obsm, self)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            # Обновляем интерфейс после изменения списков названий секторов
            self._refresh_sector_names_in_ui()
            
    def _open_settings(self):
        """Открывает диалог настроек"""
        dialog = settingsdialog.SettingsDialog(self.__obsm)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            # Настройки были сохранены, обновляем интерфейс если нужно
            pass
            
    def _refresh_cable_lists_in_ui(self):
        """Обновляет список кабелей в интерфейсе"""
        # Получаем список кабелей
        cables = self.__obsm.obj_configs.get_cable_list()
        
        # Обновляем все комбобоксы с кабелями в интерфейсе
        # Это нужно сделать для всех соединений, которые используют списки кабелей
        project_data = self.__obsm.obj_project.get_data()
        if project_data:
            # Обновляем виджеты на текущей вкладке
            if self.ui.tabw_right.currentIndex() == 2:  # Вкладка редактирования
                self._refresh_editor_widgets()
            elif self.ui.tabw_right.currentIndex() == 0:  # Основная вкладка
                self._reset_widgets_by_data(project_data)
                
    def _refresh_editor_widgets(self):
        """Обновляет виджеты редактора после изменения списков кабелей"""
        if self.__current_object and not self.__current_is_node:
            # Обновляем виджеты данных соединения
            self._create_editor_data_widgets_by_object(self.__current_object, self.__current_is_node)
            
    def _refresh_sector_names_in_ui(self):
        """Обновляет список названий секторов в интерфейсе"""
        # Получаем список названий секторов
        sector_names = self.__obsm.obj_configs.get_sector_names_list()
        
        # Обновляем все комбобоксы с названиями секторов в интерфейсе
        project_data = self.__obsm.obj_project.get_data()
        if project_data:
            # Обновляем виджеты на текущей вкладке
            if self.ui.tabw_right.currentIndex() == 2:  # Вкладка редактирования
                self._refresh_editor_widgets()
            elif self.ui.tabw_right.currentIndex() == 0:  # Основная вкладка
                self._reset_widgets_by_data(project_data)
            elif self.ui.tabw_right.currentIndex() == 3:  # Вкладка редактирования контрольного сектора
                # Обновляем виджеты контрольного сектора
                if self.__current_object:
                    self._create_editor_control_sectors_by_object(self.__current_object, self.__current_is_node)

    def hide_right_panel(self):
        """Скрывает правый блок с вкладками"""
        self.ui.gb_right.setVisible(False)
    
    def closeEvent(self, event):
        """Обработчик закрытия окна - проверяет несохранённые изменения"""
        if self._check_unsaved_changes():
            event.accept()
        else:
            event.ignore()

    def show_right_panel(self):
        """Показывает правый блок с вкладками"""
        self.ui.gb_right.setVisible(True)


