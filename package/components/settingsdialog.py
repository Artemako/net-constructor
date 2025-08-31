from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QComboBox, QCheckBox, QGroupBox, QSizePolicy, QScrollArea, QWidget
)
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, obsm):
        self.__obsm = obsm
        super(SettingsDialog, self).__init__()
        
        # СТИЛЬ
        self.__obsm.obj_style.set_style_for(self)
        self.setWindowTitle("Параметры приложения")
        
        # Конфигурация
        self.config_ui()
        self.load_settings()
        self.connecting_actions()
        
        # Свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def config_ui(self):
        """Настройка пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Создаем прокручиваемую область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Создаем виджет для содержимого
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        # Тема приложения
        theme_group = QGroupBox("Тема приложения")
        theme_layout = QHBoxLayout()
        theme_layout.setContentsMargins(10, 10, 10, 10)
        theme_layout.setSpacing(10)
        
        theme_label = QLabel("Тема:")
        theme_label.setMinimumWidth(60)
        theme_label.setMaximumWidth(60)
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        # Используем русские названия тем
        self.theme_combo.addItems(["Тёмная", "Светлая"])
        self.theme_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        theme_layout.addWidget(self.theme_combo)
        
        self.theme_reset_btn = QPushButton("Сброс")
        self.theme_reset_btn.setToolTip("Сбросить к значению по умолчанию")
        self.theme_reset_btn.setFixedWidth(60)
        theme_layout.addWidget(self.theme_reset_btn)
        
        theme_group.setLayout(theme_layout)
        content_layout.addWidget(theme_group)
        
        # Отображение параметров
        parameters_group = QGroupBox("Отображение параметров")
        parameters_layout = QHBoxLayout()
        parameters_layout.setContentsMargins(10, 10, 10, 10)
        parameters_layout.setSpacing(10)
        
        self.show_parameters_checkbox = QCheckBox("Отображать панель параметров")
        self.show_parameters_checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        parameters_layout.addWidget(self.show_parameters_checkbox)
        
        self.parameters_reset_btn = QPushButton("Сброс")
        self.parameters_reset_btn.setToolTip("Сбросить к значению по умолчанию")
        self.parameters_reset_btn.setFixedWidth(60)
        parameters_layout.addWidget(self.parameters_reset_btn)
        
        parameters_group.setLayout(parameters_layout)
        content_layout.addWidget(parameters_group)
        

        
        # Общий сброс всех настроек
        reset_all_group = QGroupBox("Сброс всех настроек")
        reset_all_layout = QHBoxLayout()
        reset_all_layout.setContentsMargins(10, 10, 10, 10)
        
        self.reset_all_btn = QPushButton("Сбросить все настройки к значениям по умолчанию")
        self.reset_all_btn.setToolTip("Сбросить все настройки к значениям по умолчанию")
        self.reset_all_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        reset_all_layout.addWidget(self.reset_all_btn)
        
        reset_all_group.setLayout(reset_all_layout)
        content_layout.addWidget(reset_all_group)
        
        # Устанавливаем виджет в прокручиваемую область
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(10)
        
        buttons_layout.addStretch()
        
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFixedWidth(100)
        buttons_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        self.resize(500, 400)
        
        # Устанавливаем политику изменения размера
        self.setMinimumSize(450, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def connecting_actions(self):
        """Подключение обработчиков событий"""
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Кнопки сброса отдельных параметров
        self.theme_reset_btn.clicked.connect(self.reset_theme)
        self.parameters_reset_btn.clicked.connect(self.reset_parameters)
        
        # Кнопка общего сброса
        self.reset_all_btn.clicked.connect(self.reset_all_settings)
        
        # Горячие клавиши
        self.save_btn.setShortcut("Ctrl+S")
        self.cancel_btn.setShortcut("Ctrl+Q")

    def reset_theme(self):
        """Сброс темы к значению по умолчанию"""
        self.theme_combo.setCurrentText("Тёмная")

    def reset_parameters(self):
        """Сброс настройки отображения параметров к значению по умолчанию"""
        self.show_parameters_checkbox.setChecked(False)



    def reset_all_settings(self):
        """Сброс всех настроек к значениям по умолчанию"""
        # Сброс темы
        self.theme_combo.setCurrentText("Тёмная")
        
        # Сброс настройки отображения параметров
        self.show_parameters_checkbox.setChecked(False)
        


    def load_settings(self):
        """Загрузка текущих настроек"""
        # Загрузка темы (получаем русское название)
        theme_display = self.__obsm.obj_settings.get_theme_display_name()
        self.theme_combo.setCurrentText(theme_display)
        
        # Загрузка настройки отображения параметров
        self.__original_show_parameters = self.__obsm.obj_settings.get_show_parameters()
        self.show_parameters_checkbox.setChecked(self.__original_show_parameters)
        


    def save_settings(self):
        """Сохранение настроек"""
        try:
            # Сохранение темы (используем русское название для установки)
            theme_display = self.theme_combo.currentText()
            self.__obsm.obj_settings.set_theme_by_display_name(theme_display)
            
            # Применение новой темы
            theme_english = self.__obsm.obj_settings.get_theme()
            self.__obsm.obj_style.apply_theme_to_all_windows(theme_english)
            
            # Сохранение настройки отображения параметров
            show_parameters = self.show_parameters_checkbox.isChecked()
            self.__obsm.obj_settings.set_show_parameters(show_parameters)
            

            
            self.__obsm.obj_settings.sync()
            
            # Обновление отображения параметров в главном окне только если настройка изменилась
            if show_parameters != self.__original_show_parameters:
                # Синхронизируем состояние действия с новой настройкой
                self.__obsm.obj_mw.ui.action_parameters.setChecked(show_parameters)
                self.__obsm.obj_mw._toggle_parameters_visibility()
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при сохранении настроек: {str(e)}"
            )
