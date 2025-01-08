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
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QFontComboBox,
)
from PySide6.QtGui import QIntValidator, QFont
from PySide6.QtCore import Qt, QModelIndex

import package.controllers.style as style
import package.controllers.imagewidget as imagewidget

import package.components.nodeconnectionselectdialog as nodeconnectionselectdialog
import package.components.nodeconnectiondeletedialog as nodeconnectiondeletedialog
import package.components.diagrammtypeselectdialog as diagrammtypeselectdialog
import package.components.changeorderdialog as changeorderdialog
import package.components.confirmchangingdiagrammtypedialog as confirmchangingdiagrammtypedialog

import package.ui.mainwindow_ui as mainwindow_ui

import package.constants as constants

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
        self.__editor_type_object_data_widgets = {}
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

    def _tab_right_changed(self, index):
        if index in [0, 1]:
            self.ui.tabw_right.tabBar().setTabVisible(2, False)

    def config(self):
        # СТИЛЬ
        obj_style = style.Style()
        obj_style.set_style_for(self)
        #
        self.resize(1280, 768)
        self.ui.centralwidget_splitter.setSizes([806, 560])
        #
        self.ui.tabw_right.tabBar().setTabVisible(2, False)
        self.ui.tabw_right.currentChanged.connect(self._tab_right_changed)

        # self.update_menu_recent_projects()
        #
        self.ui.btn_addnode.clicked.connect(self._add_node)
        self.ui.btn_movenodes.clicked.connect(self._move_nodes)
        self.ui.btn_deletenode.clicked.connect(self._delete_node)
        #
        self.ui.btn_moveconnections.clicked.connect(self._move_connections)
        #
        self.ui.combox_type_diagramm.currentIndexChanged.connect(
            self._change_type_diagramm
        )
        #
        # создание нового файла
        self.ui.action_new.triggered.connect(self.create_file_nce)
        # октрытие файла
        self.ui.action_open.triggered.connect(self.open_file_nce)
        # сохранение текущих данных
        self.ui.action_save.triggered.connect(self._save_changes_to_file_nce)
        # экспорт в картинку
        self.ui.action_export_to_image.triggered.connect(self._export_to_image)
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
                self._reset_widgets_by_data(project_data)
                self.start_qt_actions()

    def open_file_nce(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, " ", "", "NCE (пока json) files (*.json)"
        )
        if file_name:
            self.__obsm.obj_project.open_project(file_name)
            #
            project_data = self.__obsm.obj_project.get_data()
            #
            self.ui.imagewidget.run(project_data)
            self._reset_widgets_by_data(project_data)
            self.start_qt_actions()

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
            elif widget_type == "line_string":
                new_data_or_parameters[key] = {"value": widget.text()}
            elif widget_type == "fill_style":
                new_data_or_parameters[key] = {"value": widget.currentText()}
            elif widget_type == "bool":
                new_data_or_parameters[key] = {"value": widget.isChecked()}
            elif widget_type == "number_int_signed":
                new_data_or_parameters[key] = {"value": widget.value()}
            elif widget_type == "number_int":
                new_data_or_parameters[key] = {"value": widget.value()}
            else:
                if is_parameters:
                    new_data_or_parameters[key] = {"value": widget.value()}
                else:
                    new_data_or_parameters[key] = {"value": widget.toPlainText()}

        return new_data_or_parameters

    def _save_changes_to_file_nce(self):
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
            is_general_tab = False
            is_editor_tab = False
            if self.ui.tabw_right.currentIndex() == 0:
                is_general_tab = True
                diagramm_type_id = self.ui.combox_type_diagramm.currentData().get(
                    "type_id", ""
                )
                diagramm_name = self.ui.combox_type_diagramm.currentData().get(
                    "name", ""
                )
                new_image_parameters = self._get_new_data_or_parameters(
                    self.__general_image_parameters_widgets, is_parameters=True
                )
                new_diagramm_parameters = self._get_new_data_or_parameters(
                    self.__general_diagramm_parameters_widgets, is_parameters=True
                )
            elif self.ui.tabw_right.currentIndex() == 2:
                is_editor_tab = True
                # Объединить дата с двух разных форм
                new_data = self._get_new_data_or_parameters(
                    self.__editor_object_data_widgets, is_parameters=False
                )
                new_type_parameters = self._get_new_data_or_parameters(
                    self.__editor_type_object_data_widgets, is_parameters=False
                )
                new_data.update(new_type_parameters)
                # Объединить параметры с двух разных форм
                new_parameters = self._get_new_data_or_parameters(
                    self.__editor_object_parameters_widgets, is_parameters=True
                )
                new_type_parameters = self._get_new_data_or_parameters(
                    self.__editor_type_object_parameters_widgets, is_parameters=True
                )
                new_parameters.update(new_type_parameters)
            #
            if is_editor_tab or is_general_tab:
                config_nodes = self.__obsm.obj_configs.get_nodes()
                config_connections = self.__obsm.obj_configs.get_connections()
                #
                self.__obsm.obj_project.save_project(
                    self.__current_object,
                    self.__current_is_node,
                    is_general_tab,
                    is_editor_tab,
                    config_nodes,
                    config_connections,
                    diagramm_type_id,
                    diagramm_name,
                    new_image_parameters,
                    new_diagramm_parameters,
                    new_data,
                    new_parameters,
                )
            #
            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_widgets_by_data(project_data)

    def _export_to_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, " ", "", "PNG images (*.png)")
        if file_name:
            print(f"save_image to {file_name}")
            self.ui.imagewidget.save_image(file_name)

    def _add_node(self):
        if self.__obsm.obj_project.is_active():
            # TODO в зависимости от выбранной диаграммы
            diagramm_type_id = self.__obsm.obj_project.get_data().get(
                "diagramm_type_id", ""
            )
            #
            config_diagramm_nodes = (
                self.__obsm.obj_configs.get_config_diagramm_nodes_by_type_id(
                    diagramm_type_id
                )
            )
            config_diagramm_connections = (
                self.__obsm.obj_configs.get_config_diagramm_connections_by_type_id(
                    diagramm_type_id
                )
            )
            #
            dialog = nodeconnectionselectdialog.NodeConnectSelectDialog(
                config_diagramm_nodes, config_diagramm_connections, self
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

    def _delete_node(self, node):
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
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

    def _reset_combobox_type_diagramm(self, diagramm_type_id):
        print("reset_combobox_type_diagramm():\n")
        print(f"diagramm_type_id={diagramm_type_id}\n")
        combox_widget = self.ui.combox_type_diagramm
        combox_widget.blockSignals(True)
        combox_widget.clear()
        #
        index = 0
        global_diagramms = self.__obsm.obj_configs.get_config_diagramms()
        for key, elem in global_diagramms.items():
            print(f"key={key}, elem={elem}")
            name = elem.get("name", "")
            type_id = elem.get("type_id", "0")
            combox_widget.addItem(name, elem)
            if type_id == diagramm_type_id:
                combox_widget.setCurrentIndex(index)
            index += 1
        combox_widget.blockSignals(False)
        #

    def _change_type_diagramm(self, index):
        new_diagramm = self.ui.combox_type_diagramm.currentData()
        new_type_id = new_diagramm.get("type_id", "0")
        current_type_id = self.__obsm.obj_project.get_data().get(
            "diagramm_type_id", None
        )
        # диалоговое окно с выбором диаграммы
        if self.__obsm.obj_project.is_active() and new_type_id != current_type_id:
            dialog = confirmchangingdiagrammtypedialog.ConfirmChangingDiagrammType(
                new_diagramm, self
            )
            if dialog.exec():
                self.__obsm.obj_project.change_type_diagramm(new_diagramm)
                #
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

    def reset_tab_general(
        self, diagramm_type_id, diagramm_parameters, image_parameters
    ):
        print("reset_tab_general")
        # очистка типа диаграммы
        self._reset_combobox_type_diagramm(diagramm_type_id)
        # Параметры изображения
        config_image_parameters = self.__obsm.obj_configs.get_config_image_parameters()
        self._create_parameters_widgets(
            self.__general_image_parameters_widgets,
            self.ui.fl_image_parameters,
            config_image_parameters,
            image_parameters,
        )
        # Параметры диаграммы
        config_diagramm_parameters = (
            self.__obsm.obj_configs.get_config_diagramm_parameters_by_type_id(
                diagramm_type_id
            )
        )
        self._create_parameters_widgets(
            self.__general_diagramm_parameters_widgets,
            self.ui.fl_diagramm_parameters,
            config_diagramm_parameters,
            diagramm_parameters,
        )

    def reset_tab_elements(self, nodes, connections):
        nodes = sorted(nodes, key=lambda node: node.get("order", 0))
        connections = sorted(
            connections, key=lambda connection: connection.get("order", 0)
        )
        self._reset_table_nodes(nodes)
        self._reset_table_connections(connections)

    def _reset_table_nodes(self, nodes):
        print("reset_table_nodes")
        self.__nodes_data = nodes
        table_widget = self.ui.tablew_nodes
        table_widget.blockSignals(True)
        table_widget.clearContents()
        table_widget.setRowCount(len(nodes))
        headers = ["Название", "Перенос", "Редактировать"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        #
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
            btn_wrap.clicked.connect(partial(self._wrap_node, node))
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

    def _reset_table_connections(self, connections):
        print("reset_table_connections")
        self.__connections_data = connections
        table_widget = self.ui.tablew_connections
        table_widget.blockSignals(True)
        table_widget.clearContents()
        table_widget.setRowCount(len(connections))
        headers = ["Название", "Редактировать"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        #
        row_headers = []
        for index, connection in enumerate(connections):
            connection_name = (
                connection.get("data", {}).get("название", {}).get("value", "")
            )
            print("CONNECTION_NAME:", connection_name)
            item = QTableWidgetItem(connection_name)
            table_widget.setItem(index, 0, item)
            #
            connection_text = f"{index + 1}—{index + 2}"
            row_headers.append(connection_text)
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 1, btn_edit)
            btn_edit.clicked.connect(
                partial(self.edit_object, connection, index + 1, is_node=False)
            )
        # Устанавливаем заголовки строк
        table_widget.setVerticalHeaderLabels(row_headers)
        # Настраиваем режимы изменения размера для заголовков
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.blockSignals(False)

    def _reset_widgets_by_data(self, data):
        #
        diagramm_type_id = data.get("diagramm_type_id", "")
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
        self._change_name_tab_editor(index, is_node)
        #
        self._create_editor_data_widgets_by_object(obj, is_node)
        self._create_editor_parameters_widgets_by_object(obj, is_node)

    def _wrap_node(self, node):
        self.__obsm.obj_project.wrap_node(node)
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
            text_name = f"Редактирование соединения {index}—{index + 1}"
        self.ui.tabw_right.setTabText(2, text_name)

    def create_data_widgets(
        self, dict_widgets, form_layout, config_object_data, object_data
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
        for config_parameter_key, config_parameter_data in config_object_data.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            widget_type = config_parameter_data.get("type", "")
            label_text = config_parameter_data.get("name", "")
            # названия параметра data
            label = self._get_label_name(label_text, widget_type)
            # значение параметра data
            value = object_data.get(config_parameter_key, {}).get("value", None)
            value = (
                value if value is not None else config_parameter_data.get("value", "")
            )
            #
            # тип виджета
            new_widget = self._get_widget(widget_type, value, is_parameters=False)
            #
            form_layout.addRow(label, new_widget)
            # в словарь виджетов
            dict_widgets[config_parameter_key] = [widget_type, new_widget]

        print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _get_widget(self, widget_type, value, is_parameters=True):
        if widget_type == "title":
            new_widget = QLabel()
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
        elif widget_type == "line_string":
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
        elif widget_type == "number_int_signed":
            new_widget = QSpinBox()
            new_widget.setRange(-2147483647, 2147483647)
            new_widget.setValue(value)
        #
        elif widget_type == "number_int":
            new_widget = QSpinBox()
            new_widget.setRange(0, 2147483647)
            new_widget.setValue(value)
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
        #
        return new_widget

    def _get_label_name(self, label_text, widget_type):
        label = QLabel(label_text)
        if widget_type == "title":
            label.setStyleSheet("font-style: italic; font-weight: bold; ")
        return label

    def _create_parameters_widgets(
        self, dict_widgets, form_layout, config_object_parameters, object_parameters
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
        for (
            config_parameter_key,
            config_parameter_data,
        ) in config_object_parameters.items():
            print(
                f"config_parameter_key: {config_parameter_key}, config_parameter_data: {config_parameter_data}"
            )
            #
            widget_type = config_parameter_data.get("type", "")
            label_text = config_parameter_data.get("name", "")
            # название параметра parameters
            label = self._get_label_name(label_text, widget_type)
            # значение параметра parameters
            if widget_type == "font_name":
                print("font_name BEFORE")
            value = object_parameters.get(config_parameter_key, {}).get("value", None)
            print("value", value)
            value = (
                value if value is not None else config_parameter_data.get("value", "")
            )
            print("new_value", value)
            #
            # тип виджета
            new_widget = self._get_widget(widget_type, value, is_parameters=True)
            #
            form_layout.addRow(label, new_widget)
            if widget_type != "title":
                dict_widgets[config_parameter_key] = [widget_type, new_widget]
        print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _create_editor_parameters_widgets_by_object(self, obj, is_node=False):
        if is_node:
            config_object_parameters = (
                self.__obsm.obj_configs.get_config_node_parameters_by_node(obj)
            )
            config_type_object_parameters = (
                self.__obsm.obj_configs.get_config_type_node_parameters_by_node(obj)
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
        # именно только parameters
        object_parameters = obj.get("parameters", {})
        flag = self._create_parameters_widgets(
            self.__editor_object_parameters_widgets,
            self.ui.fl_object_parameters,
            config_object_parameters,
            object_parameters,
        )
        self.ui.label_object_parameters.setVisible(flag)
        #
        flag = self._create_parameters_widgets(
            self.__editor_type_object_parameters_widgets,
            self.ui.fl_type_object_parameters,
            config_type_object_parameters,
            object_parameters,
        )
        self.ui.label_type_object_parameters.setVisible(flag)

    def _create_editor_data_widgets_by_object(self, obj, is_node=False):
        if is_node:
            config_object_data = self.__obsm.obj_configs.get_config_node_data_by_node(
                obj
            )
            config_type_object_data = (
                self.__obsm.obj_configs.get_config_type_node_data_by_node(obj)
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
        # именно только data
        object_data = obj.get("data", {})
        flag = self.create_data_widgets(
            self.__editor_object_data_widgets,
            self.ui.fl_object_data,
            config_object_data,
            object_data,
        )
        self.ui.label_object_data.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_type_object_data_widgets,
            self.ui.fl_type_object_data,
            config_type_object_data,
            object_data,
        )
        self.ui.label_type_object_data.setVisible(flag)
