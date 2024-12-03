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
    QSizePolicy
)

import package.controllers.style as style
import package.controllers.imagewidget as imagewidget

import package.components.nodeconnectionselectdialog as nodeconnectionselectdialog

import package.ui.mainwindow_ui as mainwindow_ui

import json
from functools import partial


class MainWindow(QMainWindow):
    def __init__(self, obsm):
        self.__obsm = obsm
        super(MainWindow, self).__init__()
        self.ui = mainwindow_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        #
        self.ui.imagewidget.set_obsm(self.__obsm)
        # config
        self.config()

    def config(self):
        # СТИЛЬ
        obj_style = style.Style()
        obj_style.set_style_for(self)
        #
        self.ui.centralwidget_splitter.setSizes([806, 560])
        # self.update_menu_recent_projects()
        #
        self.ui.btn_addnode.clicked.connect(self.add_node)
        # создание нового файла
        self.ui.action_new.triggered.connect(self.create_file_nce)
        # октрытие файла
        self.ui.action_open.triggered.connect(self.open_file_nce)
        # сохранение текущих данных
        self.ui.action_save.triggered.connect(self.save_file_nce)
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

    def save_file_nce(self):
        # TODO Получить data из виджетов
        self.__obsm.obj_project.save_project()

    def export_to_image(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, " ", "", "PNG images (*.png)"
        )
        if file_name:
            self.ui.imagewidget.save_image()


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



    def reset_tab_general(self, diagramm_type_id, width, height):
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

    def reset_tab_elements(self, nodes, connections):
        nodes = sorted(nodes, key=lambda node: node.get("order", 0))
        connections = sorted(
            connections, key=lambda connection: connection.get("order", 0)
        )
        self.reset_table_nodes(nodes)
        self.reset_table_connections(connections)

    def reset_table_nodes(self, nodes):
        table_widget = self.ui.tablew_nodes
        table_widget.clearContents()
        table_widget.setRowCount(len(nodes))
        headers = ["Название", "Перенос?", "Редактировать", "Удалить"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        print("NODES", nodes)
        for index, node in enumerate(nodes):
            print("NODE", node)
            node_name = node.get("data", {}).get("название", {}).get("value", "")
            table_widget.setItem(index, 0, QTableWidgetItem(node_name))
            #
            is_wrap = node.get("is_wrap", False)
            value_wrap = "ДА" if is_wrap else "НЕТ"
            table_widget.setItem(index, 1, QTableWidgetItem(value_wrap))
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 2, btn_edit)
            btn_edit.clicked.connect(partial(self.edit_node, node))
            #
            btn_delete = QPushButton("Удалить") 
            table_widget.setCellWidget(index, 3, btn_delete)
            # TODO self.__obsm.obj_project.delete_node
            btn_delete.clicked.connect(partial(self.delete_node, node))

        # Настраиваем режимы изменения размера для заголовков
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

    def reset_table_connections(self, connections):
        print("reset_table_connections")
        table_widget = self.ui.tablew_connections
        table_widget.clearContents()
        table_widget.setRowCount(len(connections))
        headers = ["Название", "Редактировать", "Удалить"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        for index, connection in enumerate(connections):
            connection_name = (
                connection.get("data", {}).get("название", {}).get("value", "")
            )
            table_widget.setItem(index, 0, QTableWidgetItem(connection_name))
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 1, btn_edit)
            btn_edit.clicked.connect(partial(self.edit_connection, connection))
            #
            btn_delete = QPushButton("Удалить")
            table_widget.setCellWidget(index, 2, btn_delete)
            btn_delete.clicked.connect(partial(self.delete_connection, connection))
            # TODO delete_connection
        # Настраиваем режимы изменения размера для заголовков
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

    def reset_widgets_by_data(self, data):
        #
        diagramm_type_id = data.get("diagramm_settings", {}).get("diagramm_type_id", 0)
        width = data.get("image_settings", {}).get("width", 0)
        height = data.get("image_settings", {}).get("height", 0)
        self.reset_tab_general(diagramm_type_id, width, height)
        #
        nodes = data.get("nodes", [])
        connections = data.get("connections", [])
        self.reset_tab_elements(nodes, connections)

    def edit_node(self, node):
        print("edit_node", node)
        # TODO
        self.ui.tabw_right.setCurrentIndex(2)
        self.create_data_widgets_by_object(node, is_node=True)
        self.create_metrics_widgets_by_object(node, is_node=True)

    def edit_connection(self, connection):
        print("edit_connection", connection)
        self.ui.tabw_right.setCurrentIndex(2)
        self.create_data_widgets_by_object(connection, is_node=False)
        self.create_metrics_widgets_by_object(connection, is_node=False)

    def delete_node(self, node):
        print("delete_node", node)
        # TODO

    def delete_connection(self, connection):
        print("delete_connection", connection)
        # TODO

    def clear_form_layout(self, form_layout):
        while form_layout.count():
            child = form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_data_widgets_by_object(self, object, is_node=False):
        form_layout = self.ui.fl_data
        self.clear_form_layout(form_layout)
        # TODO
        if is_node:
            config_object_data = self.__obsm.obj_configs.get_config_node_data_by_node(object)
        elif not is_node:
            config_object_data = self.__obsm.obj_configs.get_config_connection_data_by_connection(object)
        for config_parameter_key, config_parameter_data in config_object_data.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            # название параметра data
            label_text = config_parameter_data.get("value", "")
            label = QLabel(label_text)
            # значение параметра data
            value = object.get("data", {}).get(config_parameter_key, {}).get("value", "")
            value = value if value else config_parameter_data.get("value", "")
            #
            text_edit = QTextEdit()
            text_edit.setText(str(value))
            text_edit.setFixedHeight(50)
            form_layout.addRow(label, text_edit)

    def create_metrics_widgets_by_object(self, object, is_node=False):
        form_layout = self.ui.fl_metrics
        self.clear_form_layout(form_layout)
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
            #
            spin_box = QSpinBox()
            spin_box.setRange(0, 99999)
            spin_box.setValue(value)
            form_layout.addRow(label, spin_box)

