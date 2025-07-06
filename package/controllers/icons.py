from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize

class Icons:
    def __init__(self):
        self.__icon_sets = {"dark": "white-icons", "light": "black-icons"}

    def set_icons_for_mw_by_name(self, mw, theme_name = "dark"):
        icon_set = self.__icon_sets.get(theme_name)
        actions_and_icons = [
            (mw.ui.action_new, f":/{icon_set}/resources/{icon_set}/add-file.svg"),
            (mw.ui.action_open, f":/{icon_set}/resources/{icon_set}/open.svg"),
            (mw.ui.action_saveas, f":/{icon_set}/resources/{icon_set}/save.svg"),
            (mw.ui.action_save, f":/{icon_set}/resources/{icon_set}/save.svg"),
            (mw.ui.action_export_to_image, f":/{icon_set}/resources/{icon_set}/export.svg"),
            (mw.ui.action_parameters, f":/{icon_set}/resources/{icon_set}/show-properties.svg"),
        ]
        for action, icon_path in actions_and_icons:
            icon = QIcon()
            icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
            action.setIcon(icon)