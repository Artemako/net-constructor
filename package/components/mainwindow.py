from PySide6.QtWidgets import QMainWindow, QMenu, QFileDialog

import package.controllers.style as style
import package.controllers.imagewidget as imagewidget

import package.ui.mainwindow_ui as mainwindow_ui

import json


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
        # self.start_qt_actions()
        # self.update_menu_recent_projects()
        #
        # октрытие файла
        self.ui.action_open.triggered.connect(self.open_file_nce)

    def open_file_nce(self):
        file_name, _ = QFileDialog.getOpenFileName(self, " ", "", "NCE (пока json) files (*.json)")
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.ui.imagewidget.run(data)
