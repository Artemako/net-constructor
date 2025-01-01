from PySide6.QtWidgets import (
    QMainWindow,
    QMenu,
    QDialog,
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
    QCheckBox,
)

from PySide6.QtCore import Qt

import package.controllers.style as style
import package.controllers.imagewidget as imagewidget

import package.components.nodeconnectionselectdialog as nodeconnectionselectdialog
import package.components.nodeconnectiondeletedialog as nodeconnectiondeletedialog
import package.components.diagrammtypeselectdialog as diagrammtypeselectdialog

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
        self.__general_image_parameters_widgets = {}
        self.__general_diagramm_parameters_widgets = {}
        #
        self.__editor_object_data_widgets = {}
        self.__editor_object_parameters_widgets = {}
        self.__editor_type_object_parameters_widgets = {}
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
            global_diagramms = self.__obsm.obj_configs.get_config_diagramms()
            dialog = diagrammtypeselectdialog.DiagramTypeSelectDialog(
                global_diagramms, self
            )
            result = dialog.exec()
            if result == QDialog.Accepted:
                diagramm_data = dialog.get_data()
                #
                image_parameters = self.__obsm.obj_configs.get_config_image_parameters()
                #
                self.__obsm.obj_project.create_new_project(
                    diagramm_data, image_parameters, file_name
                )
                #
                project_data = self.__obsm.obj_project.get_data()
                #
                self.ui.imagewidget.run(project_data)
                self.reset_widgets_by_data(project_data)
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

    def get_new_parameters(self, parameters_widgets):
        new_parameters = {}
        for key, pair in parameters_widgets.items():
            widget_type = pair[0]
            widget = pair[1]
            if widget_type == "bool":
                new_parameters[key] = {"value": widget.isChecked()}
            else:
                new_parameters[key] = {"value": widget.value()}
        return new_parameters

    def get_new_data(self, data_widgets):
        new_data = {}
        for key, widget in data_widgets.items():
            new_data[key] = {"value": widget.toPlainText()}
        return new_data

    def save_changes_to_file_nce(self):
        # TODO AttributeError: 'Ui_MainWindow' object has no attribute 'sb_width'
        if self.__obsm.obj_project.is_active():
            #
            diagramm_type_id = str()
            diagramm_name = str()
            new_diagramm_parameters = {}
            new_image_parameters = {}
            #
            new_data = {}
            new_parameters = {}
            #
            diagramm_type_id = self.ui.combox_type.currentIndex()
            diagramm_name = self.ui.combox_type.currentText()
            #
            new_image_parameters = self.get_new_parameters(
                self.__general_image_parameters_widgets
            )
            #
            is_edit = False
            if self.ui.tabw_right.currentIndex() == 2:
                is_edit = True
                new_data = self.get_new_data(self.__editor_object_data_widgets)
                new_parameters = self.get_new_parameters(
                    self.__editor_object_parameters_widgets
                )
            #
            config_nodes = self.__obsm.obj_configs.get_nodes()
            config_connections = self.__obsm.obj_configs.get_connections()
            #
            self.__obsm.obj_project.save_project(
                self.__current_object,
                self.__current_is_node,
                is_edit,
                config_nodes,
                config_connections,
                diagramm_type_id,
                diagramm_name,
                new_image_parameters,
                new_data,
                new_parameters,
            )
            data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(data)
            self.reset_widgets_by_data(data)

    def export_to_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, " ", "", "PNG images (*.png)")
        if file_name:
            print(f"save_image to {file_name}")
            self.ui.imagewidget.save_image(file_name)

    def add_node(self):
        if self.__obsm.obj_project.is_active():
            config_nodes = self.__obsm.obj_configs.get_nodes()
            config_connections = self.__obsm.obj_configs.get_connections()
            dialog = nodeconnectionselectdialog.NodeConnectSelectDialog(
                config_nodes, config_connections, self
            )
            if dialog.exec():
                key_dict_node_and_key_dict_connection = (
                    dialog.get_selected_key_dict_node_and_key_dict_connection()
                )
                self.__obsm.obj_project.add_pair(key_dict_node_and_key_dict_connection)
                #
                data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(data)
                self.reset_widgets_by_data(data)

    def delete_node(self, node):
        if self.__obsm.obj_project.is_active():
            nodes = self.__obsm.obj_project.get_data().get("nodes", [])
            connections = self.__obsm.obj_project.get_data().get("connections", [])
            dialog = nodeconnectiondeletedialog.NodeConnectionDeleteDialog(
                nodes, connections, self
            )
            if dialog.exec():
                selected_data = dialog.get_selected_node_and_connection()
                node = selected_data.get("node")
                connection = selected_data.get("connection")
                self.__obsm.obj_project.delete_pair(node, connection)
                #
                data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(data)
                self.reset_widgets_by_data(data)

    def reset_tab_general(
        self, diagramm_type_id, diagramm_parameters, image_parameters
    ):
        print("reset_tab_general")
        # очистка типа
        self.ui.combox_type.clear()
        # TODO combox_type
        self.ui.combox_type.addItem(
            "Скелетная схема ВОЛП и основные данные цепей кабеля", 0
        )
        self.ui.combox_type.setCurrentIndex(diagramm_type_id)
        # Параметры изображения
        config_image_parameters = self.__obsm.obj_configs.get_config_image_parameters()
        self.create_parameters_widgets(
            self.__general_image_parameters_widgets,
            self.ui.fl_image_parameters,
            config_image_parameters,
            image_parameters,
            "image_parameters",
        )
        # Параметры диаграммы
        config_diagramm_parameters = (
            self.__obsm.obj_configs.get_config_diagramm_parameters_by_type_id(
                diagramm_type_id
            )
        )
        self.create_parameters_widgets(
            self.__general_diagramm_parameters_widgets,
            self.ui.fl_diagramm_parameters,
            config_diagramm_parameters,
            diagramm_parameters,
            "diagramm_parameters",
        )

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
            btn_edit.clicked.connect(
                partial(self.edit_object, node, index + 1, is_node=True)
            )

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
            btn_edit.clicked.connect(
                partial(self.edit_object, connection, index + 1, is_node=False)
            )

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
        diagramm_type_id = data.get("diagramm_type_id", 0)
        diagramm_parameters = data.get("diagramm_parameters", {})
        image_parameters = data.get("image_parameters", {})
        self.reset_tab_general(diagramm_type_id, diagramm_parameters, image_parameters)
        #
        nodes = data.get("nodes", [])
        connections = data.get("connections", [])
        self.reset_tab_elements(nodes, connections)

    def edit_object(self, obj, index, is_node=False):
        self.__current_object = obj
        self.__current_is_node = is_node
        #
        self.ui.tabw_right.tabBar().setTabVisible(2, True)
        self.ui.tabw_right.setCurrentIndex(2)
        #
        self.change_name_tab_editor(index, is_node)
        #
        self.create_editor_data_widgets_by_object(obj, is_node)
        self.create_editor_parameters_widgets_by_object(obj, is_node)

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

    def change_name_tab_editor(self, index, is_node=False):
        text_name = str()
        if is_node:
            text_name = f"Редактирование вершины {index}"
        elif not is_node:
            text_name = f"Редактирование соединения {index}—{index + 1}"
        self.ui.tabw_right.setTabText(2, text_name)

    def create_data_widgets(
        self, dict_widgets, form_layout, config_object_data, object_data, data_name
    ) -> bool:
        dict_widgets = {}
        self.clear_form_layout(form_layout)
        for config_parameter_key, config_parameter_data in config_object_data.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            # название параметра data
            label_text = config_parameter_data.get("name", "")
            label = QLabel(label_text)
            # значение параметра data
            value = (
                object_data.get(data_name, {})
                .get(config_parameter_key, {})
                .get("value", "")
            )
            value = value if value else config_parameter_data.get("value", "")
            #
            text_edit = QTextEdit()
            text_edit.setText(str(value))
            text_edit.setFixedHeight(50)
            form_layout.addRow(label, text_edit)
            # в словарь виджетов
            dict_widgets[config_parameter_key] = text_edit
        return len(dict_widgets) > 0

    def create_parameters_widgets(
        self,
        dict_widgets,
        form_layout,
        config_object_parameters,
        object_data,
        parameters_name,
        is_global=None,
    ) -> bool:
        # TODO Local и global параметры
        dict_widgets = {}
        self.clear_form_layout(form_layout)
        for (
            config_parameter_key,
            config_parameter_data,
        ) in config_object_parameters.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            # название параметра parameters
            label_text = config_parameter_data.get("name", "")
            label = QLabel(label_text)
            # значение параметра parameters
            value = (
                object_data.get(parameters_name, {})
                .get(config_parameter_key, {})
                .get("value", "")
            )
            value = value if value else config_parameter_data.get("value", "")
            #
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
            if (
                is_global is None
                or is_global
                and config_parameter_data.get("is_global", True)
                or not is_global
                and config_parameter_data.get("is_global", False)
            ):
                form_layout.addRow(label, new_widget)
                dict_widgets[config_parameter_key] = [widget_type, new_widget]
        return len(dict_widgets) > 0

    def create_editor_parameters_widgets_by_object(self, obj, is_node=False):
        if is_node:
            config_object_parameters = (
                self.__obsm.obj_configs.get_config_node_parameters_by_node(obj)
            )
        elif not is_node:
            config_object_parameters = (
                self.__obsm.obj_configs.get_config_connection_parameters_by_connection(
                    obj
                )
            )
        flag = self.create_parameters_widgets(
            self.__editor_object_parameters_widgets,
            self.ui.fl_object_parameters,
            config_object_parameters,
            obj,
            "parameters",
        )
        self.ui.label_object_parameters.setVisible(flag)
        #
        flag = self.create_parameters_widgets(
            self.__editor_type_object_parameters_widgets,
            self.ui.fl_object_parameters,
            config_object_parameters,
            obj,
            "parameters",
            is_global=True,
        )
        self.ui.label_type_object_parameters.setVisible(flag)

        #
        # flag_type_object_parameters = False
        # flag_object_parameters = False
        # #
        # self.__editor_parameters_widgets = {}
        # form_layout_local = self.ui.fl_object_parameters
        # form_layout_global = self.ui.fl_type_object_parameters
        # self.clear_form_layout(form_layout_local)
        # self.clear_form_layout(form_layout_global)
        # #
        # if is_node:
        #     config_object_parameters = self.__obsm.obj_configs.get_config_node_parameters_by_node(obj)
        # elif not is_node:
        #     config_object_parameters = self.__obsm.obj_configs.get_config_connection_parameters_by_connection(
        #         obj
        #     )
        # for config_parameter_key, config_parameter_data in config_object_parameters.items():
        #     print(
        #         f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
        #     )
        #     # название параметра parameters
        #     label_text = config_parameter_data.get("name", "")
        #     label = QLabel(label_text)

        #     # значение параметра parameters
        #     value = (
        #         obj.get("parameters", {}).get(config_parameter_key, {}).get("value", "")
        #     )
        #     value = value if value else config_parameter_data.get("value", "")
        #     # тип виджета
        #     widget_type = config_parameter_data.get("type", "")
        #     if widget_type == "bool":
        #         new_widget = QCheckBox()
        #         new_widget.setChecked(bool(value))
        #     else:
        #         new_widget = QSpinBox()
        #         new_widget.setRange(0, 99999)
        #         new_widget.setValue(value)
        #     #
        #     if config_parameter_data.get("is_global", False):
        #         form_layout_global.addRow(label, new_widget)
        #         flag_type_object_parameters = True
        #     else:
        #         form_layout_local.addRow(label, new_widget)
        #         flag_object_parameters = True
        #     # в словарь виджетов
        #     self.__editor_parameters_widgets[config_parameter_key] = [widget_type, new_widget]
        #
        # self.ui.label_object_parameters.setVisible(flag_object_parameters)
        # self.ui.label_type_object_parameters.setVisible(flag_type_object_parameters)

    def create_editor_data_widgets_by_object(self, obj, is_node=False):
        if is_node:
            config_object_data = self.__obsm.obj_configs.get_config_node_data_by_node(
                obj
            )
        elif not is_node:
            config_object_data = (
                self.__obsm.obj_configs.get_config_connection_data_by_connection(obj)
            )
        self.create_data_widgets(
            self.__editor_object_data_widgets,
            self.ui.fl_object_data,
            config_object_data,
            obj,
            "data",
        )

        # self.__editor_data_widgets = {}
        # form_layout = self.ui.fl_object_data
        # self.clear_form_layout(form_layout)
        # if is_node:
        #     config_object_data = self.__obsm.obj_configs.get_config_node_data_by_node(obj)
        # elif not is_node:
        #     config_object_data = self.__obsm.obj_configs.get_config_connection_data_by_connection(obj)
        # for config_parameter_key, config_parameter_data in config_object_data.items():

        #     # название параметра data
        #     label_text = config_parameter_data.get("name", "")

        #     label = QLabel(label_text)
        #     # значение параметра data
        #     value = obj.get("data", {}).get(config_parameter_key, {}).get("value", "")
        #     value = value if value else config_parameter_data.get("value", "")
        #     #
        #     text_edit = QTextEdit()
        #     text_edit.setText(str(value))
        #     text_edit.setFixedHeight(50)
        #     form_layout.addRow(label, text_edit)
        #     # в словарь виджетов
        #     self.__editor_data_widgets[config_parameter_key] = text_edit
