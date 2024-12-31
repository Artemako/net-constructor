from PySide6.QtWidgets import (
    QMainWindow,
    QMenu,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
    QCheckBox
)

from PySide6.QtCore import Qt

import package.controllers.style as style
import package.controllers.imagewidget as imagewidget

import package.components.nodeconnectionselectdialog as nodeconnectionselectdialog
import package.components.nodeconnectiondeletedialog as nodeconnectiondeletedialog

import package.ui.mainwindow_ui as mainwindow_ui

import json
from functools import partial


class MainWindow(QMainWindow):
    def __init__(self, obsm):
        self.__obsm = obsm
        #
        self.__nodes_data = []
        self.__connections_data = []
        #
        self.__current_object = None
        self.__current_is_node = None
        #
        self.__data_widgets = {}
        self.__metrics_widgets = {}
        #
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        #
        self.ui.imagewidget.set_obsm(self.__obsm)
        # config
        self.config()

    def tab_right_changed(self, index):
        if index in [0, 1]:
            self.ui.tabw_right.tabBar().setTabVisible(2, False)

    def config(self):
        # СТИЛЬ
        obj_style = style.Style()
        obj_style.set_style_for(self)
        #
        self.ui.centralwidget_splitter.setSizes([806, 560])
        #
        self.ui.tabw_right.tabBar().setTabVisible(2, False)
        self.ui.tabw_right.currentChanged.connect(self.tab_right_changed)

        # self.update_menu_recent_projects()
        #
        self.ui.btn_addnode.clicked.connect(self.add_node)
        self.ui.btn_deletenode.clicked.connect(self.delete_node)
        #
        # self.ui.tabw_right
        # создание нового файла
        self.ui.action_new.triggered.connect(self.create_file_nce)
        # октрытие файла
        self.ui.action_open.triggered.connect(self.open_file_nce)
        # сохранение текущих данных
        self.ui.action_save.triggered.connect(self.save_changes_to_file_nce)
        # экспорт в картинку
        self.ui.action_export_to_image.triggered.connect(self.export_to_image)
        #


    def start_qt_actions(self):
        self.ui.action_new.setEnabled(True)
        self.ui.action_open.setEnabled(True)
        self.ui.action_save.setEnabled(True)
        self.ui.action_export_to_image.setEnabled(True)

    def create_file_nce(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, " ", "", "NCE (пока json) files (*.json)"
        )
        if file_name:
            # TODO Выбор типа диаграммы
            
            #
            self.__obsm.obj_project.create_new_project(file_name)
            #
            data = self.__obsm.obj_project.get_data()
            #
            self.ui.imagewidget.run(data)
            self.reset_widgets_by_data(data)
            self.start_qt_actions()

    def open_file_nce(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, " ", "", "NCE (пока json) files (*.json)"
        )
        if file_name:
            self.__obsm.obj_project.open_project(file_name)
            #
            data = self.__obsm.obj_project.get_data()
            #
            self.ui.imagewidget.run(data)
            self.reset_widgets_by_data(data)
            self.start_qt_actions()

    def save_changes_to_file_nce(self):
        if self.__obsm.obj_project.is_active():
            new_diagramm_settings = {
                "diagramm_type_id" : self.ui.combox_type.currentIndex(),
                "diagramm_name" : self.ui.combox_type.currentText()
            }
            #
            new_image_settings = {
                "width": self.ui.sb_width.value(),
                "height": self.ui.sb_height.value(),
                "start_x": self.ui.sb_start_x.value(),
                "start_y": self.ui.sb_start_y.value(),
            }
            #
            new_data = {}
            new_metrics = {}
            #
            is_edit = False
            if self.ui.tabw_right.currentIndex() == 2:
                is_edit = True
                for key, widget in self.__data_widgets.items():
                    # widget_type = pair[0]
                    # widget = pair[1]
                    new_data[key] = {
                        "value": widget.toPlainText()
                    }
                #
                for key, pair in self.__metrics_widgets.items():
                    widget_type = pair[0]
                    widget = pair[1]
                    if widget_type == "bool":
                        new_metrics[key] = {
                            "value": widget.isChecked()
                        }
                    else:
                        new_metrics[key] = {
                            "value": widget.value()
                        }
            #
            config_nodes = self.__obsm.obj_configs.get_nodes()
            config_connections = self.__obsm.obj_configs.get_connections()
            #
            self.__obsm.obj_project.save_project(self.__current_object, self.__current_is_node, is_edit, config_nodes, config_connections, new_diagramm_settings, new_image_settings, new_data, new_metrics)
            data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(data)
            self.reset_widgets_by_data(data)

    def export_to_image(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, " ", "", "PNG images (*.png)"
        )
        if file_name:
            print(f"save_image to {file_name}")
            self.ui.imagewidget.save_image(file_name)


    def add_node(self):
        if self.__obsm.obj_project.is_active():
            config_nodes = self.__obsm.obj_configs.get_nodes()  
            config_connections = self.__obsm.obj_configs.get_connections()
            dialog = nodeconnectionselectdialog.NodeConnectSelectDialog(config_nodes, config_connections, self)
            if dialog.exec():
                key_dict_node_and_key_dict_connection = dialog.get_selected_key_dict_node_and_key_dict_connection()
                self.__obsm.obj_project.add_pair(key_dict_node_and_key_dict_connection)
                #
                data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(data)
                self.reset_widgets_by_data(data)


    def delete_node(self, node):
        if self.__obsm.obj_project.is_active():
            nodes = self.__obsm.obj_project.get_data().get("nodes", [])
            connections = self.__obsm.obj_project.get_data().get("connections", [])
            dialog = nodeconnectiondeletedialog.NodeConnectionDeleteDialog(nodes, connections, self)
            if dialog.exec():
                selected_data = dialog.get_selected_node_and_connection()
                node = selected_data.get("node")
                connection = selected_data.get("connection")
                self.__obsm.obj_project.delete_pair(node, connection)
                #
                data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(data)
                self.reset_widgets_by_data(data)

    def reset_tab_general(self, diagramm_type_id, width, height, start_x, start_y):
        print("reset_tab_general")
        # очистка типа
        self.ui.combox_type.clear()
        self.ui.combox_type.addItem(
            "Скелетная схема ВОЛП и основные данные цепей кабеля", 0
        )
        self.ui.combox_type.setCurrentIndex(diagramm_type_id)
        # задать ширину и высоту
        self.ui.sb_width.setValue(width)
        self.ui.sb_height.setValue(height)
        # задать стартовые координаты
        self.ui.sb_start_x.setValue(start_x)
        self.ui.sb_start_y.setValue(start_y)

    def reset_tab_elements(self, nodes, connections):
        nodes = sorted(nodes, key=lambda node: node.get("order", 0))
        connections = sorted(
            connections, key=lambda connection: connection.get("order", 0)
        )
        self.reset_table_nodes(nodes)
        self.reset_table_connections(connections)

    def reset_table_nodes(self, nodes):
        print("reset_table_nodes")
        self.__nodes_data = nodes
        table_widget = self.ui.tablew_nodes
        table_widget.blockSignals(True)
        table_widget.clearContents()
        table_widget.setRowCount(len(nodes))
        headers = ["Название", "Перенос", "Редактировать"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        print("NODES", nodes)
        for index, node in enumerate(nodes):
            print("NODE", node)
            node_name = node.get("data", {}).get("название", {}).get("value", "")
            item = QTableWidgetItem(node_name)
            table_widget.setItem(index, 0, item)
            #
            is_wrap = node.get("is_wrap", False)
            btn_wrap = QPushButton("Не переносить" if is_wrap else "Переносить")
            table_widget.setCellWidget(index, 1, btn_wrap)
            btn_wrap.clicked.connect(partial(self.wrap_node, node))
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 2, btn_edit)
            btn_edit.clicked.connect(partial(self.edit_object, node, is_node=True))

        # Настраиваем режимы изменения размера для заголовков
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.blockSignals(False)  

    def reset_table_connections(self, connections):
        print("reset_table_connections")
        self.__connections_data = connections
        table_widget = self.ui.tablew_connections
        table_widget.blockSignals(True)
        table_widget.clearContents()
        table_widget.setRowCount(len(connections))
        headers = ["Название", "Соединение", "Редактировать"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        for index, connection in enumerate(connections):
            connection_name = (
                connection.get("data", {}).get("название", {}).get("value", "")
            )
            item = QTableWidgetItem(connection_name)
            table_widget.setItem(index, 0, item)
            #
            connection_cell = QTableWidgetItem(f"{index + 1}—{index + 2}")
            table_widget.setItem(index, 1, connection_cell)
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 2, btn_edit)
            btn_edit.clicked.connect(partial(self.edit_object, connection, is_node=False))

        # Настраиваем режимы изменения размера для заголовков
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.blockSignals(False) 


    def reset_widgets_by_data(self, data):
        #
        diagramm_type_id = data.get("diagramm_settings", {}).get("diagramm_type_id", 0)
        width = data.get("image_settings", {}).get("width", 0)
        height = data.get("image_settings", {}).get("height", 0)
        start_x = data.get("image_settings", {}).get("start_x", 0)
        start_y = data.get("image_settings", {}).get("start_y", 0)
        self.reset_tab_general(diagramm_type_id, width, height, start_x, start_y)
        #
        nodes = data.get("nodes", [])
        connections = data.get("connections", [])
        self.reset_tab_elements(nodes, connections)

    def edit_object(self, object, is_node=False):
        self.__current_object = object
        self.__current_is_node = is_node
        #
        self.ui.tabw_right.tabBar().setTabVisible(2, True)
        self.ui.tabw_right.setCurrentIndex(2)
        # self.fill_name_widget_by_object(object, is_node)
        self.create_data_widgets_by_object(object, is_node)
        self.create_metrics_widgets_by_object(object, is_node)

    def wrap_node(self, node):
        self.__obsm.obj_project.wrap_node(node)
        #
        data = self.__obsm.obj_project.get_data()
        self.ui.imagewidget.run(data)
        self.reset_widgets_by_data(data)
        

    def clear_form_layout(self, form_layout):
        while form_layout.count():
            child = form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # def fill_name_widget_by_object(self, object, is_node=False):
    #     text_name = object.get("data", {}).get("название", {}).get("value", "")
    #     self.ui.le_name.setText(text_name)

    def create_data_widgets_by_object(self, object, is_node=False):
        self.__data_widgets = {}
        form_layout = self.ui.fl_data
        self.clear_form_layout(form_layout)
        if is_node:
            config_object_data = self.__obsm.obj_configs.get_config_node_data_by_node(object)
        elif not is_node:
            config_object_data = self.__obsm.obj_configs.get_config_connection_data_by_connection(object)
        for config_parameter_key, config_parameter_data in config_object_data.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            # название параметра data
            label_text = config_parameter_data.get("name", "")
            
            label = QLabel(label_text)
            # значение параметра data
            value = object.get("data", {}).get(config_parameter_key, {}).get("value", "")
            value = value if value else config_parameter_data.get("value", "")
            #
            text_edit = QTextEdit()
            text_edit.setText(str(value))
            text_edit.setFixedHeight(50)
            form_layout.addRow(label, text_edit)
            # в словарь виджетов
            self.__data_widgets[config_parameter_key] = text_edit
        

    def create_metrics_widgets_by_object(self, object, is_node=False):
        #
        flag_global_metrics = False
        flag_local_metrics = False
        #
        self.__metrics_widgets = {}
        form_layout_local = self.ui.fl_local_metrics
        form_layout_global = self.ui.fl_global_metrics
        self.clear_form_layout(form_layout_local)
        self.clear_form_layout(form_layout_global)
        #
        if is_node:
            config_object_metrics = self.__obsm.obj_configs.get_config_node_metrics_by_node(object)
        elif not is_node:
            config_object_metrics = self.__obsm.obj_configs.get_config_connection_metrics_by_connection(
                object
            )
        for config_parameter_key, config_parameter_data in config_object_metrics.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            # название параметра metrics
            label_text = config_parameter_data.get("name", "")
            label = QLabel(label_text)
            
            # значение параметра metrics
            value = (
                object.get("metrics", {}).get(config_parameter_key, {}).get("value", "")
            )
            value = value if value else config_parameter_data.get("value", "")
            # тип виджета
            widget_type = config_parameter_data.get("type", "")
            if widget_type == "bool":
                new_widget = QCheckBox()
                new_widget.setChecked(bool(value))
            else:
                new_widget = QSpinBox()
                new_widget.setRange(0, 99999)
                new_widget.setValue(value)
            #
            if config_parameter_data.get("is_global", False):
                form_layout_global.addRow(label, new_widget)
                flag_global_metrics = True
            else:
                form_layout_local.addRow(label, new_widget)
                flag_local_metrics = True
            # в словарь виджетов
            self.__metrics_widgets[config_parameter_key] = [widget_type, new_widget]
        #
        self.ui.label_local_metrics.setVisible(flag_local_metrics)
        self.ui.label_global_metrics.setVisible(flag_global_metrics)

