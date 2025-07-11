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

