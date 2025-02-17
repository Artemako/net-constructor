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
)
from PySide6.QtGui import QIntValidator, QFont
from PySide6.QtCore import Qt, QModelIndex, QLocale

import package.controllers.style as style
import package.controllers.imagewidget as imagewidget

import package.components.nodeconnectionselectdialog as nodeconnectionselectdialog
import package.components.nodeconnectiondeletedialog as nodeconnectiondeletedialog
import package.components.diagramtypeselectdialog as diagramtypeselectdialog
import package.components.changeorderdialog as changeorderdialog
import package.components.confirmchangingdiagramtypedialog as confirmchangingdiagramtypedialog
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
        self.__general_image_parameters_widgets = {}
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
        if index in [0, 1]:
            self.ui.tabw_right.tabBar().setTabVisible(2, False)
        elif index == 2:
            self.ui.tabw_right.tabBar().setTabVisible(3, False)

    def config(self):
        # СТИЛЬ
        obj_style = style.Style()
        obj_style.set_style_for(self)
        #
        self.resize(1280, 768)
        self.ui.centralwidget_splitter.setSizes([806, 560])
        #
        self.ui.tabw_right.tabBar().setTabVisible(2, False)
        self.ui.tabw_right.tabBar().setTabVisible(3, False)
        self.ui.tabw_right.currentChanged.connect(self._tab_right_changed)

        # self.update_menu_recent_projects()
        #
        self.ui.btn_addnode.clicked.connect(self._add_node)
        self.ui.btn_movenodes.clicked.connect(self._move_nodes)
        self.ui.btn_deletenode.clicked.connect(self._delete_node)
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
        #

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
                image_parameters = self.__obsm.obj_configs.get_config_image_parameters()
                control_sectors_config = (
                    self.__obsm.obj_configs.get_config_control_sectors()
                )
                #
                self.__obsm.obj_project.create_new_project(
                    diagram_data, image_parameters, control_sectors_config, file_name
                )
                #
                project_data = self.__obsm.obj_project.get_data()
                #
                self.ui.imagewidget.run(project_data)
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
            self.ui.imagewidget.run(project_data)
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
            new_image_parameters = {}

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
                new_image_parameters = self._get_new_data_or_parameters(
                    self.__general_image_parameters_widgets, is_parameters=True
                )
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
                # TODO проверка
                # Получаем новые значения из виджетов
                new_control_sector_parameters = self._get_new_data_or_parameters(
                    self.__control_data_parameters_widgets, is_parameters=True
                )
                # Обновляем данные контрольного сектора
                if self.__current_control_sector is not None:
                    for key, value in new_control_sector_parameters.items():
                        self.__current_control_sector["data_pars"][key]["value"] = value.get(
                            "value"
                        )
                # сохранение параметров контрольного сектора
                # new_cs_name = self.cs_name_edit.text()
                # new_cs_physical_length = self.cs_physical_length_edit.value()
                # new_cs_length = self.cs_length_edit.value()
                # new_cs_delta_wrap_x_edit = self.cs_delta_wrap_x_edit.value()
                # self.__current_control_sector["cs_name"] = new_cs_name
                # self.__current_control_sector["cs_lenght"] = new_cs_length
                # self.__current_control_sector["cs_physical_length"] = (
                #     new_cs_physical_length
                # )
                # self.__current_control_sector["cs_delta_wrap_x"] = (
                #     new_cs_delta_wrap_x_edit
                # )

                # self.__current_control_sector["data_pars"][...]["value"] = ...

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
                    new_image_parameters,
                    new_diagram_parameters,
                    new_data,
                    new_parameters,
                )

            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_widgets_by_data(project_data)

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
        # диалоговое окно с выбором диаграммы
        if self.__obsm.obj_project.is_active() and new_type_id != current_type_id:
            dialog = confirmchangingdiagramtypedialog.ConfirmChangingDiagramType(
                new_diagram, self
            )
            if dialog.exec():
                config_nodes = self.__obsm.obj_configs.get_nodes()
                config_connections = self.__obsm.obj_configs.get_connections()
                self.__obsm.obj_project.change_type_diagram(
                    new_diagram, config_nodes, config_connections
                )
                #
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

    def reset_tab_general(
        self, diagram_type_id, diagram_parameters, image_parameters, precision_separator
    ):
        print("reset_tab_general")
        # очистка типа диаграммы
        self._reset_combobox_type_diagram(diagram_type_id)
        # Параметры изображения
        config_image_parameters = self.__obsm.obj_configs.get_config_image_parameters()
        self._create_parameters_widgets(
            self.__general_image_parameters_widgets,
            self.ui.fl_image_parameters,
            config_image_parameters,
            image_parameters,
            precision_separator,
        )
        # Параметры диаграммы
        config_diagram_parameters = (
            self.__obsm.obj_configs.get_config_diagram_parameters_by_type_id(
                diagram_type_id
            )
        )
        self._create_parameters_widgets(
            self.__general_diagram_parameters_widgets,
            self.ui.fl_diagram_parameters,
            config_diagram_parameters,
            diagram_parameters,
            precision_separator,
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
        table_widget = self.ui.tablew_nodes
        table_widget.blockSignals(True)
        table_widget.clearContents()
        table_widget.setRowCount(len(nodes))
        #
        headers = ["№", "Название", "Перенос", "Редактировать"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.verticalHeader().setVisible(False)
        #
        print("NODES", nodes)
        for index, node in enumerate(nodes):
            print("NODE", node)
            #
            item_number = QTableWidgetItem(str(index + 1))
            table_widget.setItem(index, 0, item_number)
            #
            node_name = node.get("data", {}).get("название", {}).get("value", "")
            item = QTableWidgetItem(node_name)
            table_widget.setItem(index, 1, item)
            #
            is_wrap = node.get("is_wrap", False)
            btn_wrap = QPushButton("Не переносить" if is_wrap else "Переносить")
            table_widget.setCellWidget(index, 2, btn_wrap)
            btn_wrap.clicked.connect(partial(self._wrap_node, node))
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 3, btn_edit)
            btn_edit.clicked.connect(
                partial(self._edit_object, node, index + 1, is_node=True)
            )
        #
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        #
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.blockSignals(False)

    def _reset_table_connections(self, connections):
        print("reset_table_connections")
        table_widget = self.ui.tablew_connections
        table_widget.blockSignals(True)
        table_widget.clearContents()
        table_widget.setRowCount(len(connections))
        #
        headers = ["№", "Название", "Редактировать"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.verticalHeader().setVisible(False)
        #
        for index, connection in enumerate(connections):
            connection_name = (
                connection.get("data", {}).get("название", {}).get("value", "")
            )
            print("CONNECTION_NAME:", connection_name)
            #
            item_number = QTableWidgetItem(f"{index + 1}—{index + 2}")
            table_widget.setItem(index, 0, item_number)
            #
            item = QTableWidgetItem(connection_name)
            table_widget.setItem(index, 1, item)
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 2, btn_edit)
            btn_edit.clicked.connect(
                partial(self._edit_object, connection, index + 1, is_node=False)
            )
        #
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.blockSignals(False)

    def _check_control_sectors_length(self, control_sectors):
        """Проверка суммы физических длин секторов"""
        total_physical_length = sum(
            cs.get("cs_physical_length", 0) for cs in control_sectors
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

        if abs(total_physical_length - connection_physical_length) <= 0.001:
            return 0, total_physical_length, connection_physical_length
        elif total_physical_length > connection_physical_length:
            return 1, total_physical_length, connection_physical_length
        else:
            return -1, total_physical_length, connection_physical_length

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
        print("reset_table_control_sectors")
        table_widget = self.ui.tw_control_sectors
        table_widget.blockSignals(True)
        table_widget.clearContents()
        table_widget.setRowCount(len(control_sectors))
        #
        comparison_result, total_length, connection_length = (
            self._check_control_sectors_length(control_sectors)
        )
        #
        headers = ["№", "Название", "Физ. длина", "Перенос после", "Редактировать"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        # обновляем заголовок физической длины
        self._update_physical_length_header(table_widget, comparison_result)
        #
        table_widget.verticalHeader().setVisible(False)
        #
        for index, cs in enumerate(control_sectors):
            item_number = QTableWidgetItem(str(index + 1))
            table_widget.setItem(index, 0, item_number)
            #
            cs_name = cs.get("data_pars", {}).get("cs_name", {}).get("value", "")
            item = QTableWidgetItem(cs_name)
            table_widget.setItem(index, 1, item)
            #
            physical_length = cs.get("data_pars", {}).get("cs_physical_length", {}).get("value", 0)
            item_length = QTableWidgetItem(str(physical_length))
            table_widget.setItem(index, 2, item_length)
            # в последней строке кнопки переноса нет
            if index < len(control_sectors) - 1:
                is_wrap = cs.get("is_wrap", False)
                btn_wrap = QPushButton("Не переносить" if is_wrap else "Переносить")
                table_widget.setCellWidget(index, 3, btn_wrap)
                btn_wrap.clicked.connect(
                    partial(self._wrap_control_sector, cs)
                )
            else:
                empty_item = QTableWidgetItem("")
                empty_item.setFlags(empty_item.flags() & ~Qt.ItemIsEditable)
                table_widget.setItem(index, 3, empty_item)
            #
            btn_edit = QPushButton("Редактировать")
            table_widget.setCellWidget(index, 4, btn_edit)
            btn_edit.clicked.connect(partial(self._edit_control_sector, cs))

        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.blockSignals(False)

    def _reset_widgets_by_data(self, data):
        #
        diagram_type_id = data.get("diagram_type_id", "")
        diagram_parameters = data.get("diagram_parameters", {})
        image_parameters = data.get("image_parameters", {})
        # Сепаратор для виджета
        precision_separator = diagram_parameters.get("precision_separator", True)
        #
        self.reset_tab_general(
            diagram_type_id, diagram_parameters, image_parameters, precision_separator
        )
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
        # получаем precision_separator из параметров диаграммы
        precision_separator = (
            self.__obsm.obj_project.get_data()
            .get("diagram_parameters", {})
            .get("precision_separator", True)
        )
        #
        self.__control_data_parameters_widgets = {}
        # TODO Получить именно через config
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
        )

        # название
        # label_name = QLabel("Название контрольного сектора")
        # self.cs_name_edit = self._get_widget(
        #     "line_string", cs.get("cs_name", ""), is_parameters=False
        # )
        # self.ui.fl_control.addRow(label_name, self.cs_name_edit)
        # # физическая длина сектора
        # label_physical_length = QLabel("Физическая длина сектора")
        # self.cs_physical_length_edit = self._get_widget(
        #     "number_float",
        #     float(cs.get("cs_physical_length", 0)),
        #     is_parameters=True,
        #     precision_separator=precision_separator,
        # )
        # self.ui.fl_control.addRow(label_physical_length, self.cs_physical_length_edit)
        # # длина
        # label_length = QLabel("Длина сектора")
        # self.cs_length_edit = self._get_widget(
        #     "number_int", int(cs.get("cs_lenght", 0)), is_parameters=True
        # )
        # self.ui.fl_control.addRow(label_length, self.cs_length_edit)
        # # перенос после
        # label_wrap = QLabel("Расстояние переноса по X после сектора")
        # self.cs_delta_wrap_x_edit = self._get_widget(
        #     "number_int", int(cs.get("cs_delta_wrap_x", 0)), is_parameters=True
        # )
        # self.ui.fl_control.addRow(label_wrap, self.cs_delta_wrap_x_edit)

    def _wrap_node(self, node):
        self.__obsm.obj_project.wrap_node(node)
        #
        project_data = self.__obsm.obj_project.get_data()
        self.ui.imagewidget.run(project_data)
        self._reset_widgets_by_data(project_data)

    def _wrap_control_sector(self, control_sector):
        control_sector["is_wrap"] = not control_sector.get("is_wrap", False)
        self._reset_table_control_sectors(
            self.__current_object.get("control_sectors", [])
        )

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

    def _get_widget(
        self, widget_type, value, is_parameters=True, precision_separator=None
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
            new_widget.setRange(-2147483647, 2147483647)
            new_widget.setValue(value)
        #
        elif widget_type == "number_int":
            new_widget = QSpinBox()
            new_widget.setRange(0, 2147483647)
            new_widget.setValue(value)
        #
        elif widget_type == "number_float":
            new_widget = QDoubleSpinBox()
            new_widget.setRange(0, 2147483647)
            new_widget.setValue(value)
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
        #
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
            new_widget = self._get_widget(
                widget_type,
                value,
                is_parameters=True,
                precision_separator=precision_separator,
            )
            #
            form_layout.addRow(label, new_widget)
            if widget_type != "title":
                dict_widgets[config_parameter_key] = [widget_type, new_widget]
        print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _add_control_sector(self, obj):
        control_sectors = self.__obsm.obj_project.add_control_sector(obj)
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

    def _delete_control_sector(self, obj):
        old_control_sectors = obj.get("control_sectors", [])
        # Создаем диалоговое окно для выбора контрольной точки
        dialog = controlsectordeletedialog.ControlSectorDeleteDialog(
            old_control_sectors, self
        )
        if dialog.exec():
            selected_cs = dialog.get_selected_control_sector()
            control_sectors = self.__obsm.obj_project.delete_control_sector(
                obj, selected_cs
            )
            #
            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_table_control_sectors(control_sectors)

    def _create_editor_control_sectors_by_object(self, obj, is_node=False):
        self.ui.label_control_sectors.setVisible(not is_node)
        self.ui.tw_control_sectors.setVisible(not is_node)
        self.ui.btn_add_control_sector.setVisible(not is_node)
        self.ui.btn_delete_control_sector.setVisible(not is_node)
        self.ui.btn_move_control_sectors.setVisible(not is_node)
        # отключаем старые обработчики
        try:
            self.ui.btn_add_control_sector.clicked.disconnect()
            self.ui.btn_move_control_sectors.clicked.disconnect()
            self.ui.btn_delete_control_sector.clicked.disconnect()
        except:
            pass
        #
        self.ui.btn_add_control_sector.clicked.connect(
            partial(self._add_control_sector, obj)
        )
        self.ui.btn_move_control_sectors.clicked.connect(
            partial(self._move_control_sectors, obj)
        )
        self.ui.btn_delete_control_sector.clicked.connect(
            partial(self._delete_control_sector, obj)
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
        #
        flag = self._create_parameters_widgets(
            self.__editor_objects_parameters_widgets,
            self.ui.fl_objects_parameters,
            config_objects_parameters,
            object_parameters,
        )
        self.ui.label_objects_parameters.setVisible(flag)

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
        #
        flag = self.create_data_widgets(
            self.__editor_type_object_data_widgets,
            self.ui.fl_type_object_data,
            config_type_object_data,
            object_data,
        )
        self.ui.label_type_object_data.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_objects_data_widgets,
            self.ui.fl_objects_data,
            config_objects_data,
            object_data,
        )
        self.ui.label_objects_data.setVisible(flag)
