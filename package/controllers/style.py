from PySide6.QtWidgets import QApplication

class Style:
    def __init__(self):
        self.__themes = {
            "dark": qss,
            "light": lqss 
        }
        self.current_theme = "dark"

    def setting_all_osbm(self, osbm):
        """Установить OSBM"""
        self.__osbm = osbm

    def get_png_prefix(self, theme_name=None):
        """
        Получить префикс для PNG ресурсов в зависимости от темы
        
        Args:
            theme_name (str): Название темы. Если None, используется текущая тема
            
        Returns:
            str: Префикс для PNG ресурсов
        """
        if theme_name is None:
            theme_name = self.current_theme
            
        if theme_name == "light":
            return "white-png"
        else:
            return "black-png"

    def get_theme_style(self, theme_name=None):
        """
        Получить стиль для темы с правильными путями к PNG файлам
        
        Args:
            theme_name (str): Название темы. Если None, используется текущая тема
            
        Returns:
            str: Стиль с правильными путями к PNG файлам
        """
        if theme_name is None:
            theme_name = self.current_theme
            
        # Получаем базовый стиль для темы
        base_style = self.__themes.get(theme_name, self.__themes["dark"])
        
        # Получаем правильный префикс для PNG файлов
        png_prefix = self.get_png_prefix(theme_name)
        
        # Заменяем пути к PNG файлам
        style = base_style.replace(":/png/resources/png/", f":/{png_prefix}/resources/{png_prefix}/")
        
        return style

    def set_style_for(self, widget):
        """Совместимый метод для установки стиля для виджета (использует текущую тему)"""
        style = self.get_theme_style()
        widget.setStyleSheet(style)

    def set_style_for_mw_by_name(self, mw, theme_name="dark"):
        """Установить стиль для главного окна по имени темы"""
        style = self.get_theme_style(theme_name)
        mw.setStyleSheet(style)
        self.current_theme = theme_name
        
        # Сохраняем выбор темы в настройках
        if hasattr(self, '__osbm') and self.__osbm and hasattr(self.__osbm, 'obj_settings'):
            self.__osbm.obj_settings.set_theme(theme_name)
            self.__osbm.obj_settings.sync()

    def get_available_themes(self):
        """Получить список доступных тем"""
        return list(self.__themes.keys())

    def get_current_theme(self):
        """Получить текущую тему"""
        return self.current_theme

    def apply_theme_to_all_windows(self, theme_name):
        """Применить тему ко всем окнам приложения"""
        self.current_theme = theme_name
        style = self.get_theme_style(theme_name)
        
        # Применяем стиль ко всем виджетам приложения
        for widget in QApplication.allWidgets():
            widget.setStyleSheet(style)
        
        # Принудительно обновляем layout'ы для корректной работы WrapLongRows
        self._force_layout_updates()
        
        # Сохраняем в настройках
        if hasattr(self, '__osbm') and self.__osbm and hasattr(self.__osbm, 'obj_settings'):
            self.__osbm.obj_settings.set_theme(theme_name)
            self.__osbm.obj_settings.sync()

    def toggle_theme(self):
        """Переключить между темами"""
        current_theme = self.get_current_theme()
        new_theme = "light" if current_theme == "dark" else "dark"
        self.apply_theme_to_all_windows(new_theme)
        return new_theme

    def _force_layout_updates(self):
        """Принудительно обновляет все layout'ы для корректной работы WrapLongRows после смены темы"""
        try:
            from PySide6.QtWidgets import QApplication, QWidget
            
            # Получаем все виджеты
            for widget in QApplication.allWidgets():
                if isinstance(widget, QWidget):
                    # Обновляем layout виджета и всех его дочерних элементов
                    self._update_widget_layouts_recursive(widget)
                    
        except Exception as e:
            # Логируем ошибку, если есть система логирования
            if hasattr(self, '__osbm') and self.__osbm and hasattr(self.__osbm, 'obj_logg'):
                self.__osbm.obj_logg.debug_logger(f"Error updating layouts: {e}")
                
    def _update_widget_layouts_recursive(self, widget):
        """Рекурсивно обновляет layout'ы виджета и всех его дочерних элементов"""
        try:
            from PySide6.QtWidgets import QFormLayout, QLayout
            
            # Обновляем layout текущего виджета
            layout = widget.layout()
            if layout:
                # Особое внимание QFormLayout с WrapLongRows
                if isinstance(layout, QFormLayout):
                    # Принудительно инвалидируем и обновляем layout
                    layout.invalidate()
                    layout.activate()
                    widget.updateGeometry()
                elif isinstance(layout, QLayout):
                    # Для других типов layout'ов
                    layout.invalidate()
                    layout.activate()
                    
                # Рекурсивно обновляем все дочерние layout'ы
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget():
                        self._update_widget_layouts_recursive(item.widget())
                        
            # Принудительно обновляем размеры и геометрию виджета
            widget.updateGeometry()
            widget.update()
            
        except Exception:
            # Игнорируем ошибки для отдельных виджетов
            pass


qss = """
/*!*************************************
    VS15 Dark
****************************************
    Author: chintsu_kun, holt59, MO2 Team
    Version: 2.5.0
    Licence: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)
    Source: https://github.com/nikolay-borzov/modorganizer-themes
****************************************
*/

/* For some reason applying background-color or border fixes paddings properties */
QListWidget::item {
    border-width: 0;
}

/* Don't override install label on download widget.
     MO2 assigns color depending on download state */
#installLabel {
    color: none;
}

/* Make `background-color` work for :hover, :focus and :pressed states */
QToolButton {
    border: none;
}

* {
    font-family: Open Sans;
}

/* Main Window */
QWidget {
    background-color: #2d2d30;
    color: #f1f1f1;
}

QWidget::disabled {
    color: #656565;
}

/* Common */
/* remove outline */
* {
    outline: 0;
}

*:disabled,
QListView::item:disabled,
*::item:selected:disabled {
    color: #656565;
}

/* line heights */
/* QTreeView#fileTree::item - currently have problem with size column vertical
     text align */
#bsaList::item,
#dataTree::item,
#modList::item,
#categoriesTree::item,
#savegameList::item,
#tabConflicts QTreeWidget::item {
    padding: 0.3em 0;
}

QListView::item,
QTreeView#espList::item {
    /*
    padding: 0.3em 0;
    */
}
QListView#lw_pages_template::item {
    padding: 0.2em 0;
}

/* to enable border color */
QTreeView,
QListView,
QTextEdit,
QWebView,
QTableView {
    border-style: solid;
    border-width: 1px;
}

QAbstractItemView {
    color: #dcdcdc;
    background-color: #1e1e1e;
    alternate-background-color: #262626;
    border-color: #3f3f46;
}

QAbstractItemView::item:selected,
QAbstractItemView::item:selected:hover,
QAbstractItemView::item:alternate:selected,
QAbstractItemView::item:alternate:selected:hover {
    color: #f1f1f1;
    background-color: #3399ff;
}

QAbstractItemView[filtered=true] {
    border: 2px solid #f00 !important;
}

QAbstractItemView,
QListView,
QTreeView {
    show-decoration-selected: 1;
}

QAbstractItemView::item:hover,
QAbstractItemView::item:alternate:hover,
QAbstractItemView::item:disabled:hover,
QAbstractItemView::item:alternate:disabled:hover QListView::item:hover,
QTreeView::branch:hover,
QTreeWidget::item:hover {
    background-color: rgba(51, 153, 255, 0.3);
}

QAbstractItemView::item:selected:disabled,
QAbstractItemView::item:alternate:selected:disabled,
QListView::item:selected:disabled,
QTreeView::branch:selected:disabled,
QTreeWidget::item:selected:disabled {
    background-color: rgba(51, 153, 255, 0.3);
}

QTreeView::branch:selected,
#bsaList::branch:selected {
    background-color: #3399ff;
}

QLabel {
    background-color: transparent;
}

LinkLabel {
    qproperty-linkColor: #3399ff;
}

/* Left Pane & File Trees #QTreeView, #QListView*/
QTreeView::branch:closed:has-children {
    image: url(:/png/resources/png/branch-closed.png);
}

QTreeView::branch:open:has-children {
    image: url(:/png/resources/png/branch-open.png);
}

QListView::item {
    color: #f1f1f1;
}

/* Text areas and text fields #QTextEdit, #QLineEdit, #QWebView */
QTextEdit,
QWebView,
QLineEdit,
QAbstractSpinBox,
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button,
QComboBox {
    background-color: #333337;
    border-color: #3f3f46;
}

QLineEdit:hover,
QAbstractSpinBox:hover,
QTextEdit:hover,
QComboBox:hover,
QComboBox:editable:hover {
    border-color: #007acc;
}

QLineEdit:focus,
QAbstractSpinBox::focus,
QTextEdit:focus,
QComboBox:focus,
QComboBox:editable:focus,
QComboBox:on {
    background-color: #3f3f46;
    border-color: #3399ff;
}

QComboBox:on {
    border-bottom-color: #3f3f46;
}

QLineEdit,
QAbstractSpinBox {
    min-height: 15px;
    padding: 2px;
    border-style: solid;
    border-width: 1px;
    /* Оптимальная минимальная ширина на основе золотого сечения */
    min-width: 130px;
}

/* Специфичные размеры для разных типов полей ввода */
QSpinBox, QDoubleSpinBox {
    min-width: 110px; /* Для числового ввода */
}

QLineEdit {
    margin-top: 0;
}

/* clear button */
QLineEdit QToolButton,
QLineEdit QToolButton:hover {
    background: none;
    margin-top: 1px;
}

QLineEdit#espFilterEdit QToolButton {
    margin-top: -2px;
    margin-bottom: 1px;
}

/* Drop-downs #QComboBox*/
QComboBox {
    min-height: 20px;
    padding-left: 5px;
    margin: 3px 0 1px 0;
    border-style: solid;
    border-width: 1px;
    /* Оптимальная минимальная ширина для dropdown с учетом стрелки */
    min-width: 150px;
}

QComboBox:editable {
    padding-left: 3px;
    /* to enable hover styles */
    background-color: transparent;
}

QComboBox::drop-down {
    width: 20px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border: none;
}

QComboBox::down-arrow {
    image: url(:/png/resources/png/combobox-down.png);
}

QComboBox QAbstractItemView {
    background-color: #1b1b1c;
    selection-background-color: #3f3f46;
    border-color: #3399ff;
    border-style: solid;
    border-width: 0 1px 1px 1px;
}

/* Doesn't work http://stackoverflow.com/questions/13308341/qcombobox-abstractitemviewitem */
/* QComboBox QAbstractItemView:item {
    padding: 10px;
    margin: 10px;
} */
/* Toolbar */
QToolBar {
    border: none;
}

QToolBar::separator {
    border-left-color: #222222;
    border-right-color: #46464a;
    border-width: 0 1px 0 1px;
    border-style: solid;
    width: 0;
}

QToolButton {
    padding: 4px;
}

QToolButton:hover, QToolButton:focus {
    background-color: #3e3e40;
}

QToolButton:pressed {
    background-color: #3399ff;
}

QToolButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-top: 10%;
    padding-right: 5%;
}

/* Group Boxes #QGroupBox */
QGroupBox {
    border-color: #3f3f46;
    border-style: solid;
    border-width: 1px;
    padding: 10px 5px 5px 5px;
    margin-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px;
    left: 10px;
}

/* LCD Count */
QLCDNumber {
    border-color: #3f3f46;
    border-style: solid;
    border-width: 1px;
}

/* Buttons #QPushButton */
QPushButton {
    background-color: #333337;
    border-color: #3f3f46;
    min-height: 18px;
    padding: 2px 5px;
    border-style: solid;
    border-width: 1px;
}

QPushButton:hover,
QPushButton:checked,
QAbstractSpinBox::up-button:hover,
QAbstractSpinBox::down-button:hover {
    background-color: #007acc;
}

QPushButton:focus {
    border-color: #007acc;
}

QPushButton:pressed,
QPushButton:checked:hover,
QAbstractSpinBox::up-button:pressed,
QAbstractSpinBox::down-button:pressed {
    background-color: #1c97ea;
}

QPushButton:disabled,
QAbstractSpinBox::up-button:disabled,
QAbstractSpinBox::down-button:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}

QPushButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 5%;
}

/* Dialog buttons */
QSlider::handle:horizontal,
QSlider::handle:vertical {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}

QSlider::handle:horizontal:hover,
QSlider::handle:vertical:hover,
QSlider::handle:horizontal:pressed,
QSlider::handle:horizontal:focus:pressed,
QSlider::handle:vertical:pressed,
QSlider::handle:vertical:focus:pressed {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}

QSlider::handle:horizontal:focus,
QSlider::handle:vertical:focus {
    background-color: #dddddd;
    border-color: #3399ff;
}


QSlider::handle:horizontal:disabled,
QSlider::handle:vertical:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}


/* Check boxes and Radio buttons common #QCheckBox, #QRadioButton */
QListView::indicator,
QGroupBox::indicator,
QTreeView::indicator,
QCheckBox::indicator,
QRadioButton::indicator {
    background-color: #2d2d30;
    border-color: #3f3f46;
    width: 13px;
    height: 13px;
    border-style: solid;
    border-width: 1px;
}
QListView::indicator:hover,
QGroupBox::indicator:hover,
QTreeView::indicator:hover,
QCheckBox::indicator:hover,
QRadioButton::indicator:hover {
    background-color: #3f3f46;
    border-color: #007acc;
}
QListView::indicator:checked,
QGroupBox::indicator:checked,
QTreeView::indicator:checked,
QCheckBox::indicator:checked {
    image: url(:/png/resources/png/checkbox-check.png);
}
QListView::indicator:checked:disabled,
QGroupBox::indicator:disabled,
QTreeView::indicator:checked:disabled,
QCheckBox::indicator:checked:disabled {
    image: url(:/png/resources/png/checkbox-check-disabled.png);
}

/* Check boxes special */
QTreeView#modList::indicator {
    width: 15px;
    height: 15px;
}

/* Radio buttons #QRadioButton */
QRadioButton::indicator {
    border-radius: 7px;
}

QRadioButton::indicator::checked {
    background-color: #B9B9BA;
    border-width: 2px;
    width: 11px;
    height: 11px;
}

QRadioButton::indicator::checked:hover {
    border-color: #3f3f46;
}

/* Spinners #QSpinBox, #QDoubleSpinBox */
QAbstractSpinBox {
    margin: 1px;
}

QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button {
    border-style: solid;
    border-width: 1px;
    subcontrol-origin: padding;
}

QAbstractSpinBox::up-button {
    subcontrol-position: top right;
}

QAbstractSpinBox::up-arrow {
    image: url(:/png/resources/png/spinner-up.png);
}

QAbstractSpinBox::down-button {
    subcontrol-position: bottom right;
}

QAbstractSpinBox::down-arrow {
    image: url(:/png/resources/png/spinner-down.png);
}

/* Sliders #QSlider */
QSlider::groove:horizontal {
    background-color: #3f3f46;
    border: none;
    height: 8px;
    margin: 2px 0;
}

QSlider::handle:horizontal {
    width: 0.5em;
    height: 2em;
    margin: -7px 0;
    subcontrol-origin: margin;
}

/* Scroll Bars #QAbstractScrollArea, #QScrollBar*/
/* assigning background still leaves not filled area*/
QAbstractScrollArea::corner {
    background-color: transparent;
}

/* Horizontal */
QScrollBar:horizontal {
    height: 18px;
    border: none;
    margin: 0 23px 0 23px;
}

QScrollBar::handle:horizontal {
    min-width: 32px;
    margin: 4px 2px;
}

QScrollBar::add-line:horizontal {
    width: 23px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    width: 23px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

/* Vertical */
QScrollBar:vertical {
    width: 20px;
    border: none;
    margin: 23px 0 23px 0;
}

QScrollBar::handle:vertical {
    min-height: 32px;
    margin: 2px 4px;
}

QScrollBar::add-line:vertical {
    height: 23px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    height: 23px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

/* Combined */
QScrollBar {
    background-color: #3e3e42;
    border: none;
}

QScrollBar::handle {
    background-color: #686868;
}

QScrollBar::add-line,
QScrollBar::sub-line {
    background-color: #3e3e42;
    border: none;
}

/* QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::add-line:vertical:hover,
QScrollBar::sub-line:vertical:hover,
QScrollBar::add-line:horizontal:pressed,
QScrollBar::sub-line:horizontal:pressed,
QScrollBar::add-line:vertical:pressed,
QScrollBar::sub-line:vertical:pressed { } */
QScrollBar::handle:hover {
    background: #9e9e9e;
}

QScrollBar::handle:pressed {
    background: #efebef;
}

QScrollBar::handle:disabled {
    background: #555558;
}

QScrollBar::add-page,
QScrollBar::sub-page {
    background: transparent;
}

QScrollBar::up-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-up.png);
}

QScrollBar::up-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-up-hover.png);
}

QScrollBar::up-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-up-disabled.png);
}

QScrollBar::right-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-right.png);
}

QScrollBar::right-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}

QScrollBar::right-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-right-disabled.png);
}

QScrollBar::down-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-down.png);
}

QScrollBar::down-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-down-hover.png);
}

QScrollBar::down-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-down-disabled.png);
}

QScrollBar::left-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-left.png);
}

QScrollBar::left-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}

QScrollBar::left-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-left-disabled.png);
}

/* Header Rows and Tables (Configure Mod Categories) #QTableView, #QHeaderView */
QTableView {
    gridline-color: #3f3f46;
    selection-background-color: #3399ff;
    selection-color: #f1f1f1;
}

QTableView QTableCornerButton::section {
    background: #252526;
    border-color: #3f3f46;
    border-style: solid;
    border-width: 0 1px 1px 0;
}

QHeaderView {
    border: none;
}

QHeaderView::section {
    background: #252526;
    border-color: #3f3f46;
    padding: 3px 5px;
    border-style: solid;
    border-width: 0 1px 1px 0;
}

QHeaderView::section:hover {
    background: #3e3e40;
    color: #f6f6f6;
}

QHeaderView::section:last {
    border-right: 0;
}

QHeaderView::up-arrow {
    image: url(:/png/resources/png/sort-asc.png);
    width: 0px;
}


QHeaderView::down-arrow {
    image: url(:/png/resources/png/sort-desc.png);
    width: 0px;
}


/* Context menus, toolbar drop-downs #QMenu    */
QMenu {
    background-color: #1a1a1c;
    border-color: #333337;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}

QMenu::item {
    background: transparent;
    padding: 4px 20px;
}

QMenu::item:selected,
QMenuBar::item:selected {
    background-color: #333334;
}

QMenu::item:disabled {
    background-color: transparent;
}

QMenu::separator {
    background-color: #333337;
    height: 1px;
    margin: 1px 0;
}

QMenu::icon {
    margin: 1px;
}

QMenu::right-arrow {
    image: url(:/png/resources/png/sub-menu-arrow.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 0.5em;
}

QMenu QPushButton {
    background-color: transparent;
    border-color: #3f3f46;
    margin: 1px 0 1px 0;
}

QMenu QCheckBox,
QMenu QRadioButton {
    background-color: transparent;
    padding: 5px 2px;
}

/* Tool tips #QToolTip, #SaveGameInfoWidget */
QToolTip,
SaveGameInfoWidget {
    background-color: #424245;
    border-color: #4d4d50;
    color: #f1f1f1;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}

QStatusBar::item {
    border: None;
}

/* Progress Bars (Downloads) #QProgressBar */
QProgressBar {
    background-color: #e6e6e6;
    color: #000;
    border-color: #bcbcbc;
    text-align: center;
    border-style: solid;
    border-width: 1px;
    margin: 0px;
}

QProgressBar::chunk {
    background: #06b025;
}

DownloadListView[downloadView=standard]::item {
    padding: 16px;
}

DownloadListView[downloadView=compact]::item {
    padding: 4px;
}

/* Right Pane and Tab Bars #QTabWidget, #QTabBar */
QTabWidget::pane {
    border-color: #3f3f46;
    border-top-color: #007acc;
    top: 0;
    border-style: solid;
    border-width: 1px;
}

QTabWidget::pane:disabled {
    border-top-color: #3f3f46;
}

QTabBar::tab {
    background-color: transparent;
    padding: 4px 1em;
    border: none;
}

QTabBar::tab:hover {
    background-color: #1c97ea;
}

QTabBar::tab:selected,
QTabBar::tab:selected:hover {
    background-color: #007acc;
}

QTabBar::tab:disabled {
    background-color: transparent;
    color: #656565;
}

QTabBar::tab:selected:disabled {
    background-color: #3f3f46;
}

/* Scrollers */
QTabBar QToolButton {
    background-color: #333337;
    border-color: #3f3f46;
    padding: 1px;
    margin: 0;
    border-style: solid;
    border-width: 1px;
}

QTabBar QToolButton:hover {
    border-color: #007acc;
    border-width: 1px;
    border-style: solid;
}

QTabBar QToolButton:disabled,
QTabBar QToolButton:pressed:hover {
    background-color: #333337;
}

QTabBar::scroller {
    width: 23px;
    background-color: red;
}

QTabBar QToolButton::right-arrow {
    image: url(:/png/resources/png/scrollbar-right.png);
}

QTabBar QToolButton::right-arrow:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}

QTabBar QToolButton::left-arrow {
    image: url(:/png/resources/png/scrollbar-left.png);
}

QTabBar QToolButton::left-arrow:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}

/* Special styles */
QWidget#tabImages QPushButton {
    background-color: transparent;
    margin: 0 0.3em;
    padding: 0;
}

/* like dialog QPushButton*/
QWidget#tabESPs QToolButton {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}

QWidget#tabESPs QToolButton:hover {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}

QWidget#tabESPs QToolButton:focus {
    background-color: #dddddd;
    border-color: #3399ff;
}

QWidget#tabESPs QToolButton:disabled {
    background-color: #333337;
    border-color: #3f3f46;
}

QTreeWidget#categoriesList {
    /* min-width: 225px; */
}

QTreeWidget#categoriesList::item {
    background-position: center left;
    background-repeat: no-repeat;
    padding: 0.35em 10px;
}

QTreeWidget#categoriesList::item:has-children {
    background-image: url(:/png/resources/png/branch-closed.png);
}

QTreeWidget#categoriesList::item:has-children:open {
    background-image: url(:/png/resources/png/branch-open.png);
}

QDialog#QueryOverwriteDialog QPushButton {
    margin-left: 0.5em;
}

QDialog#PyCfgDialog QPushButton:hover {
    background-color: #BEE6FD;
}

QLineEdit#modFilterEdit {
    margin-top: 2px;
}

/* highlight unchecked BSAs */
QWidget#bsaTab QTreeWidget::indicator:unchecked {
    background-color: #3399ff;
}

/* increase version text field */
QLineEdit#versionEdit {
    max-width: 100px;
}

/* Dialogs width changes */
/* increase width to prevent buttons cutting */
QDialog#QueryOverwriteDialog {
    min-width: 565px;
}

QDialog#ModInfoDialog {
    min-width: 850px;
}

QLineEdit[valid-filter=false] {
    background-color: #661111 !important;
}

/* собственное решение */
QToolBar QToolButton:disabled {
    background-color: #252526;
}

QToolBar QToolButton:checked {
    background-color: #3399ff;
}

/* Оптимизация для QFormLayout и WrapLongRows */
QFormLayout {
    /* Обеспечиваем правильное поведение переноса */
    spacing: 6px;
}

/* Убираем жёсткие ограничения ширины для виджетов в формах */
QWidget[qformLayoutWidget="true"] QLineEdit,
QWidget[qformLayoutWidget="true"] QComboBox,
QWidget[qformLayoutWidget="true"] QSpinBox,
QWidget[qformLayoutWidget="true"] QDoubleSpinBox {
    max-width: none;
    min-width: 50px; /* Минимальная разумная ширина */
}

/* Минимальная ширина правого блока с вкладками (на основе золотого сечения) */
QGroupBox[objectName="gb_right"],
QWidget[objectName="gb_right"] {
    min-width: 400px;
}

"""



lqss = """
/*!*************************************
    VS15 Light
****************************************
    Author: chintsu_kun, holt59, MO2 Team
    Modified by: User
    Version: 2.5.0
    Licence: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)
    Source: https://github.com/nikolay-borzov/modorganizer-themes
****************************************
*/
/* For some reason applying background-color or border fixes paddings properties */
QListWidget::item {
    border-width: 0;
}
/* Don't override install label on download widget.
     MO2 assigns color depending on download state */
#installLabel {
    color: none;
}
/* Make `background-color` work for :hover, :focus and :pressed states */
QToolButton {
    border: none;
}
* {
    font-family: Open Sans;
}
/* Main Window */
QWidget {
    background-color: #f9f9f9;
    color: #333333;
}
QWidget::disabled {
    color: #999999;
}
/* Common */
/* remove outline */
* {
    outline: 0;
}
*:disabled,
QListView::item:disabled,
*::item:selected:disabled {
    color: #999999;
}
/* line heights */
/* QTreeView#fileTree::item - currently have problem with size column vertical
     text align */
#bsaList::item,
#dataTree::item,
#modList::item,
#categoriesTree::item,
#savegameList::item,
#tabConflicts QTreeWidget::item {
    padding: 0.3em 0;
}
QListView::item,
QTreeView#espList::item {
    /*
    padding: 0.3em 0;
    */
}
QListView#lw_pages_template::item {
    padding: 0.2em 0;
}
/* to enable border color */
QTreeView,
QListView,
QTextEdit,
QWebView,
QTableView {
    border-style: solid;
    border-width: 1px;
}
QAbstractItemView {
    color: #333333;
    background-color: #ffffff;
    alternate-background-color: #f0f0f0;
    border-color: #cccccc;
}
QAbstractItemView::item:selected,
QAbstractItemView::item:selected:hover,
QAbstractItemView::item:alternate:selected,
QAbstractItemView::item:alternate:selected:hover {
    color: #ffffff;
    background-color: #4a90e2;
}
QAbstractItemView[filtered=true] {
    border: 2px solid #ff0000 !important;
}
QAbstractItemView,
QListView,
QTreeView {
    show-decoration-selected: 1;
}
QAbstractItemView::item:hover,
QAbstractItemView::item:alternate:hover,
QAbstractItemView::item:disabled:hover,
QAbstractItemView::item:alternate:disabled:hover QListView::item:hover,
QTreeView::branch:hover,
QTreeWidget::item:hover {
    background-color: rgba(70, 140, 220, 0.2);
}
QAbstractItemView::item:selected:disabled,
QAbstractItemView::item:alternate:selected:disabled,
QListView::item:selected:disabled,
QTreeView::branch:selected:disabled,
QTreeWidget::item:selected:disabled {
    background-color: rgba(80, 150, 220, 0.2);
}
QTreeView::branch:selected,
#bsaList::branch:selected {
    background-color: #4a90e2;
}
QLabel {
    background-color: transparent;
}
LinkLabel {
    qproperty-linkColor: #4a90e2;
}
/* Left Pane & File Trees #QTreeView, #QListView*/
QTreeView::branch:closed:has-children {
    image: url(:/png/resources/png/branch-closed.png);
}
QTreeView::branch:open:has-children {
    image: url(:/png/resources/png/branch-open.png);
}
QListView::item {
    color: #333333;
}
/* Text areas and text fields #QTextEdit, #QLineEdit, #QWebView */
QTextEdit,
QWebView,
QLineEdit,
QAbstractSpinBox,
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button,
QComboBox {
    background-color: #ffffff;
    border-color: #cccccc;
}
QLineEdit:hover,
QAbstractSpinBox:hover,
QTextEdit:hover,
QComboBox:hover,
QComboBox:editable:hover {
    border-color: #4a90e2;
}
QLineEdit:focus,
QAbstractSpinBox::focus,
QTextEdit:focus,
QComboBox:focus,
QComboBox:editable:focus,
QComboBox:on {
    background-color: #f0f0f0;
    border-color: #4a90e2;
}
QComboBox:on {
    border-bottom-color: #cccccc;
}
QLineEdit,
QAbstractSpinBox {
    min-height: 15px;
    padding: 2px;
    border-style: solid;
    border-width: 1px;
    /* Оптимальная минимальная ширина на основе золотого сечения */
    min-width: 130px;
}

/* Специфичные размеры для разных типов полей ввода */
QSpinBox, QDoubleSpinBox {
    min-width: 110px; /* Для числового ввода */
}
QLineEdit {
    margin-top: 0;
}
/* clear button */
QLineEdit QToolButton,
QLineEdit QToolButton:hover {
    background: none;
    margin-top: 1px;
}
QLineEdit#espFilterEdit QToolButton {
    margin-top: -2px;
    margin-bottom: 1px;
}
/* Drop-downs #QComboBox*/
QComboBox {
    min-height: 20px;
    padding-left: 5px;
    margin: 3px 0 1px 0;
    border-style: solid;
    border-width: 1px;
    /* Оптимальная минимальная ширина для dropdown с учетом стрелки */
    min-width: 150px;
}
QComboBox:editable {
    padding-left: 3px;
    /* to enable hover styles */
    background-color: transparent;
}
QComboBox::drop-down {
    width: 20px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border: none;
}
QComboBox::down-arrow {
    image: url(:/png/resources/png/combobox-down.png);
}
QComboBox QAbstractItemView {
    background-color: #fafafa;
    selection-background-color: #f0f0f0;
    border-color: #4a90e2;
    border-style: solid;
    border-width: 0 1px 1px 1px;
}
/* Doesn't work http://stackoverflow.com/questions/13308341/qcombobox-abstractitemviewitem */
/* QComboBox QAbstractItemView:item {
    padding: 10px;
    margin: 10px;
} */
/* Toolbar */
QToolBar {
    border: none;
}
QToolBar::separator {
    border-left-color: #dddddd;
    border-right-color: #bbbbbb;
    border-width: 0 1px 0 1px;
    border-style: solid;
    width: 0;
}
QToolButton {
    padding: 4px;
}
QToolButton:hover, QToolButton:focus {
    background-color: #e0e0e0;
}
QToolButton:pressed {
    background-color: #4a90e2;
}
QToolButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-top: 10%;
    padding-right: 5%;
}
/* Group Boxes #QGroupBox */
QGroupBox {
    border-color: #cccccc;
    border-style: solid;
    border-width: 1px;
    padding: 10px 5px 5px 5px;
    margin-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px;
    left: 10px;
}
/* LCD Count */
QLCDNumber {
    border-color: #cccccc;
    border-style: solid;
    border-width: 1px;
}
/* Buttons #QPushButton */
QPushButton {
    background-color: #f0f0f0;
    border-color: #cccccc;
    min-height: 18px;
    padding: 2px 5px;
    border-style: solid;
    border-width: 1px;
}
QPushButton:hover,
QPushButton:checked,
QAbstractSpinBox::up-button:hover,
QAbstractSpinBox::down-button:hover {
    background-color: #4a90e2;
}
QPushButton:focus {
    border-color: #4a90e2;
}
QPushButton:pressed,
QPushButton:checked:hover,
QAbstractSpinBox::up-button:pressed,
QAbstractSpinBox::down-button:pressed {
    background-color: #3c85d8;
}
QPushButton:disabled,
QAbstractSpinBox::up-button:disabled,
QAbstractSpinBox::down-button:disabled {
    background-color: #f0f0f0;
    border-color: #cccccc;
}
QPushButton::menu-indicator {
    image: url(:/png/resources/png/combobox-down.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 5%;
}
/* Dialog buttons */
QSlider::handle:horizontal,
QSlider::handle:vertical {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}
QSlider::handle:horizontal:hover,
QSlider::handle:vertical:hover,
QSlider::handle:horizontal:pressed,
QSlider::handle:horizontal:focus:pressed,
QSlider::handle:vertical:pressed,
QSlider::handle:vertical:focus:pressed {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}
QSlider::handle:horizontal:focus,
QSlider::handle:vertical:focus {
    background-color: #dddddd;
    border-color: #4a90e2;
}
QSlider::handle:horizontal:disabled,
QSlider::handle:vertical:disabled {
    background-color: #f0f0f0;
    border-color: #cccccc;
}
/* Check boxes and Radio buttons common #QCheckBox, #QRadioButton */
QListView::indicator,
QGroupBox::indicator,
QTreeView::indicator,
QCheckBox::indicator,
QRadioButton::indicator {
    background-color: #ffffff;
    border-color: #cccccc;
    width: 13px;
    height: 13px;
    border-style: solid;
    border-width: 1px;
}
QListView::indicator:hover,
QGroupBox::indicator:hover,
QTreeView::indicator:hover,
QCheckBox::indicator:hover,
QRadioButton::indicator:hover {
    background-color: #e0e0e0;
    border-color: #4a90e2;
}
QListView::indicator:checked,
QGroupBox::indicator:checked,
QTreeView::indicator:checked,
QCheckBox::indicator:checked {
    image: url(:/png/resources/png/checkbox-check.png);
}
QListView::indicator:checked:disabled,
QGroupBox::indicator:disabled,
QTreeView::indicator:checked:disabled,
QCheckBox::indicator:checked:disabled {
    image: url(:/png/resources/png/checkbox-check-disabled.png);
}
/* Check boxes special */
QTreeView#modList::indicator {
    width: 15px;
    height: 15px;
}
/* Radio buttons #QRadioButton */
QRadioButton::indicator {
    border-radius: 7px;
}
QRadioButton::indicator::checked {
    background-color: #dcdcdc;
    border-width: 2px;
    width: 11px;
    height: 11px;
}
QRadioButton::indicator::checked:hover {
    border-color: #cccccc;
}
/* Spinners #QSpinBox, #QDoubleSpinBox */
QAbstractSpinBox {
    margin: 1px;
}
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button {
    border-style: solid;
    border-width: 1px;
    subcontrol-origin: padding;
}
QAbstractSpinBox::up-button {
    subcontrol-position: top right;
}
QAbstractSpinBox::up-arrow {
    image: url(:/png/resources/png/spinner-up.png);
}
QAbstractSpinBox::down-button {
    subcontrol-position: bottom right;
}
QAbstractSpinBox::down-arrow {
    image: url(:/png/resources/png/spinner-down.png);
}
/* Sliders #QSlider */
QSlider::groove:horizontal {
    background-color: #cccccc;
    border: none;
    height: 8px;
    margin: 2px 0;
}
QSlider::handle:horizontal {
    width: 0.5em;
    height: 2em;
    margin: -7px 0;
    subcontrol-origin: margin;
}
/* Scroll Bars #QAbstractScrollArea, #QScrollBar*/
/* assigning background still leaves not filled area*/
QAbstractScrollArea::corner {
    background-color: transparent;
}
/* Horizontal */
QScrollBar:horizontal {
    height: 18px;
    border: none;
    margin: 0 23px 0 23px;
}
QScrollBar::handle:horizontal {
    min-width: 32px;
    margin: 4px 2px;
}
QScrollBar::add-line:horizontal {
    width: 23px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    width: 23px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
/* Vertical */
QScrollBar:vertical {
    width: 20px;
    border: none;
    margin: 23px 0 23px 0;
}
QScrollBar::handle:vertical {
    min-height: 32px;
    margin: 2px 4px;
}
QScrollBar::add-line:vertical {
    height: 23px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    height: 23px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
/* Combined */
QScrollBar {
    background-color: #e0e0e0;
    border: none;
}
QScrollBar::handle {
    background-color: #aaaaaa;
}
QScrollBar::add-line,
QScrollBar::sub-line {
    background-color: #e0e0e0;
    border: none;
}
/* QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::add-line:vertical:hover,
QScrollBar::sub-line:vertical:hover,
QScrollBar::add-line:horizontal:pressed,
QScrollBar::sub-line:horizontal:pressed,
QScrollBar::add-line:vertical:pressed,
QScrollBar::sub-line:vertical:pressed { } */
QScrollBar::handle:hover {
    background: #cccccc;
}
QScrollBar::handle:pressed {
    background: #eeeeee;
}
QScrollBar::handle:disabled {
    background: #bbbbbb;
}
QScrollBar::add-page,
QScrollBar::sub-page {
    background: transparent;
}
QScrollBar::up-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-up.png);
}
QScrollBar::up-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-up-hover.png);
}
QScrollBar::up-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-up-disabled.png);
}
QScrollBar::right-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-right.png);
}
QScrollBar::right-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}
QScrollBar::right-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-right-disabled.png);
}
QScrollBar::down-arrow:vertical {
    image: url(:/png/resources/png/scrollbar-down.png);
}
QScrollBar::down-arrow:vertical:hover {
    image: url(:/png/resources/png/scrollbar-down-hover.png);
}
QScrollBar::down-arrow:vertical:disabled {
    image: url(:/png/resources/png/scrollbar-down-disabled.png);
}
QScrollBar::left-arrow:horizontal {
    image: url(:/png/resources/png/scrollbar-left.png);
}
QScrollBar::left-arrow:horizontal:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}
QScrollBar::left-arrow:horizontal:disabled {
    image: url(:/png/resources/png/scrollbar-left-disabled.png);
}
/* Header Rows and Tables (Configure Mod Categories) #QTableView, #QHeaderView */
QTableView {
    gridline-color: #cccccc;
    selection-background-color: #4a90e2;
    selection-color: #ffffff;
}
QTableView QTableCornerButton::section {
    background: #f5f5f5;
    border-color: #cccccc;
    border-style: solid;
    border-width: 0 1px 1px 0;
}
QHeaderView {
    border: none;
}
QHeaderView::section {
    background: #f5f5f5;
    border-color: #cccccc;
    padding: 3px 5px;
    border-style: solid;
    border-width: 0 1px 1px 0;
}
QHeaderView::section:hover {
    background: #e0e0e0;
    color: #111111;
}
QHeaderView::section:last {
    border-right: 0;
}
QHeaderView::up-arrow {
    image: url(:/png/resources/png/sort-asc.png);
    width: 0px;
}
QHeaderView::down-arrow {
    image: url(:/png/resources/png/sort-desc.png);
    width: 0px;
}
/* Context menus, toolbar drop-downs #QMenu    */
QMenu {
    background-color: #ffffff;
    border-color: #f0f0f0;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}
QMenu::item {
    background: transparent;
    padding: 4px 20px;
}
QMenu::item:selected,
QMenuBar::item:selected {
    background-color: #e0e0e0;
}
QMenu::item:disabled {
    background-color: transparent;
}
QMenu::separator {
    background-color: #f0f0f0;
    height: 1px;
    margin: 1px 0;
}
QMenu::icon {
    margin: 1px;
}
QMenu::right-arrow {
    image: url(:/png/resources/png/sub-menu-arrow.png);
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 0.5em;
}
QMenu QPushButton {
    background-color: transparent;
    border-color: #cccccc;
    margin: 1px 0 1px 0;
}
QMenu QCheckBox,
QMenu QRadioButton {
    background-color: transparent;
    padding: 5px 2px;
}
/* Tool tips #QToolTip, #SaveGameInfoWidget */
QToolTip,
SaveGameInfoWidget {
    background-color: #f0f0f0;
    border-color: #dddddd;
    color: #333333;
    border-style: solid;
    border-width: 1px;
    padding: 2px;
}
QStatusBar::item {
    border: None;
}
/* Progress Bars (Downloads) #QProgressBar */
QProgressBar {
    background-color: #e6e6e6;
    color: #000;
    border-color: #bcbcbc;
    text-align: center;
    border-style: solid;
    border-width: 1px;
    margin: 0px;
}
QProgressBar::chunk {
    background: #06b025;
}
DownloadListView[downloadView=standard]::item {
    padding: 16px;
}
DownloadListView[downloadView=compact]::item {
    padding: 4px;
}
/* Right Pane and Tab Bars #QTabWidget, #QTabBar */
QTabWidget::pane {
    border-color: #cccccc;
    border-top-color: #4a90e2;
    top: 0;
    border-style: solid;
    border-width: 1px;
}
QTabWidget::pane:disabled {
    border-top-color: #cccccc;
}
QTabBar::tab {
    background-color: transparent;
    padding: 4px 1em;
    border: none;
}
QTabBar::tab:hover {
    background-color: #3c85d8;
}
QTabBar::tab:selected,
QTabBar::tab:selected:hover {
    background-color: #4a90e2;
}
QTabBar::tab:disabled {
    background-color: transparent;
    color: #999999;
}
QTabBar::tab:selected:disabled {
    background-color: #f0f0f0;
}
/* Scrollers */
QTabBar QToolButton {
    background-color: #f0f0f0;
    border-color: #cccccc;
    padding: 1px;
    margin: 0;
    border-style: solid;
    border-width: 1px;
}
QTabBar QToolButton:hover {
    border-color: #4a90e2;
    border-width: 1px;
    border-style: solid;
}
QTabBar QToolButton:disabled,
QTabBar QToolButton:pressed:hover {
    background-color: #f0f0f0;
}
QTabBar::scroller {
    width: 23px;
    background-color: red;
}
QTabBar QToolButton::right-arrow {
    image: url(:/png/resources/png/scrollbar-right.png);
}
QTabBar QToolButton::right-arrow:hover {
    image: url(:/png/resources/png/scrollbar-right-hover.png);
}
QTabBar QToolButton::left-arrow {
    image: url(:/png/resources/png/scrollbar-left.png);
}
QTabBar QToolButton::left-arrow:hover {
    image: url(:/png/resources/png/scrollbar-left-hover.png);
}
/* Special styles */
QWidget#tabImages QPushButton {
    background-color: transparent;
    margin: 0 0.3em;
    padding: 0;
}
/* like dialog QPushButton*/
QWidget#tabESPs QToolButton {
    color: #000000;
    background-color: #dddddd;
    border-color: #707070;
    border-style: solid;
    border-width: 1px;
}
QWidget#tabESPs QToolButton:hover {
    background-color: #BEE6FD;
    border-color: #3c7fb1;
}
QWidget#tabESPs QToolButton:focus {
    background-color: #dddddd;
    border-color: #4a90e2;
}
QWidget#tabESPs QToolButton:disabled {
    background-color: #f0f0f0;
    border-color: #cccccc;
}
QTreeWidget#categoriesList {
    /* min-width: 225px; */
}
QTreeWidget#categoriesList::item {
    background-position: center left;
    background-repeat: no-repeat;
    padding: 0.35em 10px;
}
QTreeWidget#categoriesList::item:has-children {
    background-image: url(:/png/resources/png/branch-closed.png);
}
QTreeWidget#categoriesList::item:has-children:open {
    background-image: url(:/png/resources/png/branch-open.png);
}
QDialog#QueryOverwriteDialog QPushButton {
    margin-left: 0.5em;
}
QDialog#PyCfgDialog QPushButton:hover {
    background-color: #BEE6FD;
}
QLineEdit#modFilterEdit {
    margin-top: 2px;
}
/* highlight unchecked BSAs */
QWidget#bsaTab QTreeWidget::indicator:unchecked {
    background-color: #4a90e2;
}
/* increase version text field */
QLineEdit#versionEdit {
    max-width: 100px;
}
/* Dialogs width changes */
/* increase width to prevent buttons cutting */
QDialog#QueryOverwriteDialog {
    min-width: 565px;
}
QDialog#ModInfoDialog {
    min-width: 850px;
}
QLineEdit[valid-filter=false] {
    background-color: #ffdddd !important;
}
/* Ñ  Ð¾Ð±Ñ  Ñ  Ð²ÐµÐ½Ð½Ð¾Ðµ Ñ  ÐµÑ  ÐµÐ½Ð¸Ðµ */
QToolBar QToolButton:disabled {
    background-color: #f5f5f5;
}
QToolBar QToolButton:checked {
    background-color: #4a90e2;
}

/* Оптимизация для QFormLayout и WrapLongRows */
QFormLayout {
    /* Обеспечиваем правильное поведение переноса */
    spacing: 6px;
}

/* Убираем жёсткие ограничения ширины для виджетов в формах */
QWidget[qformLayoutWidget="true"] QLineEdit,
QWidget[qformLayoutWidget="true"] QComboBox,
QWidget[qformLayoutWidget="true"] QSpinBox,
QWidget[qformLayoutWidget="true"] QDoubleSpinBox {
    max-width: none;
    min-width: 50px; /* Минимальная разумная ширина */
}

/* Минимальная ширина правого блока с вкладками (на основе золотого сечения) */
QGroupBox[objectName="gb_right"],
QWidget[objectName="gb_right"] {
    min-width: 400px;
}


"""
