from PySide6.QtCore import Qt, QSize, QRect, QCoreApplication, QMetaObject
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QGroupBox, QTabWidget,
    QScrollArea, QFrame, QFormLayout, QMenuBar, QMenu, QToolBar, QStatusBar
)

from package.controllers.imagewidget import ImageWidget
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(1144, 653)
        MainWindow.setMinimumSize(QSize(0, 0))

        # Actions
        self.action_new = QAction(QIcon.fromTheme("document-new", QIcon(":/white-icons/resources/white-icons/add-file.svg")), "Новый", MainWindow)
        self.action_new.setShortcut("Ctrl+N")

        self.action_open = QAction(QIcon(":/white-icons/resources/white-icons/open.svg"), "Открыть", MainWindow)
        self.action_open.setShortcut("Ctrl+O")

        self.action_save = QAction(QIcon(":/white-icons/resources/white-icons/save.svg"), "Сохранить", MainWindow)
        self.action_save.setEnabled(False)

        self.action_saveas = QAction(QIcon(":/white-icons/resources/white-icons/save.svg"), "Сохранить как", MainWindow)
        self.action_saveas.setEnabled(False)
        self.action_saveas.setShortcut("Ctrl+Shift+S")

        self.action_zoomin = QAction(QIcon(":/white-icons/resources/white-icons/zoom-in.svg"), "Увеличить", MainWindow)
        self.action_zoomin.setEnabled(False)
        self.action_zoomin.setShortcut("Ctrl++")

        self.action_zoomout = QAction(QIcon(":/white-icons/resources/white-icons/zoom-out.svg"), "Уменьшить", MainWindow)
        self.action_zoomout.setEnabled(False)
        self.action_zoomout.setShortcut("Ctrl+-")

        self.action_edit_variables = QAction(QIcon(":/white-icons/resources/white-icons/text-editor.svg"), "Редактор переменных", MainWindow)
        self.action_edit_variables.setEnabled(False)

        self.action_zoomfitpage = QAction(QIcon(":/white-icons/resources/white-icons/zoom-fit-width.svg"), "По ширине", MainWindow)
        self.action_zoomfitpage.setCheckable(True)
        self.action_zoomfitpage.setEnabled(False)

        self.action_export_to_image = QAction(QIcon(":/white-icons/resources/white-icons/export.svg"), "Экспорт в изображение", MainWindow)
        self.action_export_to_image.setEnabled(False)

        self.action_edit_templates = QAction(QIcon(":/white-icons/resources/white-icons/template.svg"), "Редактор шаблонов", MainWindow)
        self.action_edit_templates.setEnabled(False)

        self.action_edit_composition = QAction(QIcon(":/white-icons/resources/white-icons/items-tree.svg"), "Редактор состава ИД", MainWindow)
        self.action_edit_composition.setEnabled(False)

        self.action_clear_trash = QAction(QIcon(":/white-icons/resources/white-icons/trash.svg"), "Очистка от мусора", MainWindow)

        self.action_edit_cable_lists = QAction(QIcon(":/white-icons/resources/white-icons/list.svg"), "Список кабелей", MainWindow)
        self.action_edit_sector_names = QAction(QIcon(":/white-icons/resources/white-icons/list.svg"), "Список названий секторов", MainWindow)

        self.action_parameters = QAction(QIcon(":/white-icons/resources/white-icons/show-properties.svg"), "Показать/скрыть параметры", MainWindow)
        self.action_parameters.setCheckable(True)

        self.light_action = QAction("Светлая", MainWindow)
        self.dark_action = QAction("Тёмная", MainWindow)

        self.action_settings = QAction(QIcon(":/white-icons/resources/white-icons/settings.svg"), "Настройки", MainWindow)
        self.action_settings.setShortcut("Ctrl+,")

        # Центральный виджет и лейаут
        self.centralwidget = QWidget(MainWindow)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(4, 0, 4, 0)

        # Сплиттер центральной области
        self.centralwidget_splitter = QSplitter(Qt.Horizontal, self.centralwidget)

        # Левая часть (центральная область)
        self.gb_center = QWidget(self.centralwidget_splitter)
        self.gb_center.setMinimumSize(QSize(250, 0))
        self.verticalLayout = QVBoxLayout(self.gb_center)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.imagewidget = ImageWidget(self.gb_center)
        self.verticalLayout.addWidget(self.imagewidget)
        self.verticalLayout.setStretch(0, 1)

        # Правая часть (группа с табами)
        self.gb_right = QWidget(self.centralwidget_splitter)
        self.gb_right.setMinimumSize(QSize(560, 0))
        self.verticalLayout_2 = QVBoxLayout(self.gb_right)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)

        self.tabw_right = QTabWidget(self.gb_right)

        # Вкладка "Основные настройки"
        self.tab_general = QWidget()
        self.verticalLayout_5 = QVBoxLayout(self.tab_general)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.sa_general = QScrollArea(self.tab_general)
        self.sa_general.setFrameShape(QFrame.NoFrame)
        self.sa_general.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sa_general.setWidgetResizable(True)
        self.sa_general_contents = QWidget()
        self.verticalLayout_8 = QVBoxLayout(self.sa_general_contents)
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.sa_general.setWidget(self.sa_general_contents)
        self.verticalLayout_5.addWidget(self.sa_general)
        self.tabw_right.addTab(self.tab_general, "Основные настройки")

        # Вкладка "Элементы"
        self.tab_elements = QWidget()
        self.verticalLayout_3 = QVBoxLayout(self.tab_elements)
        self.verticalLayout_3.setSpacing(6)
        self.splitter = QSplitter(Qt.Vertical, self.tab_elements)
        self.verticalLayoutWidget = QWidget()
        self.vl_nodes = QVBoxLayout(self.verticalLayoutWidget)
        self.vl_nodes.setSpacing(4)
        self.vl_nodes.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget()
        self.vl_connections = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vl_connections.setSpacing(4)
        self.vl_connections.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.verticalLayoutWidget_2)
        self.verticalLayout_3.addWidget(self.splitter)
        self.tabw_right.addTab(self.tab_elements, "Элементы")

        # Вкладка "Редактирование"
        self.tab_editor = QWidget()
        self.verticalLayout_7 = QVBoxLayout(self.tab_editor)
        self.verticalLayout_7.setSpacing(9)
        self.verticalLayout_7.setContentsMargins(9, 9, 9, 9)
        self.editor_scrollarea = QScrollArea(self.tab_editor)
        self.editor_scrollarea.setFrameShape(QFrame.NoFrame)
        self.editor_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor_scrollarea.setWidgetResizable(True)
        self.editor_scrollarea_contents = QWidget()
        self.verticalLayout_4 = QVBoxLayout(self.editor_scrollarea_contents)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.editor_scrollarea.setWidget(self.editor_scrollarea_contents)
        self.verticalLayout_7.addWidget(self.editor_scrollarea)
        self.tabw_right.addTab(self.tab_editor, "Редактирование")

        # Вкладка "Редактирование контрольного сектора"
        self.tab_control = QWidget()
        self.verticalLayout_6 = QVBoxLayout(self.tab_control)
        self.fl_control = QFormLayout()
        self.verticalLayout_6.addLayout(self.fl_control)
        self.tabw_right.addTab(self.tab_control, "Редактирование контрольного сектора")

        self.verticalLayout_2.addWidget(self.tabw_right)

        # Добавляем группы в сплиттер
        self.centralwidget_splitter.addWidget(self.gb_center)
        self.centralwidget_splitter.addWidget(self.gb_right)
        self.horizontalLayout.addWidget(self.centralwidget_splitter)

        MainWindow.setCentralWidget(self.centralwidget)

        # Меню и тулбары
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_file = QMenu("Файл", self.menu_bar)
        self.menu = QMenu("Прочее", self.menu_bar)
        self.menu_bar.addMenu(self.menu_file)
        self.menu_bar.addMenu(self.menu)
        MainWindow.setMenuBar(self.menu_bar)

        self.tb_main = QToolBar("Панель инструментов", MainWindow)
        self.tb_main.setIconSize(QSize(32, 24))
        self.tb_main.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.tb_main)

        self.status_bar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.status_bar)

        # Заполнение меню и тулбара
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_export_to_image)

        self.menu.addAction(self.action_parameters)
        self.menu.addAction(self.action_edit_cable_lists)
        self.menu.addAction(self.action_edit_sector_names)
        self.menu.addSeparator()
        self.menu.addAction(self.action_settings)

        self.tb_main.addAction(self.action_new)
        self.tb_main.addAction(self.action_open)
        self.tb_main.addAction(self.action_save)
        self.tb_main.addAction(self.action_export_to_image)
        self.tb_main.addSeparator()
        self.tb_main.addAction(self.action_parameters)

        # По умолчанию открыта вкладка "Редактирование контрольного сектора"
        self.tabw_right.setCurrentIndex(3)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Автоматизация ИД")
