# mainwindow.py
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
    QMessageBox,
    QApplication,
    QToolButton,
    QStyle,
    QHBoxLayout,
    QStyledItemDelegate,
    QWidget,
)

from PySide6.QtGui import (
    QRegularExpressionValidator,
    QIntValidator,
    QFont,
    QColor,
    QFontMetrics,
    QKeySequence,
    QAction,
    QIcon,
)
from PySide6.QtCore import QRegularExpression, Qt, QModelIndex, QLocale, QSettings

import package.controllers.style as style
import package.controllers.icons as icons
import package.controllers.imagewidget as imagewidget

import package.components.nodeconnectionselectdialog as nodeconnectionselectdialog
import package.components.nodeconnectiondeletedialog as nodeconnectiondeletedialog
import package.components.diagramtypeselectdialog as diagramtypeselectdialog
import package.components.changeorderdialog as changeorderdialog
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
        # Скрываем вкладки
        if index in [0, 1]:
            self.ui.tabw_right.tabBar().setTabVisible(2, False)
        elif index == 2:
            self.ui.tabw_right.tabBar().setTabVisible(3, False)
            self._clear_error_messages()
            self._validate_connection(self.__current_object, show_errors=True)

    def config(self):
        # тема
        self.__settings = QSettings("Constant", "Net-constructor")
        self.__theme_name = self.__settings.value("theme_name", "dark")
        # СТИЛЬ
        self.__obj_style = style.Style()
        self.__obj_style.set_style_for_mw_by_name(self, self.__theme_name)
        # + иконки
        self.__obj_icons = icons.Icons()
        self.__obj_icons.set_icons_for_mw_by_name(self, self.__theme_name)
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
        self.ui.tabw_right.tabBar().setTabVisible(2, False)
        self.ui.tabw_right.tabBar().setTabVisible(3, False)
        self.ui.tabw_right.currentChanged.connect(self._tab_right_changed)

        # self.update_menu_recent_projects()
        #
        self.ui.btn_addnode.clicked.connect(self._add_node)
        self.ui.btn_movenodes.clicked.connect(self._move_nodes)
        # self.ui.btn_deletenode.clicked.connect(self._delete_node)
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
        # видимость параметров
        self.ui.action_parameters.triggered.connect(self._toggle_parameters_visibility)
        # смены темы
        self.ui.dark_action.triggered.connect(lambda: self._change_theme("dark"))
        self.ui.light_action.triggered.connect(lambda: self._change_theme("light"))

    def _change_theme(self, theme_name):
        self.__settings.setValue("theme_name", theme_name)
        self.__obj_style.set_style_for_mw_by_name(self, theme_name)
        self.__obj_icons.set_icons_for_mw_by_name(self, theme_name)
        # self.setStyleSheet(style)
        # QApplication.instance().setStyleSheet(style)

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

    def _toggle_parameters_visibility(self):
        # Обновляем все вкладки при изменении видимости параметров
        project_data = self.__obsm.obj_project.get_data()
        
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
                control_sectors_config = (
                    self.__obsm.obj_configs.get_config_control_sectors()
                )
                #
                self.__obsm.obj_project.create_new_project(
                    diagram_data, control_sectors_config, file_name
                )
                #
                project_data = self.__obsm.obj_project.get_data()
                #
                self.ui.imagewidget.run(project_data, is_new=True)
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
            self.ui.imagewidget.run(project_data, is_new=True)
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
                        item_cs_name = self.ui.tw_control_sectors.item(row, 1)
                        item_cs_physical_length = self.ui.tw_control_sectors.item(
                            row, 2
                        )
                        if item_cs_name:
                            cs["data_pars"]["cs_name"]["value"] = (
                                item_cs_name.text().strip()
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
                # Получаем новые значения из виджетов
                new_control_sector_parameters = self._get_new_data_or_parameters(
                    self.__control_data_parameters_widgets, is_parameters=True
                )
                print(
                    f"new_control_sector_parameters = {new_control_sector_parameters}"
                )
                # Обновляем данные контрольного сектора
                if self.__current_control_sector is not None:
                    print(
                        f"self.__current_control_sector = {self.__current_control_sector}"
                    )
                    for key, value in new_control_sector_parameters.items():
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

            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_widgets_by_data(project_data)

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

                # Если добавляем соединение, обновляем таблицу секторов
                if not key_dict_node_and_key_dict_connection.get("node"):
                    connections = project_data.get("connections", [])
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

        # Удаляем пару (узел и соединение)
        self.__obsm.obj_project.delete_pair(node, connection_to_delete)

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
        #
        if self.__obsm.obj_project.is_active() and new_type_id != current_type_id:
            config_nodes = self.__obsm.obj_configs.get_nodes()
            config_connections = self.__obsm.obj_configs.get_connections()
            self.__obsm.obj_project.change_type_diagram(
                new_diagram, config_nodes, config_connections
            )
            #
            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_widgets_by_data(project_data)

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
            self.ui.fl_diagram_parameters,
            config_diagram_parameters,
            diagram_parameters,
            combined_data_parameters=False,
        )
        self.ui.label_diagram_parameters.setVisible(flag)
        self.ui.line_p_dia.setVisible(flag)

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
            table_widget = self.ui.tablew_nodes
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

        self._save_and_restore_scroll_position(self.ui.tablew_nodes, reset_nodes)

    def _reset_table_connections(self, connections):
        def reset_connections():
            print("reset_table_connections")
            table_widget = self.ui.tablew_connections
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
            self.ui.tablew_connections, reset_connections
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
            table_widget = self.ui.tw_control_sectors
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

                cs_name = cs.get("data_pars", {}).get("cs_name", {}).get("value", "")
                item_name = QTableWidgetItem(cs_name)
                item_name.setFlags(item_name.flags() | Qt.ItemIsEditable)
                table_widget.setItem(index, 1, item_name)

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

            table_widget.blockSignals(False)

        self._save_and_restore_scroll_position(
            self.ui.tw_control_sectors, reset_control_sectors
        )

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
        self._clear_form_layout(self.ui.fl_control)
        self._create_control_sector_widgets(cs)

    def _create_control_sector_widgets(self, cs):
        self._clear_form_layout(self.ui.fl_control)
        # получаем precision_separator и precision_number из параметров диаграммы
        precision_separator, precision_number = (
            self._get_precision_separator_and_number()
        )
        #
        self.__control_data_parameters_widgets = {}
        # Получить именно через config
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
            precision_number,
            combined_data_parameters=True,
        )

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

        print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _get_widget(
        self,
        widget_type,
        value,
        arguments,
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
        if combined_data_parameters or is_action_parameters:
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
                    is_parameters=True,
                    precision_separator=precision_separator,
                    precision_number=precision_number,
                )

                # Для секторов
                is_parameter = config_parameter_data.get("is_parameter", False)
                if (
                    combined_data_parameters
                    and not is_action_parameters
                    and is_parameter
                ):
                    continue

                widget_to_add = self._create_widget_with_info(new_widget, info)
                form_layout.addRow(label, widget_to_add)

                if widget_type != "title":
                    dict_widgets[config_parameter_key] = [widget_type, new_widget]

        # print("BEFORE return len(dict_widgets) > 0: dict_widgets", dict_widgets)
        return len(dict_widgets) > 0

    def _add_control_sector(self, obj):
        control_sectors = self.__obsm.obj_project.add_control_sector(
            obj, penultimate=True
        )
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

    def _delete_control_sector(self, obj, selected_cs):
        control_sectors = self.__obsm.obj_project.delete_control_sector(
            obj, selected_cs
        )
        #
        project_data = self.__obsm.obj_project.get_data()
        self.ui.imagewidget.run(project_data)
        self._reset_table_control_sectors(control_sectors)

    def _create_editor_control_sectors_by_object(self, obj, is_node=False):
        self.ui.label_control_sectors.setVisible(not is_node)
        self.ui.line_cont_sect.setVisible(not is_node)
        #
        self.ui.tw_control_sectors.setVisible(not is_node)
        self.ui.btn_add_control_sector.setVisible(not is_node)
        self.ui.btn_move_control_sectors.setVisible(not is_node)
        # отключаем старые обработчики
        try:
            self.ui.btn_add_control_sector.clicked.disconnect()
            self.ui.btn_move_control_sectors.clicked.disconnect()
        except:
            pass
        #
        self.ui.btn_add_control_sector.clicked.connect(
            partial(self._add_control_sector, obj)
        )
        self.ui.btn_move_control_sectors.clicked.connect(
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
        flag = self._create_parameters_widgets(
            self.__editor_object_parameters_widgets,
            self.ui.fl_object_parameters,
            config_object_parameters,
            object_parameters,
            combined_data_parameters=False,
        )
        self.ui.label_object_parameters.setVisible(flag)
        self.ui.line_pars.setVisible(flag)
        #
        flag = self._create_parameters_widgets(
            self.__editor_type_object_parameters_widgets,
            self.ui.fl_type_object_parameters,
            config_type_object_parameters,
            object_parameters,
            combined_data_parameters=False,
        )
        self.ui.label_type_object_parameters.setVisible(flag)
        self.ui.line_type_pars.setVisible(flag)
        #
        flag = self._create_parameters_widgets(
            self.__editor_objects_parameters_widgets,
            self.ui.fl_objects_parameters,
            config_objects_parameters,
            object_parameters,
            combined_data_parameters=False,
        )
        self.ui.label_objects_parameters.setVisible(flag)
        self.ui.line_global_pars.setVisible(flag)

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
        self.ui.line_data.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_type_object_data_widgets,
            self.ui.fl_type_object_data,
            config_type_object_data,
            object_data,
        )
        self.ui.label_type_object_data.setVisible(flag)
        self.ui.line_type_data.setVisible(flag)
        #
        flag = self.create_data_widgets(
            self.__editor_objects_data_widgets,
            self.ui.fl_objects_data,
            config_objects_data,
            object_data,
        )
        self.ui.label_objects_data.setVisible(flag)
        self.ui.line_global_data.setVisible(flag)

    def node_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы узлов"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.ui.tablew_nodes.currentRow()
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
        action = menu.exec_(self.ui.tablew_nodes.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if selected_row >= 0 and selected_node:
            if action == copy_data_action:
                self.__obsm.obj_project.copy_node_data(selected_node)
            elif action == paste_data_action:
                self.__obsm.obj_project.paste_node_data(selected_node)
                # Обновляем интерфейс
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)
            elif action == delete_with_left_action:
                self._delete_node_with_connection(selected_node, "left")
            elif action == delete_with_right_action:
                self._delete_node_with_connection(selected_node, "right")

    def connection_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы соединений"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.ui.tablew_connections.currentRow()
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
        action = menu.exec_(self.ui.tablew_connections.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if selected_row >= 0 and selected_connection:
            if action == copy_data_action:
                self.__obsm.obj_project.copy_connection_data(selected_connection)
            elif action == paste_data_action:
                self.__obsm.obj_project.paste_connection_data(selected_connection)
                # Обновляем интерфейс
                project_data = self.__obsm.obj_project.get_data()
                self.ui.imagewidget.run(project_data)
                self._reset_widgets_by_data(project_data)

    def control_sector_table_context_menu(self, position):
        """Отображение контекстного меню для таблицы контрольных секторов"""
        menu = QMenu()
        menu.setStyleSheet(self.styleSheet())

        selected_row = self.ui.tw_control_sectors.currentRow()
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
        action = menu.exec_(self.ui.tw_control_sectors.viewport().mapToGlobal(position))

        # Обработка выбора действия
        if action == copy_data_action and selected_cs:
            self.__obsm.obj_project.copy_control_sector_data(selected_cs)
        elif action == paste_data_action and selected_cs:
            self.__obsm.obj_project.paste_control_sector_data(selected_cs)
            # Обновляем интерфейс
            project_data = self.__obsm.obj_project.get_data()
            self.ui.imagewidget.run(project_data)
            self._reset_table_control_sectors(control_sectors)
        elif action == delete_action and selected_cs:
            self._delete_control_sector(obj, selected_cs)

    def _clear_error_messages(self):
        """
        Очищает все сообщения об ошибках из контейнера vl_edit_errors.
        """
        while self.ui.vl_edit_errors.count():
            item = self.ui.vl_edit_errors.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.ui.label_edit_errors.setVisible(False)
        self.ui.line_errors.setVisible(False)

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
        self.ui.label_edit_errors.setVisible(True)
        self.ui.line_errors.setVisible(True)

        # Используем QLabel вместо QTextEdit
        error_label = QLabel()
        error_label.setText(message)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("color: #e29c4a;")

        self.ui.vl_edit_errors.addWidget(error_label)

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
        Сохранение выполняется только если фокус не находится в текстовом поле.
        """
        from PySide6.QtCore import QEvent
        from PySide6.QtGui import QKeyEvent
        
        if event.type() == QEvent.KeyPress:
            key_event = QKeyEvent(event)
            if key_event.key() == Qt.Key_Return or key_event.key() == Qt.Key_Enter:
                # Получаем виджет с фокусом
                focused_widget = QApplication.focusWidget()
                
                # Проверяем, является ли виджет с фокусом текстовым полем
                if focused_widget is not None:
                    widget_class_name = focused_widget.__class__.__name__
                    if widget_class_name in ['QLineEdit', 'QTextEdit', 'QPlainTextEdit']:
                        # Если фокус в текстовом поле, не выполняем сохранение
                        return False
                
                # Если фокус не в текстовом поле, выполняем сохранение
                if self.__obsm.obj_project.is_active():
                    self._save_changes_to_file_nce()
                return True
        
        return False
