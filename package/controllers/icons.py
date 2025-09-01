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
            (mw.ui.action_zoomin, f":/{icon_set}/resources/{icon_set}/zoom-in.svg"),
            (mw.ui.action_zoomout, f":/{icon_set}/resources/{icon_set}/zoom-out.svg"),
            (mw.ui.action_edit_variables, f":/{icon_set}/resources/{icon_set}/text-editor.svg"),
            (mw.ui.action_zoomfitpage, f":/{icon_set}/resources/{icon_set}/zoom-fit-width.svg"),
            (mw.ui.action_edit_templates, f":/{icon_set}/resources/{icon_set}/template.svg"),
            (mw.ui.action_edit_composition, f":/{icon_set}/resources/{icon_set}/items-tree.svg"),
            (mw.ui.action_clear_trash, f":/{icon_set}/resources/{icon_set}/trash.svg"),
            (mw.ui.action_edit_cable_lists, f":/{icon_set}/resources/{icon_set}/items-list.svg"),
            (mw.ui.action_edit_sector_names, f":/{icon_set}/resources/{icon_set}/items-list.svg"),
            (mw.ui.action_settings, f":/{icon_set}/resources/{icon_set}/settings.svg"),
        ]
        for action, icon_path in actions_and_icons:
            icon = QIcon()
            icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
            action.setIcon(icon)